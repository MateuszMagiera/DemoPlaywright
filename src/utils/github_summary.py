"""Write pytest summaries to the GitHub Actions step summary file."""

from __future__ import annotations

import os
from pathlib import Path


def write_github_summary(passed: int, failed: int, skipped: int, duration: float) -> None:
    """Append a Markdown summary to the GitHub Actions step summary file if present."""
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    path = Path(summary_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "## 🧪 Test Results",
        "",
        "| Status | Count |",
        "|--------|-------|",
        f"| ✅ Passed | {passed} |",
        f"| ❌ Failed | {failed} |",
        f"| ⏭️ Skipped | {skipped} |",
        f"| ⏱️ Duration | {duration:.2f}s |",
        "",
    ]
    path.write_text(
        path.read_text(encoding="utf-8") + "\n".join(lines), encoding="utf-8"
    ) if path.exists() else path.write_text("\n".join(lines), encoding="utf-8")
