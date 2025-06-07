#!/usr/bin/env python3
"""Script to update coverage badge in README.md"""

import json
import re
import sys
from pathlib import Path


def get_coverage_percentage() -> int:
    """Get coverage percentage from coverage.json file."""
    coverage_file = Path("coverage.json")

    if not coverage_file.exists():
        print("coverage.json not found. Run 'uv run pytest' first.")
        sys.exit(1)

    with open(coverage_file) as f:
        coverage_data = json.load(f)

    total_coverage = coverage_data["totals"]["percent_covered"]
    return int(round(total_coverage))


def get_badge_color(percentage: int) -> str:
    """Get badge color based on coverage percentage."""
    if percentage >= 90:
        return "brightgreen"
    elif percentage >= 80:
        return "green"
    elif percentage >= 70:
        return "yellowgreen"
    elif percentage >= 60:
        return "yellow"
    elif percentage >= 50:
        return "orange"
    else:
        return "red"


def update_readme_badge(percentage: int) -> None:
    """Update coverage badge in README.md."""
    readme_file = Path("README.md")

    if not readme_file.exists():
        print("README.md not found.")
        sys.exit(1)

    content = readme_file.read_text()

    color = get_badge_color(percentage)
    new_badge = (
        f"![Coverage](https://img.shields.io/badge/coverage-{percentage}%25-{color})"
    )

    # Pattern to match existing coverage badge
    pattern = r"!\[Coverage\]\(https://img\.shields\.io/badge/coverage-\d+%25-\w+\)"

    if re.search(pattern, content):
        # Replace existing badge
        new_content = re.sub(pattern, new_badge, content)
    else:
        # Add badge after the main title
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("# ") and not line.startswith("## "):
                lines.insert(i + 2, new_badge)
                lines.insert(i + 3, "")
                break
        new_content = "\n".join(lines)

    readme_file.write_text(new_content)
    print(f"Updated README.md with coverage badge: {percentage}% ({color})")


def main() -> None:
    """Main function."""
    percentage = get_coverage_percentage()
    update_readme_badge(percentage)


if __name__ == "__main__":
    main()
