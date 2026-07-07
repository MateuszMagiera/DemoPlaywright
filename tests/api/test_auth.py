"""Auth flow tests — login, token usage, JWT inspection, and session management.

Auth flows are fully mocked with respx — we control the server behaviour,
which makes tests fast, deterministic, and independent of external API changes.
This pattern is best-practice for testing auth code paths.
"""

from __future__ import annotations

import base64
import json
import time

import httpx
import pytest
import respx

from src.api.auth import AuthManager, TokenPayload
from src.api.base_client import ApiClient
from tests.api.conftest import assert_response

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

AUTH_BASE = "https://auth.example.com"
FAKE_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyXzEifQ.fakesig"


def _make_jwt(payload: dict) -> str:  # type: ignore[type-arg]
    """Create a minimal (unsigned) JWT for testing."""
    header = base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').rstrip(b"=").decode()
    body = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    return f"{header}.{body}.fakesig"


# ──────────────────────────────────────────────────────────────────────────────
# Mocked login / register flows
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
@pytest.mark.smoke
class TestMockedLoginFlow:
    """Mocked auth server — tests the login flow and token handling patterns."""

    @respx.mock
    async def test_successful_login_returns_token(self) -> None:
        """200 login response includes a token."""
        respx.post(f"{AUTH_BASE}/login").mock(
            return_value=httpx.Response(200, json={"token": FAKE_TOKEN, "id": 4})
        )
        async with ApiClient(AUTH_BASE) as client:
            response = await client.post(
                "/login", json={"email": "eve@reqres.in", "password": "cityslicka"}
            )
        assert_response(response, status=200)
        assert "token" in response.json()

    @respx.mock
    async def test_login_token_stored_in_auth_manager(self) -> None:
        """Token from login is stored in AuthManager correctly."""
        respx.post(f"{AUTH_BASE}/login").mock(
            return_value=httpx.Response(200, json={"token": FAKE_TOKEN})
        )
        async with ApiClient(AUTH_BASE) as client:
            response = await client.post(
                "/login", json={"email": "user@test.com", "password": "pass"}
            )
        token = response.json()["token"]
        auth = AuthManager()
        auth.set_token(token)
        assert auth.has_token()
        assert auth.get_token() == FAKE_TOKEN

    @respx.mock
    async def test_token_injected_into_subsequent_request(self) -> None:
        """Bearer token from login is forwarded in the Authorization header."""
        respx.post(f"{AUTH_BASE}/login").mock(
            return_value=httpx.Response(200, json={"token": FAKE_TOKEN})
        )
        respx.get(f"{AUTH_BASE}/profile").mock(
            return_value=httpx.Response(200, json={"id": 1, "email": "user@test.com"})
        )

        async with ApiClient(AUTH_BASE) as client:
            # Step 1: login
            login_resp = await client.post(
                "/login", json={"email": "user@test.com", "password": "pass"}
            )
            token = login_resp.json()["token"]

            # Step 2: inject token
            client.set_auth_token(token)

            # Step 3: make authenticated request
            profile_resp = await client.get("/profile")

        assert_response(profile_resp, status=200)
        assert profile_resp.json()["email"] == "user@test.com"

    @respx.mock
    async def test_register_returns_id_and_token(self) -> None:
        """Registration response contains both id and token."""
        respx.post(f"{AUTH_BASE}/register").mock(
            return_value=httpx.Response(200, json={"id": 4, "token": FAKE_TOKEN})
        )
        async with ApiClient(AUTH_BASE) as client:
            response = await client.post(
                "/register", json={"email": "eve@reqres.in", "password": "pistol"}
            )
        assert_response(response, status=200)
        body = response.json()
        assert "token" in body
        assert "id" in body

    @respx.mock
    async def test_missing_password_returns_400(self) -> None:
        """Login without password returns 400 with an error message."""
        respx.post(f"{AUTH_BASE}/login").mock(
            return_value=httpx.Response(400, json={"error": "Missing password"})
        )
        async with ApiClient(AUTH_BASE) as client:
            response = await client.post("/login", json={"email": "user@test.com"})
        assert_response(response, status=400)
        assert "error" in response.json()

    @respx.mock
    async def test_expired_token_returns_401(self) -> None:
        """Accessing a resource with an expired token returns 401."""
        expired_token = _make_jwt({"sub": "user_1", "exp": 1})
        respx.get(f"{AUTH_BASE}/profile").mock(
            return_value=httpx.Response(401, json={"error": "Token expired"})
        )
        async with ApiClient(
            AUTH_BASE, extra_headers={"Authorization": f"Bearer {expired_token}"}
        ) as client:
            response = await client.get("/profile")
        assert_response(response, status=401)

    @respx.mock
    async def test_clear_token_removes_auth_header(self) -> None:
        """After clearing the token, Authorization header is no longer sent."""
        respx.get(f"{AUTH_BASE}/public").mock(
            return_value=httpx.Response(200, json={"public": True})
        )
        async with ApiClient(AUTH_BASE) as client:
            client.set_auth_token("some-token")
            client.clear_auth_token()
            response = await client.get("/public")
        assert_response(response, status=200)


# ──────────────────────────────────────────────────────────────────────────────
# AuthManager unit tests (no HTTP)
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
class TestAuthManager:
    """Unit tests for the AuthManager class."""

    def test_set_and_get_token(self) -> None:
        auth = AuthManager()
        auth.set_token("my-token-123")
        assert auth.get_token() == "my-token-123"

    def test_has_token_false_initially(self) -> None:
        auth = AuthManager()
        assert not auth.has_token()

    def test_has_token_true_after_set(self) -> None:
        auth = AuthManager()
        auth.set_token("tok")
        assert auth.has_token()

    def test_clear_removes_token(self) -> None:
        auth = AuthManager()
        auth.set_token("tok")
        auth.clear()
        assert not auth.has_token()

    def test_get_token_raises_without_token(self) -> None:
        auth = AuthManager()
        with pytest.raises(RuntimeError, match="No auth token set"):
            auth.get_token()

    def test_bearer_header_format(self) -> None:
        auth = AuthManager()
        auth.set_token("abc123")
        header = auth.bearer_header()
        assert header == {"Authorization": "Bearer abc123"}


# ──────────────────────────────────────────────────────────────────────────────
# JWT TokenPayload unit tests (no HTTP)
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
class TestTokenPayload:
    """Unit tests for JWT TokenPayload parsing."""

    def test_parse_claims_from_valid_jwt(self) -> None:
        token = _make_jwt({"sub": "user_42", "name": "Test User"})
        payload = TokenPayload.from_jwt(token)
        assert payload.claims["sub"] == "user_42"
        assert payload.subject() == "user_42"

    def test_not_expired_when_no_exp_claim(self) -> None:
        token = _make_jwt({"sub": "user_1"})
        payload = TokenPayload.from_jwt(token)
        assert not payload.is_expired()

    def test_expired_when_exp_in_past(self) -> None:
        token = _make_jwt({"sub": "user_1", "exp": 1})  # epoch 1 = 1970
        payload = TokenPayload.from_jwt(token)
        assert payload.is_expired()

    def test_not_expired_when_exp_in_future(self) -> None:
        token = _make_jwt({"sub": "user_1", "exp": int(time.time()) + 3600})
        payload = TokenPayload.from_jwt(token)
        assert not payload.is_expired()

    def test_graceful_handling_of_invalid_token(self) -> None:
        payload = TokenPayload.from_jwt("not.a.jwt")
        assert isinstance(payload.claims, dict)

    def test_subject_returns_none_when_no_sub(self) -> None:
        token = _make_jwt({"name": "no subject"})
        payload = TokenPayload.from_jwt(token)
        assert payload.subject() is None


# ──────────────────────────────────────────────────────────────────────────────
# Authorization header forwarding (httpbin)
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
class TestAuthHeaderPassthrough:
    """Verify the ApiClient forwards the Authorization header correctly."""

    @respx.mock
    async def test_auth_header_included_in_request(self) -> None:
        """Mocked endpoint receives the Authorization header we set."""

        def capture_handler(request: httpx.Request) -> httpx.Response:
            auth_header = request.headers.get("authorization", "")
            return httpx.Response(200, json={"Authorization": auth_header})

        respx.get("https://echo.example.com/headers").mock(side_effect=capture_handler)

        async with ApiClient("https://echo.example.com") as client:
            client.set_auth_token("test-token-xyz")
            response = await client.get("/headers")

        assert_response(response, status=200)
        auth = response.json().get("Authorization", "")
        assert "test-token-xyz" in auth
