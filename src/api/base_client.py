"""Async API client with retry logic, response wrapping, and structured logging."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any

import httpx

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Custom exceptions
# ──────────────────────────────────────────────────────────────────────────────


class ApiError(Exception):
    """Raised when an API call fails with a non-2xx status code."""

    def __init__(self, status: int, body: Any, url: str) -> None:
        self.status = status
        self.body = body
        self.url = url
        super().__init__(f"API error {status} for {url}: {body}")


class ApiTimeoutError(ApiError):
    """Raised when the API call times out."""

    def __init__(self, url: str) -> None:
        super().__init__(408, "Request timed out", url)


# ──────────────────────────────────────────────────────────────────────────────
# Response wrapper
# ──────────────────────────────────────────────────────────────────────────────


@dataclass
class ApiResponse:
    """Thin wrapper around httpx.Response for consistent access patterns."""

    status: int
    body: Any
    headers: dict[str, str] = field(default_factory=dict)
    url: str = ""

    @classmethod
    def from_httpx(cls, response: httpx.Response) -> ApiResponse:
        """Build ApiResponse from a raw httpx.Response."""
        try:
            body = response.json()
        except Exception:
            body = response.text
        return cls(
            status=response.status_code,
            body=body,
            headers=dict(response.headers),
            url=str(response.url),
        )

    def json(self) -> Any:
        """Return the parsed JSON body (same as .body for API responses)."""
        return self.body

    def is_success(self) -> bool:
        """Return True if status is 2xx."""
        return 200 <= self.status < 300


# ──────────────────────────────────────────────────────────────────────────────
# API Client
# ──────────────────────────────────────────────────────────────────────────────


class ApiClient:
    """Async HTTP client with retry logic, default headers, and logging.

    Usage:
        async with ApiClient("https://reqres.in/api") as client:
            response = await client.get("/users/1")

    Or as a plain object (manual lifecycle):
        client = ApiClient("https://reqres.in/api")
        await client.start()
        response = await client.get("/users/1")
        await client.stop()
    """

    DEFAULT_HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        max_retries: int = 3,
        retry_delay: float = 0.5,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        headers = {**self.DEFAULT_HEADERS, **(extra_headers or {})}
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
        )

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    async def start(self) -> None:
        """No-op placeholder — client is created in __init__."""

    async def stop(self) -> None:
        """Close the underlying httpx client."""
        await self._client.aclose()

    async def __aenter__(self) -> ApiClient:
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.stop()

    # ── HTTP methods ──────────────────────────────────────────────────────────

    async def get(self, path: str, **kwargs: Any) -> ApiResponse:
        """Perform a GET request with retry logic."""
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> ApiResponse:
        """Perform a POST request."""
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> ApiResponse:
        """Perform a PUT request."""
        return await self._request("PUT", path, **kwargs)

    async def patch(self, path: str, **kwargs: Any) -> ApiResponse:
        """Perform a PATCH request."""
        return await self._request("PATCH", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> ApiResponse:
        """Perform a DELETE request."""
        return await self._request("DELETE", path, **kwargs)

    # ── Core request logic ────────────────────────────────────────────────────

    async def _request(self, method: str, path: str, **kwargs: Any) -> ApiResponse:
        """Execute request with exponential back-off retry on transient errors."""
        last_exc: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(
                    "API request",
                    extra={"method": method, "path": path, "attempt": attempt},
                )
                response = await self._client.request(method, path, **kwargs)
                api_response = ApiResponse.from_httpx(response)
                logger.debug(
                    "API response",
                    extra={"status": api_response.status, "url": api_response.url},
                )
                return api_response

            except httpx.TimeoutException as exc:
                last_exc = exc
                logger.warning(
                    "Request timeout",
                    extra={"method": method, "path": path, "attempt": attempt},
                )
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * attempt)

            except httpx.RequestError as exc:
                last_exc = exc
                logger.warning(
                    "Request error",
                    extra={"method": method, "path": path, "error": str(exc)},
                )
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * attempt)

        # All retries exhausted
        url = f"{self.base_url}{path}"
        if isinstance(last_exc, httpx.TimeoutException):
            raise ApiTimeoutError(url) from last_exc
        raise ApiError(0, str(last_exc), url) from last_exc

    # ── Token injection helper ─────────────────────────────────────────────────

    def set_auth_token(self, token: str) -> None:
        """Set a Bearer token on all subsequent requests."""
        self._client.headers["Authorization"] = f"Bearer {token}"

    def clear_auth_token(self) -> None:
        """Remove the Authorization header."""
        self._client.headers.pop("Authorization", None)
