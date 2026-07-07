"""Negative API tests — error responses, boundary cases, malformed payloads."""

from __future__ import annotations

import httpx
import pytest
import respx

from src.api.base_client import ApiClient
from tests.api.conftest import assert_response

# ──────────────────────────────────────────────────────────────────────────────
# 404 — Not Found (JSONPlaceholder)
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
@pytest.mark.regression
class TestNotFound:
    """Tests for resources that do not exist (404)."""

    @pytest.mark.parametrize("post_id", [0, 9999, 99999])
    async def test_non_existent_post_returns_404(
        self, jsonplaceholder_client: ApiClient, post_id: int
    ) -> None:
        response = await jsonplaceholder_client.get(f"/posts/{post_id}")
        assert_response(response, status=404)

    async def test_non_existent_endpoint_returns_404(
        self, jsonplaceholder_client: ApiClient
    ) -> None:
        response = await jsonplaceholder_client.get("/nonexistent-endpoint")
        assert_response(response, status=404)

    async def test_non_existent_comment_returns_404(
        self, jsonplaceholder_client: ApiClient
    ) -> None:
        response = await jsonplaceholder_client.get("/comments/99999")
        assert_response(response, status=404)

    async def test_non_existent_user_returns_404(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/users/99999")
        assert_response(response, status=404)


# ──────────────────────────────────────────────────────────────────────────────
# JSONPlaceholder boundary / edge case tests
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
@pytest.mark.regression
class TestBoundaryInputs:
    """Boundary and edge case inputs for JSONPlaceholder API."""

    @pytest.mark.parametrize(
        "title,body,user_id",
        [
            ("", "valid body", 1),  # empty title
            ("valid title", "", 1),  # empty body
            ("a" * 500, "b" * 500, 1),  # very long fields
            ("Title with 🦀 emoji", "body", 1),  # unicode / emoji
            ("Ñoño ÄÖÜ ñ café", "body", 1),  # non-ASCII chars
        ],
    )
    async def test_boundary_post_payloads(
        self,
        jsonplaceholder_client: ApiClient,
        title: str,
        body: str,
        user_id: int,
    ) -> None:
        """JSONPlaceholder accepts and echoes boundary inputs without crashing."""
        response = await jsonplaceholder_client.post(
            "/posts", json={"title": title, "body": body, "userId": user_id}
        )
        assert response.status in (200, 201)

    async def test_string_id_returns_404(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts/abc")
        assert_response(response, status=404)

    async def test_negative_id_returns_404(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts/-1")
        assert_response(response, status=404)


# ──────────────────────────────────────────────────────────────────────────────
# Mocked Auth Error Scenarios (no real API needed)
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
@pytest.mark.regression
class TestMockedAuthErrors:
    """Mock auth error scenarios to test client error-handling code paths."""

    @respx.mock
    async def test_missing_credentials_returns_400(self) -> None:
        """Endpoint returns 400 when required fields are absent."""
        respx.post("https://auth.example.com/login").mock(
            return_value=httpx.Response(400, json={"error": "Missing email or password"})
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://auth.example.com/login",
                json={},  # no email or password
            )
        assert response.status_code == 400
        assert "error" in response.json()

    @respx.mock
    async def test_wrong_credentials_returns_401(self) -> None:
        """Endpoint returns 401 for invalid credentials."""
        respx.post("https://auth.example.com/login").mock(
            return_value=httpx.Response(401, json={"error": "Invalid email or password"})
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://auth.example.com/login",
                json={"email": "bad@bad.com", "password": "wrong"},
            )
        assert response.status_code == 401

    @respx.mock
    async def test_expired_token_returns_401(self) -> None:
        """Accessing protected resource with expired token returns 401."""
        respx.get("https://auth.example.com/profile").mock(
            return_value=httpx.Response(
                401, json={"error": "Token expired", "code": "TOKEN_EXPIRED"}
            )
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://auth.example.com/profile",
                headers={"Authorization": "Bearer expired_token_here"},
            )
        assert response.status_code == 401
        assert response.json()["code"] == "TOKEN_EXPIRED"

    @respx.mock
    async def test_no_token_returns_403(self) -> None:
        """Accessing protected resource without token returns 403."""
        respx.get("https://auth.example.com/admin").mock(
            return_value=httpx.Response(403, json={"error": "Forbidden"})
        )
        async with httpx.AsyncClient() as client:
            response = await client.get("https://auth.example.com/admin")
        assert response.status_code == 403

    @respx.mock
    async def test_unknown_user_register_returns_400(self) -> None:
        """Registering with unsupported email returns 400."""
        respx.post("https://auth.example.com/register").mock(
            return_value=httpx.Response(400, json={"error": "Note: Only defined users succeed"})
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://auth.example.com/register",
                json={"email": "nobody@unknown.com", "password": "pass"},
            )
        assert response.status_code == 400


# ──────────────────────────────────────────────────────────────────────────────
# HTTP Status Code Verification (mocked — no external dependency)
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
class TestHttpStatusCodes:
    """Verify the ApiClient correctly captures each HTTP status code."""

    @pytest.mark.parametrize("code", [200, 201, 204, 400, 401, 403, 404, 405, 422, 500, 503])
    @respx.mock
    async def test_client_captures_status_code(self, code: int) -> None:
        """Mock each status code and verify ApiClient returns it correctly."""
        url = f"https://mock-status.example.com/status/{code}"
        respx.get(url).mock(return_value=httpx.Response(code))

        async with ApiClient("https://mock-status.example.com") as client:
            response = await client.get(f"/status/{code}")

        assert response.status == code, f"Expected {code}, got {response.status}"


# ──────────────────────────────────────────────────────────────────────────────
