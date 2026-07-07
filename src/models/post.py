"""Pydantic models for JSONPlaceholder /posts endpoints."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator


class Post(BaseModel):
    """Post object from JSONPlaceholder API."""

    model_config = ConfigDict(populate_by_name=True)

    userId: int  # noqa: N815 — matches API field name
    id: int
    title: str
    body: str

    @field_validator("title", "body")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title and body must not be empty.")
        return v


class CreatePostRequest(BaseModel):
    """Payload for POST /posts."""

    title: str
    body: str
    userId: int  # noqa: N815


class CreatePostResponse(BaseModel):
    """Response from POST /posts (JSONPlaceholder echoes input + assigns id)."""

    id: int
    title: str
    body: str
    userId: int  # noqa: N815
