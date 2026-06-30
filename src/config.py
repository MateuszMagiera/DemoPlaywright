from __future__ import annotations

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project-wide settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Target application
    base_url: str = "https://demoqa.com"

    # Browser settings
    browser: str = "chromium"
    headless: bool = True
    slow_mo: float = 0.0

    # Timeouts (milliseconds)
    default_timeout: int = 30_000
    navigation_timeout: int = 30_000

    # Tracing / artifacts
    tracing: str = "retain-on-failure"  # off | on | retain-on-failure
    video: str = "retain-on-failure"  # off | on | retain-on-failure

    # Reporting
    allure_results_dir: str = "reports/allure-results"
    html_report_path: str = "reports/report.html"
    screenshots_dir: str = "reports/screenshots"

    @field_validator("browser")
    @classmethod
    def browser_must_be_valid(cls, v: str) -> str:
        allowed = {"chromium", "firefox", "webkit"}
        if v not in allowed:
            raise ValueError(f"browser must be one of {allowed}, got '{v}'")
        return v

    @field_validator("tracing", "video")
    @classmethod
    def artifact_mode_must_be_valid(cls, v: str) -> str:
        allowed = {"off", "on", "retain-on-failure"}
        if v not in allowed:
            raise ValueError(f"value must be one of {allowed}, got '{v}'")
        return v


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached singleton of Settings."""
    return Settings()
