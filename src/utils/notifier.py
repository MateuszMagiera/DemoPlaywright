"""Simple Slack webhook notifier for pytest session summaries."""

from __future__ import annotations

import json
import os
import urllib.request


class SlackNotifier:
    """Send simple text notifications to a Slack incoming webhook."""

    def __init__(self, webhook_url: str | None = None) -> None:
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")

    def send(self, message: str, webhook_url: str | None = None) -> bool:
        """Send a plain text message to Slack."""
        url = webhook_url or self.webhook_url
        if not url:
            return False

        payload = {"text": message}
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status < 400
        except Exception:
            return False

    def send_summary(
        self,
        passed: int,
        failed: int,
        skipped: int,
        duration: float,
        browser: str = "chromium",
        webhook_url: str | None = None,
    ) -> bool:
        """Send a compact pytest summary message to Slack."""
        message = (
            "🧪 Test Suite Finished\n"
            f"✅ Passed: {passed} | ❌ Failed: {failed} | ⏭️ Skipped: {skipped}\n"
            f"⏱️ Duration: {duration:.2f}s\n"
            f"🌐 Browser: {browser}"
        )
        return self.send(message, webhook_url=webhook_url)
