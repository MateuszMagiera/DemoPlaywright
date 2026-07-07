"""Shared fixtures and helpers for API tests."""

from __future__ import annotations

from typing import Any, TypeVar

import pytest_asyncio
from pydantic import BaseModel

from src.api.base_client import ApiClient, ApiResponse

M = TypeVar("M", bound=BaseModel)

# ── Base URLs ──────────────────────────────────────────────────────────────────

REQRES_BASE_URL = "https://reqres.in/api"
JSONPLACEHOLDER_BASE_URL = "https://jsonplaceholder.typicode.com"
HTTPBIN_BASE_URL = "https://httpbin.org"


# ── Client fixtures ────────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def reqres_client() -> ApiClient:  # type: ignore[misc]
    """Async API client pointing at ReqRes."""
    async with ApiClient(REQRES_BASE_URL) as client:
        yield client


@pytest_asyncio.fixture
async def jsonplaceholder_client() -> ApiClient:  # type: ignore[misc]
    """Async API client pointing at JSONPlaceholder."""
    async with ApiClient(JSONPLACEHOLDER_BASE_URL) as client:
        yield client


@pytest_asyncio.fixture
async def httpbin_client() -> ApiClient:  # type: ignore[misc]
    """Async API client pointing at httpbin."""
    async with ApiClient(HTTPBIN_BASE_URL) as client:
        yield client


# ── Assertion helpers ─────────────────────────────────────────────────────────


def assert_response(response: ApiResponse, *, status: int) -> None:
    """Assert that *response* has the expected HTTP *status* code."""
    assert (
        response.status == status
    ), f"Expected HTTP {status}, got {response.status}.\nBody: {response.body}"


def assert_response_schema(response: ApiResponse, *, status: int, schema: type[M]) -> M:
    """Assert status and validate the response body against *schema*.

    Returns the validated Pydantic model instance.
    """
    assert_response(response, status=status)
    return schema.model_validate(response.json())


def assert_field(body: Any, field: str, expected: Any) -> None:
    """Assert that *body[field]* equals *expected*."""
    actual = body[field] if isinstance(body, dict) else getattr(body, field)
    assert actual == expected, f"Expected {field}={expected!r}, got {actual!r}"
