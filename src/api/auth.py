"""Auth manager — Bearer token storage and auto-injection."""

from __future__ import annotations

import base64
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class TokenPayload:
    """Parsed JWT payload (no signature verification — for testing only)."""

    raw: str
    claims: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_jwt(cls, token: str) -> TokenPayload:
        """Decode JWT payload without verifying signature."""
        try:
            parts = token.split(".")
            if len(parts) < 2:
                return cls(raw=token)
            # Pad base64 to multiple of 4
            padding = "=" * (4 - len(parts[1]) % 4)
            payload_bytes = base64.urlsafe_b64decode(parts[1] + padding)
            claims = json.loads(payload_bytes)
            return cls(raw=token, claims=claims)
        except Exception as exc:
            logger.debug("Could not parse JWT payload: %s", exc)
            return cls(raw=token)

    def is_expired(self) -> bool:
        """Return True if the token has an 'exp' claim that is in the past."""
        exp = self.claims.get("exp")
        if exp is None:
            return False
        return bool(datetime.now(tz=timezone.utc).timestamp() > exp)

    def subject(self) -> str | None:
        """Return the 'sub' claim value, if present."""
        return self.claims.get("sub")


class AuthManager:
    """Manages authentication tokens for API test sessions.

    Usage:
        auth = AuthManager()
        auth.set_token("eyJhbGc...")
        client.set_auth_token(auth.get_token())
    """

    def __init__(self) -> None:
        self._token: str | None = None
        self._payload: TokenPayload | None = None

    def set_token(self, token: str) -> None:
        """Store a token and parse its payload."""
        self._token = token
        self._payload = TokenPayload.from_jwt(token)
        logger.debug("Auth token set", extra={"subject": self._payload.subject()})

    def get_token(self) -> str:
        """Return the stored token, raising if not set."""
        if self._token is None:
            raise RuntimeError("No auth token set. Call set_token() first.")
        return self._token

    def get_payload(self) -> TokenPayload:
        """Return the parsed token payload."""
        if self._payload is None:
            raise RuntimeError("No auth token set.")
        return self._payload

    def is_token_expired(self) -> bool:
        """Return True if the stored token is expired."""
        if self._payload is None:
            return True
        return self._payload.is_expired()

    def clear(self) -> None:
        """Remove the stored token."""
        self._token = None
        self._payload = None

    def has_token(self) -> bool:
        """Return True if a token is stored."""
        return self._token is not None

    def bearer_header(self) -> dict[str, str]:
        """Return a dict suitable for use as an Authorization header."""
        return {"Authorization": f"Bearer {self.get_token()}"}
