"""API tests — JSONPlaceholder /posts CRUD operations.

JSONPlaceholder (jsonplaceholder.typicode.com) is a reliable, free, open-source
fake REST API. No auth required, always available. Perfect for demonstrating
CRUD testing patterns.
"""

from __future__ import annotations

import pytest

from src.api.base_client import ApiClient
from src.models.post import CreatePostResponse, Post
from tests.api.conftest import assert_response, assert_response_schema

# ──────────────────────────────────────────────────────────────────────────────
# List / Read
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
@pytest.mark.smoke
class TestListPosts:
    """Tests for GET /posts (list of 100 posts)."""

    async def test_returns_200(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts")
        assert_response(response, status=200)

    async def test_returns_100_posts(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts")
        assert_response(response, status=200)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 100

    async def test_each_post_has_required_fields(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts")
        posts = response.json()
        for post in posts[:5]:  # sample first 5
            Post.model_validate(post)  # raises if schema invalid

    async def test_pagination_via_limit_filter(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts", params={"_limit": 5})
        assert_response(response, status=200)
        assert len(response.json()) == 5

    async def test_filter_by_user_id(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts", params={"userId": 1})
        posts = response.json()
        assert len(posts) > 0
        assert all(p["userId"] == 1 for p in posts)


@pytest.mark.api
@pytest.mark.smoke
class TestGetSinglePost:
    """Tests for GET /posts/{id}."""

    async def test_returns_200_for_existing_post(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts/1")
        assert_response(response, status=200)

    async def test_response_schema_valid(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts/1")
        post = assert_response_schema(response, status=200, schema=Post)
        assert post.id == 1

    @pytest.mark.parametrize(
        "post_id,expected_user",
        [
            (1, 1),
            (11, 2),
            (21, 3),
        ],
    )
    async def test_known_posts(
        self, jsonplaceholder_client: ApiClient, post_id: int, expected_user: int
    ) -> None:
        response = await jsonplaceholder_client.get(f"/posts/{post_id}")
        post = assert_response_schema(response, status=200, schema=Post)
        assert post.userId == expected_user

    async def test_returns_404_for_missing_post(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts/9999")
        assert_response(response, status=404)

    async def test_post_fields_are_non_empty(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.get("/posts/1")
        post = assert_response_schema(response, status=200, schema=Post)
        assert len(post.title.strip()) > 0
        assert len(post.body.strip()) > 0


# ──────────────────────────────────────────────────────────────────────────────
# Create
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
class TestCreatePost:
    """Tests for POST /posts (JSONPlaceholder echoes input + assigns id=101)."""

    async def test_create_returns_201(self, jsonplaceholder_client: ApiClient) -> None:
        payload = {"title": "Test Post", "body": "Test content", "userId": 1}
        response = await jsonplaceholder_client.post("/posts", json=payload)
        assert_response(response, status=201)

    async def test_create_response_schema_valid(self, jsonplaceholder_client: ApiClient) -> None:
        payload = {"title": "QA Post", "body": "Automation body", "userId": 2}
        response = await jsonplaceholder_client.post("/posts", json=payload)
        data = assert_response_schema(response, status=201, schema=CreatePostResponse)
        assert data.title == "QA Post"
        assert data.userId == 2
        assert data.id > 0

    async def test_create_echoes_title(self, jsonplaceholder_client: ApiClient) -> None:
        title = "Unique title for echo test 🦀"
        response = await jsonplaceholder_client.post(
            "/posts", json={"title": title, "body": "body", "userId": 1}
        )
        assert response.json()["title"] == title

    async def test_create_includes_generated_id(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.post(
            "/posts", json={"title": "T", "body": "B", "userId": 1}
        )
        assert "id" in response.json()


# ──────────────────────────────────────────────────────────────────────────────
# Update
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
class TestUpdatePost:
    """Tests for PUT and PATCH /posts/{id}."""

    async def test_put_returns_200(self, jsonplaceholder_client: ApiClient) -> None:
        payload = {"title": "Updated", "body": "Updated body", "userId": 1}
        response = await jsonplaceholder_client.put("/posts/1", json=payload)
        assert_response(response, status=200)

    async def test_put_echoes_updated_title(self, jsonplaceholder_client: ApiClient) -> None:
        payload = {"title": "PUT Updated Title", "body": "body", "userId": 1}
        response = await jsonplaceholder_client.put("/posts/1", json=payload)
        assert response.json()["title"] == "PUT Updated Title"

    async def test_patch_returns_200(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.patch("/posts/1", json={"title": "Patched"})
        assert_response(response, status=200)

    async def test_patch_echoes_changed_field(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.patch("/posts/1", json={"title": "PATCHED"})
        assert "PATCHED" in response.json().get("title", "")


# ──────────────────────────────────────────────────────────────────────────────
# Delete
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.api
class TestDeletePost:
    """Tests for DELETE /posts/{id}."""

    async def test_delete_returns_200(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.delete("/posts/1")
        assert_response(response, status=200)

    async def test_delete_body_is_empty_object(self, jsonplaceholder_client: ApiClient) -> None:
        response = await jsonplaceholder_client.delete("/posts/2")
        # JSONPlaceholder returns 200 with empty body {}
        body = response.json()
        assert body == {} or body is None or body == ""
