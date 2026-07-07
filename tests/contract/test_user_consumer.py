"""Consumer-side Pact contract tests for ReqRes User API.

Defines what our "MyApp" consumer expects from the "ReqRes" provider.
Generated pact files are saved to the pacts/ directory.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import requests
from pact import Consumer, Like, Provider  # type: ignore[import]

PACT_DIR = Path(__file__).parents[2] / "pacts"
PACT_DIR.mkdir(exist_ok=True)

PACT_MOCK_HOST = "localhost"
PACT_MOCK_PORT = 1234
PACT_MOCK_URL = f"http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}"


@pytest.fixture(scope="module")
def pact():  # type: ignore[no-untyped-def]
    """Create and manage the Pact consumer/provider pair."""
    pact = Consumer("MyApp").has_pact_with(
        Provider("ReqRes"),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
        pact_dir=str(PACT_DIR),
    )
    pact.start_service()
    yield pact
    pact.stop_service()


@pytest.mark.api
class TestUserConsumerPact:
    """Consumer contracts — what MyApp expects from the ReqRes provider."""

    def test_get_existing_user(self, pact) -> None:  # type: ignore[no-untyped-def]
        """GET /users/1 returns a user object with required fields."""
        expected_user = {
            "data": Like(
                {
                    "id": 1,
                    "email": "george.bluth@reqres.in",
                    "first_name": "George",
                    "last_name": "Bluth",
                    "avatar": "https://reqres.in/img/faces/1-image.jpg",
                }
            )
        }

        (
            pact.given("user 1 exists")
            .upon_receiving("a GET request for user 1")
            .with_request(method="GET", path="/api/users/1")
            .will_respond_with(status=200, body=expected_user)
        )

        with pact:
            response = requests.get(f"{PACT_MOCK_URL}/api/users/1", timeout=5)

        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert body["data"]["id"] == 1

    def test_get_missing_user(self, pact) -> None:  # type: ignore[no-untyped-def]
        """GET /users/9999 returns 404 for a non-existent user."""
        (
            pact.given("user 9999 does not exist")
            .upon_receiving("a GET request for non-existent user")
            .with_request(method="GET", path="/api/users/9999")
            .will_respond_with(status=404, body={})
        )

        with pact:
            response = requests.get(f"{PACT_MOCK_URL}/api/users/9999", timeout=5)

        assert response.status_code == 404

    def test_create_user(self, pact) -> None:  # type: ignore[no-untyped-def]
        """POST /users creates a new user and returns 201 with id and createdAt."""
        request_body = {"name": "Contract Tester", "job": "QA"}
        expected_response = {
            "id": Like("123"),
            "name": Like("Contract Tester"),
            "job": Like("QA"),
            "createdAt": Like("2024-01-01T00:00:00.000Z"),
        }

        (
            pact.given("a request to create a new user")
            .upon_receiving("a POST request to /users")
            .with_request(
                method="POST",
                path="/api/users",
                body=request_body,
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(status=201, body=expected_response)
        )

        with pact:
            response = requests.post(
                f"{PACT_MOCK_URL}/api/users",
                json=request_body,
                headers={"Content-Type": "application/json"},
                timeout=5,
            )

        assert response.status_code == 201
        body = response.json()
        assert "id" in body
        assert "createdAt" in body

    def test_delete_user(self, pact) -> None:  # type: ignore[no-untyped-def]
        """DELETE /users/2 returns 204 No Content."""
        (
            pact.given("user 2 exists")
            .upon_receiving("a DELETE request for user 2")
            .with_request(method="DELETE", path="/api/users/2")
            .will_respond_with(status=204)
        )

        with pact:
            response = requests.delete(f"{PACT_MOCK_URL}/api/users/2", timeout=5)

        assert response.status_code == 204
