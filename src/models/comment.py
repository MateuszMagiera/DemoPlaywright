"""Pydantic models for JSONPlaceholder /comments endpoints."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr


class Comment(BaseModel):
    """Comment object from JSONPlaceholder API."""

    model_config = ConfigDict(populate_by_name=True)

    postId: int  # noqa: N815 — matches API field name
    id: int
    name: str
    email: EmailStr
    body: str
