"""Pydantic models for ReqRes /users endpoints."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl, field_validator


class User(BaseModel):
    """Single user object returned by ReqRes API."""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl

    @field_validator("first_name", "last_name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Name fields must contain at least one non-whitespace character."""
        if not v.strip():
            raise ValueError("Name fields must not be empty or whitespace only.")
        return v

    @property
    def full_name(self) -> str:
        """Convenience property combining first and last name."""
        return f"{self.first_name} {self.last_name}"


class UserListResponse(BaseModel):
    """Paginated list of users from GET /users."""

    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[User]


class UserSingleResponse(BaseModel):
    """Single-user response wrapper from GET /users/{id}."""

    data: User


class CreateUserRequest(BaseModel):
    """Payload for POST /users."""

    name: str
    job: str


class CreateUserResponse(BaseModel):
    """Response from POST /users."""

    id: str
    name: str
    job: str
    createdAt: str  # noqa: N815 — matches API field name


class UpdateUserResponse(BaseModel):
    """Response from PUT /users/{id} or PATCH /users/{id}."""

    name: str
    job: str
    updatedAt: str  # noqa: N815 — matches API field name


class SupportInfo(BaseModel):
    """Optional support section in some ReqRes responses."""

    url: str
    text: str
