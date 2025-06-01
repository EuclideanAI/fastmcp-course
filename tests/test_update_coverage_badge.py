"""Tests for update_coverage_badge.py."""

import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from update_coverage_badge import (
    get_badge_color,
    get_coverage_percentage,
    main,
    update_readme_badge,
)


class TestGetCoveragePercentage:
    """Test get_coverage_percentage function."""

    def test_get_coverage_percentage_success(self, tmp_path: Path) -> None:
        """Test successful coverage percentage retrieval."""
        # Create a temporary coverage.json file
        coverage_data = {"totals": {"percent_covered": 85.67}}
        coverage_file = tmp_path / "coverage.json"
        coverage_file.write_text(json.dumps(coverage_data))

        # Mock Path to return our temp file
        with patch("update_coverage_badge.Path") as mock_path_class:
            mock_path_instance = mock_path_class.return_value
            mock_path_instance.exists.return_value = True

            with patch("builtins.open", mock_open(read_data=json.dumps(coverage_data))):
                result = get_coverage_percentage()

        assert result == 86  # Should be rounded

    def test_get_coverage_percentage_file_not_found(self) -> None:
        """Test when coverage.json file doesn't exist."""
        with patch("update_coverage_badge.Path") as mock_path:
            mock_path.return_value.exists.return_value = False

            with pytest.raises(SystemExit) as excinfo:
                with patch("builtins.print") as mock_print:
                    get_coverage_percentage()

            assert excinfo.value.code == 1
            mock_print.assert_called_once_with(
                "coverage.json not found. Run 'uv run pytest' first."
            )

    def test_get_coverage_percentage_rounding(self, tmp_path: Path) -> None:
        """Test rounding of coverage percentage."""
        test_cases = [
            (85.4, 85),
            (85.5, 86),
            (85.6, 86),
            (100.0, 100),
            (0.0, 0),
            (99.9, 100),
        ]

        for input_percent, expected_output in test_cases:
            coverage_data = {"totals": {"percent_covered": input_percent}}

            with patch("update_coverage_badge.Path") as mock_path:
                mock_path.return_value.exists.return_value = True

                with patch(
                    "builtins.open", mock_open(read_data=json.dumps(coverage_data))
                ):
                    result = get_coverage_percentage()

                assert result == expected_output


class TestGetBadgeColor:
    """Test get_badge_color function."""

    def test_get_badge_color_ranges(self) -> None:
        """Test badge color for different coverage ranges."""
        test_cases = [
            (95, "brightgreen"),
            (90, "brightgreen"),
            (89, "green"),
            (80, "green"),
            (79, "yellowgreen"),
            (70, "yellowgreen"),
            (69, "yellow"),
            (60, "yellow"),
            (59, "orange"),
            (50, "orange"),
            (49, "red"),
            (0, "red"),
            (100, "brightgreen"),
        ]

        for percentage, expected_color in test_cases:
            result = get_badge_color(percentage)
            assert (
                result == expected_color
            ), f"Expected {expected_color} for {percentage}%, got {result}"


class TestUpdateReadmeBadge:
    """Test update_readme_badge function."""

    def test_update_readme_badge_file_not_found(self) -> None:
        """Test when README.md file doesn't exist."""
        with patch("update_coverage_badge.Path") as mock_path:
            mock_path.return_value.exists.return_value = False

            with pytest.raises(SystemExit) as excinfo:
                with patch("builtins.print") as mock_print:
                    update_readme_badge(85)

            assert excinfo.value.code == 1
            mock_print.assert_called_once_with("README.md not found.")

    def test_update_readme_badge_replace_existing(self) -> None:
        """Test replacing existing coverage badge."""
        existing_content = """# My Project

![Coverage](https://img.shields.io/badge/coverage-75%25-yellowgreen)

Some content here.
"""

        expected_content = """# My Project

![Coverage](https://img.shields.io/badge/coverage-85%25-green)

Some content here.
"""

        with patch("update_coverage_badge.Path") as mock_path:
            mock_readme = mock_path.return_value
            mock_readme.exists.return_value = True
            mock_readme.read_text.return_value = existing_content

            with patch("builtins.print") as mock_print:
                update_readme_badge(85)

            mock_readme.write_text.assert_called_once_with(expected_content)
            mock_print.assert_called_once_with(
                "Updated README.md with coverage badge: 85% (green)"
            )

    def test_update_readme_badge_add_new(self) -> None:
        """Test adding new coverage badge when none exists."""
        existing_content = """# My Project

Some content here.
"""

        expected_content = """# My Project

![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)

Some content here.
"""

        with patch("update_coverage_badge.Path") as mock_path:
            mock_readme = mock_path.return_value
            mock_readme.exists.return_value = True
            mock_readme.read_text.return_value = existing_content

            with patch("builtins.print") as mock_print:
                update_readme_badge(92)

            mock_readme.write_text.assert_called_once_with(expected_content)
            mock_print.assert_called_once_with(
                "Updated README.md with coverage badge: 92% (brightgreen)"
            )

    def test_update_readme_badge_multiple_headers(self) -> None:
        """Test adding badge after main title when multiple headers exist."""
        existing_content = """# Main Project Title

## Section 1

Some content.

## Section 2

More content.
"""

        expected_content = """# Main Project Title

![Coverage](https://img.shields.io/badge/coverage-78%25-yellowgreen)

## Section 1

Some content.

## Section 2

More content.
"""

        with patch("update_coverage_badge.Path") as mock_path:
            mock_readme = mock_path.return_value
            mock_readme.exists.return_value = True
            mock_readme.read_text.return_value = existing_content

            with patch("builtins.print") as mock_print:
                update_readme_badge(78)

            mock_readme.write_text.assert_called_once_with(expected_content)
            mock_print.assert_called_once_with(
                "Updated README.md with coverage badge: 78% (yellowgreen)"
            )

    def test_update_readme_badge_no_main_header(self) -> None:
        """Test when no main header exists."""
        existing_content = """## Section 1

Some content here.

## Section 2

More content.
"""

        # When no main header is found, the badge should not be added
        with patch("update_coverage_badge.Path") as mock_path:
            mock_readme = mock_path.return_value
            mock_readme.exists.return_value = True
            mock_readme.read_text.return_value = existing_content

            with patch("builtins.print") as mock_print:
                update_readme_badge(85)

            # Should write the original content unchanged
            mock_readme.write_text.assert_called_once_with(existing_content)
            mock_print.assert_called_once_with(
                "Updated README.md with coverage badge: 85% (green)"
            )

    def test_update_readme_badge_different_coverage_levels(self) -> None:
        """Test badge generation for different coverage levels."""
        test_cases = [
            (95, "brightgreen"),
            (85, "green"),
            (75, "yellowgreen"),
            (65, "yellow"),
            (55, "orange"),
            (45, "red"),
        ]

        existing_content = "# Test Project\n\nContent here."

        for percentage, expected_color in test_cases:
            expected_badge = f"![Coverage](https://img.shields.io/badge/coverage-{percentage}%25-{expected_color})"

            with patch("update_coverage_badge.Path") as mock_path:
                mock_readme = mock_path.return_value
                mock_readme.exists.return_value = True
                mock_readme.read_text.return_value = existing_content

                with patch("builtins.print") as mock_print:
                    update_readme_badge(percentage)

                written_content = mock_readme.write_text.call_args[0][0]
                assert expected_badge in written_content
                mock_print.assert_called_with(
                    f"Updated README.md with coverage badge: {percentage}% ({expected_color})"
                )

    def test_update_readme_badge_complex_existing_badge(self) -> None:
        """Test replacing existing badge with complex README structure."""
        existing_content = """# Complex Project

[![Build Status](https://travis-ci.org/user/repo.svg?branch=main)](https://travis-ci.org/user/repo)
![Coverage](https://img.shields.io/badge/coverage-67%25-yellow)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

This is a complex project.
"""

        expected_content = """# Complex Project

[![Build Status](https://travis-ci.org/user/repo.svg?branch=main)](https://travis-ci.org/user/repo)
![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

This is a complex project.
"""

        with patch("update_coverage_badge.Path") as mock_path:
            mock_readme = mock_path.return_value
            mock_readme.exists.return_value = True
            mock_readme.read_text.return_value = existing_content

            with patch("builtins.print") as mock_print:
                update_readme_badge(91)

            mock_readme.write_text.assert_called_once_with(expected_content)
            mock_print.assert_called_once_with(
                "Updated README.md with coverage badge: 91% (brightgreen)"
            )


class TestMain:
    """Test main function."""

    def test_main_success(self) -> None:
        """Test successful main function execution."""
        with patch(
            "update_coverage_badge.get_coverage_percentage"
        ) as mock_get_coverage:
            with patch(
                "update_coverage_badge.update_readme_badge"
            ) as mock_update_badge:
                mock_get_coverage.return_value = 88

                main()

                mock_get_coverage.assert_called_once()
                mock_update_badge.assert_called_once_with(88)

    def test_main_with_coverage_file_error(self) -> None:
        """Test main function when coverage file is missing."""
        with patch(
            "update_coverage_badge.get_coverage_percentage"
        ) as mock_get_coverage:
            mock_get_coverage.side_effect = SystemExit(1)

            with pytest.raises(SystemExit) as excinfo:
                main()

            assert excinfo.value.code == 1
            mock_get_coverage.assert_called_once()

    def test_main_with_readme_error(self) -> None:
        """Test main function when README file is missing."""
        with patch(
            "update_coverage_badge.get_coverage_percentage"
        ) as mock_get_coverage:
            with patch(
                "update_coverage_badge.update_readme_badge"
            ) as mock_update_badge:
                mock_get_coverage.return_value = 75
                mock_update_badge.side_effect = SystemExit(1)

                with pytest.raises(SystemExit) as excinfo:
                    main()

                assert excinfo.value.code == 1
                mock_get_coverage.assert_called_once()
                mock_update_badge.assert_called_once_with(75)


class TestIntegration:
    """Integration tests."""

    def test_full_workflow_with_temp_files(self, tmp_path: Path) -> None:
        """Test the full workflow with temporary files."""
        # Set up temporary directory
        original_cwd = Path.cwd()

        try:
            # Create coverage.json
            coverage_data = {"totals": {"percent_covered": 87.3}}
            coverage_file = tmp_path / "coverage.json"
            coverage_file.write_text(json.dumps(coverage_data))

            # Create README.md
            readme_content = """# Test Project

Some description here.

## Installation

Run `pip install`.
"""
            readme_file = tmp_path / "README.md"
            readme_file.write_text(readme_content)

            # Change to temp directory
            import os

            os.chdir(tmp_path)

            # Run the main function
            main()

            # Check results
            updated_readme = readme_file.read_text()
            assert (
                "![Coverage](https://img.shields.io/badge/coverage-87%25-green)"
                in updated_readme
            )
            assert "# Test Project" in updated_readme
            assert "Some description here." in updated_readme

        finally:
            # Restore original directory
            import os

            os.chdir(original_cwd)

    def test_edge_case_empty_readme(self, tmp_path: Path) -> None:
        """Test edge case with empty README."""
        # Set up temporary directory
        original_cwd = Path.cwd()

        try:
            # Create coverage.json
            coverage_data = {"totals": {"percent_covered": 100.0}}
            coverage_file = tmp_path / "coverage.json"
            coverage_file.write_text(json.dumps(coverage_data))

            # Create empty README.md
            readme_file = tmp_path / "README.md"
            readme_file.write_text("")

            # Change to temp directory
            import os

            os.chdir(tmp_path)

            # Run the main function
            main()

            # Check results - badge should not be added to empty file
            updated_readme = readme_file.read_text()
            assert updated_readme == ""  # Should remain empty

        finally:
            # Restore original directory
            import os

            os.chdir(original_cwd)
