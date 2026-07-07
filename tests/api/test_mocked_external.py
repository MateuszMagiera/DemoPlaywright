"""Tests for HTTP mocking with respx — isolate external service calls."""

from __future__ import annotations

import httpx
import pytest
import respx

from src.api.base_client import ApiClient, ApiTimeoutError

PAYMENT_URL = "https://payment.example.com"
EMAIL_URL = "https://email.example.com"
SMS_URL = "https://sms.example.com"


@pytest.mark.api
class TestExternalServiceMocking:
    """Use respx to mock external service calls and test error-handling code paths."""

    @respx.mock
    async def test_successful_payment_returns_200(self) -> None:
        """Happy path: payment service responds 200."""
        respx.post(f"{PAYMENT_URL}/charge").mock(
            return_value=httpx.Response(
                200,
                json={"transaction_id": "txn_abc123", "status": "approved"},
            )
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PAYMENT_URL}/charge",
                json={"amount": 100, "currency": "USD"},
            )
        assert response.status_code == 200
        assert response.json()["status"] == "approved"

    @respx.mock
    async def test_payment_service_500_handled(self) -> None:
        """Payment service 500 → client receives the error response."""
        respx.post(f"{PAYMENT_URL}/charge").mock(
            return_value=httpx.Response(500, json={"error": "Internal Server Error"})
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PAYMENT_URL}/charge",
                json={"amount": 100},
            )
        assert response.status_code == 500

    @respx.mock
    async def test_payment_service_timeout_raises(self) -> None:
        """Payment service timeout → TimeoutException raised."""
        respx.post(f"{PAYMENT_URL}/charge").mock(
            side_effect=httpx.TimeoutException("timeout", request=None)
        )
        async with httpx.AsyncClient(timeout=1.0) as client:
            with pytest.raises(httpx.TimeoutException):
                await client.post(f"{PAYMENT_URL}/charge", json={"amount": 100})

    @respx.mock
    async def test_email_service_returns_accepted(self) -> None:
        """Email service returns 202 Accepted."""
        respx.post(f"{EMAIL_URL}/send").mock(
            return_value=httpx.Response(202, json={"message_id": "msg_xyz", "queued": True})
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{EMAIL_URL}/send",
                json={"to": "user@test.com", "subject": "Test"},
            )
        assert response.status_code == 202
        assert response.json()["queued"] is True

    @respx.mock
    async def test_sms_service_rate_limited(self) -> None:
        """SMS service returns 429 Too Many Requests."""
        respx.post(f"{SMS_URL}/send").mock(
            return_value=httpx.Response(
                429,
                json={"error": "Rate limit exceeded", "retry_after": 60},
                headers={"Retry-After": "60"},
            )
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SMS_URL}/send",
                json={"to": "+48123456789", "message": "Hello"},
            )
        assert response.status_code == 429
        assert response.headers["Retry-After"] == "60"

    @respx.mock
    async def test_network_connection_error(self) -> None:
        """Network error → ConnectError raised."""
        respx.get("https://unreachable.example.com/api").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )
        async with httpx.AsyncClient() as client:
            with pytest.raises(httpx.ConnectError):
                await client.get("https://unreachable.example.com/api")

    @respx.mock
    async def test_api_client_retries_on_timeout(self) -> None:
        """ApiClient retries up to max_retries on TimeoutException then raises."""
        call_count = 0

        def timeout_side_effect(request: httpx.Request) -> httpx.Response:
            nonlocal call_count
            call_count += 1
            raise httpx.TimeoutException("timeout", request=request)

        respx.get("https://flaky.example.com/data").mock(side_effect=timeout_side_effect)

        client = ApiClient(
            "https://flaky.example.com",
            timeout=1.0,
            max_retries=3,
            retry_delay=0.01,
        )
        with pytest.raises(ApiTimeoutError):
            await client.get("/data")

        # Should have attempted max_retries times
        assert call_count == 3, f"Expected 3 attempts, got {call_count}"
        await client.stop()


@pytest.mark.api
class TestRespxReqResIntercept:
    """Intercept real ReqRes calls with mocked responses."""

    @respx.mock
    async def test_mock_user_list_response(self) -> None:
        """Mock a user list response and verify the client processes it correctly."""
        mock_body = {
            "page": 1,
            "per_page": 6,
            "total": 12,
            "total_pages": 2,
            "data": [
                {
                    "id": 1,
                    "email": "mock@test.com",
                    "first_name": "Mock",
                    "last_name": "User",
                    "avatar": "https://reqres.in/img/faces/1-image.jpg",
                }
            ],
        }
        # Create client INSIDE the respx.mock context so it gets the patched transport
        respx.get("https://mock-api.example.com/users").mock(
            return_value=httpx.Response(200, json=mock_body)
        )

        async with ApiClient("https://mock-api.example.com") as client:
            response = await client.get("/users")

        assert response.status == 200
        assert response.json()["data"][0]["email"] == "mock@test.com"

    @respx.mock
    async def test_mock_delayed_response(self) -> None:
        """Mock a slow response to test timeout handling."""
        import asyncio

        async def slow_response(request: httpx.Request) -> httpx.Response:
            await asyncio.sleep(0.05)
            return httpx.Response(200, json={"ok": True})

        respx.get("https://slow.example.com/data").mock(side_effect=slow_response)

        async with httpx.AsyncClient() as client:
            response = await client.get("https://slow.example.com/data")

        assert response.status_code == 200
