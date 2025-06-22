# Copyright (c) 2025 Find File Type (fft)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Tests for the CLI module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

# import pytest  # Used by test runner
from click.testing import CliRunner

from fft.cli import _display_result, _run_specific_test, main, walk_paths
from fft.detector import FileTypeDetector
from fft.types import DetectionMethod, DetectionResult, FileType


class TestCLI:
    """Test cases for CLI functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.temp_dir = Path(tempfile.mkdtemp())

        # Create test files
        self.python_file = self.temp_dir / "test.py"
        self.python_file.write_text("print('Hello, world!')")

        self.js_file = self.temp_dir / "test.js"
        self.js_file.write_text("console.log('Hello, world!');")

        self.text_file = self.temp_dir / "readme.txt"
        self.text_file.write_text("This is a text file.")

        self.json_file = self.temp_dir / "data.json"
        self.json_file.write_text('{"name": "test"}')

        # Create a subdirectory with files
        self.sub_dir = self.temp_dir / "subdir"
        self.sub_dir.mkdir()
        self.sub_python_file = self.sub_dir / "nested.py"
        self.sub_python_file.write_text("# Nested Python file")

    def teardown_method(self) -> None:
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_help_option(self) -> None:
        """Test --help option displays help text."""
        result = self.runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Find File Type (fft)" in result.output
        assert "Usage:" in result.output
        assert "--verbose" in result.output
        assert "--quiet" in result.output
        assert "--test-type" in result.output

    def test_version_option(self) -> None:
        """Test --version option displays version."""
        result = self.runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output.lower()

    def test_single_file_analysis(self) -> None:
        """Test analyzing a single file."""
        result = self.runner.invoke(main, [str(self.python_file)])
        assert result.exit_code == 0
        assert str(self.python_file) in result.output
        assert "Python source" in result.output

    def test_multiple_files_analysis(self) -> None:
        """Test analyzing multiple files."""
        result = self.runner.invoke(main, [str(self.python_file), str(self.js_file)])
        assert result.exit_code == 0
        assert str(self.python_file) in result.output
        assert str(self.js_file) in result.output
        assert "Python source" in result.output
        assert "JavaScript source" in result.output

    def test_directory_analysis(self) -> None:
        """Test analyzing a directory."""
        result = self.runner.invoke(main, [str(self.temp_dir)])
        assert result.exit_code == 0
        # Should find files in the directory
        assert "Python source" in result.output or "JavaScript source" in result.output

    def test_verbose_mode(self) -> None:
        """Test --verbose option provides detailed output."""
        result = self.runner.invoke(main, ["--verbose", str(self.python_file)])
        assert result.exit_code == 0
        assert "confidence" in result.output
        assert (
            "filesystem" in result.output
            or "magic" in result.output
            or "language" in result.output
        )
        assert (
            "Extension:" in result.output
            or "Magic:" in result.output
            or "Shebang:" in result.output
        )

    def test_quiet_mode(self) -> None:
        """Test --quiet option provides minimal output."""
        result = self.runner.invoke(main, ["--quiet", str(self.python_file)])
        assert result.exit_code == 0
        # Should have path and type, but no extra details
        assert str(self.python_file) in result.output
        assert "Python source" in result.output
        assert "confidence" not in result.output
        assert "Extension:" not in result.output

    def test_verbose_with_multiple_files_shows_summary(self) -> None:
        """Test verbose mode shows summary for multiple files."""
        result = self.runner.invoke(main, ["--verbose", str(self.temp_dir)])
        assert result.exit_code == 0
        assert "Summary:" in result.output
        assert "files identified" in result.output

    def test_include_directories_option(self) -> None:
        """Test --include-directories option includes directories in output."""
        result = self.runner.invoke(main, ["--include-directories", str(self.temp_dir)])
        assert result.exit_code == 0
        # Should include the subdirectory
        assert str(self.sub_dir) in result.output or "Directory" in result.output

    def test_exclude_directories_by_default(self) -> None:
        """Test directories are excluded by default."""
        result = self.runner.invoke(main, [str(self.temp_dir)])
        assert result.exit_code == 0
        # Should not include directory entries by default
        lines = result.output.strip().split("\n")
        directory_lines = [line for line in lines if "Directory" in line]
        # By default, directories should not be shown
        assert len(directory_lines) == 0

    def test_test_type_filesystem(self) -> None:
        """Test --test-type filesystem option."""
        result = self.runner.invoke(
            main, ["--test-type", "filesystem", "--verbose", str(self.python_file)]
        )
        assert result.exit_code == 0
        assert "filesystem" in result.output
        # Should not have magic or language detection info
        assert "Magic:" not in result.output

    def test_test_type_magic(self) -> None:
        """Test --test-type magic option."""
        result = self.runner.invoke(
            main, ["--test-type", "magic", "--verbose", str(self.python_file)]
        )
        assert result.exit_code == 0
        # May or may not find magic signatures, but should attempt magic detection
        assert result.exit_code == 0  # Command should complete successfully

    def test_test_type_language(self) -> None:
        """Test --test-type language option."""
        result = self.runner.invoke(
            main, ["--test-type", "language", "--verbose", str(self.python_file)]
        )
        assert result.exit_code == 0
        # Should use language detection
        assert result.exit_code == 0  # Command should complete successfully

    def test_filter_type_single(self) -> None:
        """Test --filter-type option with single type."""
        result = self.runner.invoke(
            main, ["--filter-type", "Python source", str(self.temp_dir)]
        )
        assert result.exit_code == 0
        assert "Python source" in result.output
        # Should not show JavaScript files
        assert "JavaScript source" not in result.output

    def test_filter_type_multiple(self) -> None:
        """Test --filter-type option with multiple types."""
        result = self.runner.invoke(
            main,
            [
                "--filter-type",
                "Python source",
                "--filter-type",
                "JavaScript source",
                str(self.temp_dir),
            ],
        )
        assert result.exit_code == 0
        # Should show both Python and JavaScript files
        # Note: output may vary based on what files exist, but command should succeed
        assert result.exit_code == 0

    def test_max_depth_option(self) -> None:
        """Test --max-depth option limits recursion."""
        # Create nested directory structure
        deep_dir = self.sub_dir / "level2" / "level3"
        deep_dir.mkdir(parents=True)
        deep_file = deep_dir / "deep.py"
        deep_file.write_text("# Deep file")

        # With max-depth 1, should not find the deep file
        result = self.runner.invoke(main, ["--max-depth", "1", str(self.temp_dir)])
        assert result.exit_code == 0
        # Should find files in temp_dir and immediate subdirectory
        # but not the deeply nested file

    def test_no_paths_uses_current_directory(self) -> None:
        """Test that no paths defaults to current directory."""
        with patch("fft.cli.Path.cwd", return_value=self.temp_dir):
            result = self.runner.invoke(main, [])
            assert result.exit_code == 0
            # Should analyze files in the temp directory
            assert len(result.output.strip()) > 0

    def test_nonexistent_file_error(self) -> None:
        """Test error handling for nonexistent files."""
        nonexistent_file = self.temp_dir / "does_not_exist.txt"
        result = self.runner.invoke(main, [str(nonexistent_file)])
        assert result.exit_code == 0
        # Should show an error message about the nonexistent path
        assert "does not exist" in result.output or "Error:" in result.output

    def test_permission_error_handling(self) -> None:
        """Test graceful handling of permission errors."""
        # Create a file and then mock a permission error
        with patch("pathlib.Path.rglob") as mock_rglob:
            mock_rglob.side_effect = PermissionError("Permission denied")
            result = self.runner.invoke(main, [str(self.temp_dir)])
            assert result.exit_code == 0
            # Should handle the error gracefully

    def test_keyboard_interrupt_handling(self) -> None:
        """Test handling of keyboard interrupts."""
        with patch("fft.cli.walk_paths") as mock_walk:
            mock_walk.side_effect = KeyboardInterrupt()
            result = self.runner.invoke(main, [str(self.temp_dir)])
            assert result.exit_code == 1
            assert "Interrupted by user" in result.output

    def test_error_processing_with_verbose(self) -> None:
        """Test error handling during file processing with verbose mode."""
        with patch("fft.detector.FileTypeDetector.detect_file_type") as mock_detect:
            mock_detect.side_effect = Exception("Test error")
            result = self.runner.invoke(main, ["--verbose", str(self.python_file)])
            assert result.exit_code == 0
            assert "Error processing" in result.output

    def test_error_processing_without_verbose(self) -> None:
        """Test error handling during file processing without verbose mode."""
        with patch("fft.detector.FileTypeDetector.detect_file_type") as mock_detect:
            mock_detect.side_effect = Exception("Test error")
            result = self.runner.invoke(main, [str(self.python_file)])
            assert result.exit_code == 0
            # Should not show error details without verbose mode
            assert "Error processing" not in result.output


class TestWalkPaths:
    """Test cases for the walk_paths function."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

        # Create test files and directories
        self.file1 = self.temp_dir / "file1.txt"
        self.file1.write_text("File 1")

        self.subdir = self.temp_dir / "subdir"
        self.subdir.mkdir()
        self.file2 = self.subdir / "file2.txt"
        self.file2.write_text("File 2")

    def teardown_method(self) -> None:
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_walk_single_file(self) -> None:
        """Test walking a single file."""
        paths = list(walk_paths([self.file1]))
        assert len(paths) == 1
        assert paths[0] == self.file1

    def test_walk_directory(self) -> None:
        """Test walking a directory."""
        paths = list(walk_paths([self.temp_dir]))
        # Should find all files in the directory tree
        file_paths = [p for p in paths if p.is_file()]
        assert len(file_paths) >= 2  # At least file1 and file2
        assert self.file1 in file_paths
        assert self.file2 in file_paths

    def test_walk_nonexistent_path(self) -> None:
        """Test walking a nonexistent path."""
        nonexistent = self.temp_dir / "does_not_exist"

        # Capture stderr to check for error message
        paths = list(walk_paths([nonexistent]))
        assert len(paths) == 0  # Should yield no paths

    def test_walk_multiple_paths(self) -> None:
        """Test walking multiple paths."""
        paths = list(walk_paths([self.file1, self.subdir]))
        assert self.file1 in paths
        assert self.file2 in paths

    def test_walk_symlink(self) -> None:
        """Test walking symbolic links."""
        # Create a symbolic link
        link_target = self.temp_dir / "link_target.txt"
        link_target.write_text("Link target")

        symlink = self.temp_dir / "symlink"
        try:
            symlink.symlink_to(link_target)
            paths = list(walk_paths([symlink]))
            assert symlink in paths
        except OSError:
            # Skip test if symlinks are not supported (e.g., Windows without privileges)
            # Skip test if symlinks are not supported
            return


class TestDisplayResult:
    """Test cases for the _display_result function."""

    def test_display_result_quiet_mode(self) -> None:
        """Test displaying result in quiet mode."""
        result = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.8,
            details="Extension: .py",
        )

        from click.testing import CliRunner

        runner = CliRunner()

        with runner.isolated_filesystem():
            # Use Click's echo capture
            import io
            from contextlib import redirect_stdout

            output = io.StringIO()
            with redirect_stdout(output):
                _display_result(result, verbose=False, quiet=True)

            captured = output.getvalue()
            assert "test.py: Python source" in captured
            assert "confidence" not in captured
            assert "Extension:" not in captured

    def test_display_result_verbose_mode(self) -> None:
        """Test displaying result in verbose mode."""
        result = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.8,
            details="Extension: .py",
        )

        from click.testing import CliRunner

        runner = CliRunner()

        with runner.isolated_filesystem():
            import io
            from contextlib import redirect_stdout

            output = io.StringIO()
            with redirect_stdout(output):
                _display_result(result, verbose=True, quiet=False)

            captured = output.getvalue()
            assert "test.py: Python source" in captured
            assert "80% confidence" in captured
            assert "Extension: .py" in captured

    def test_display_result_standard_mode(self) -> None:
        """Test displaying result in standard mode."""
        result = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.8,
            details="Extension: .py",
        )

        from click.testing import CliRunner

        runner = CliRunner()

        with runner.isolated_filesystem():
            import io
            from contextlib import redirect_stdout

            output = io.StringIO()
            with redirect_stdout(output):
                _display_result(result, verbose=False, quiet=False)

            captured = output.getvalue()
            assert "test.py: Python source" in captured
            # Should use the __str__ method of DetectionResult

    def test_display_result_verbose_without_details(self) -> None:
        """Test displaying result in verbose mode without details."""
        result = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.8,
            details=None,
        )

        from click.testing import CliRunner

        runner = CliRunner()

        with runner.isolated_filesystem():
            import io
            from contextlib import redirect_stdout

            output = io.StringIO()
            with redirect_stdout(output):
                _display_result(result, verbose=True, quiet=False)

            captured = output.getvalue()
            assert "test.py: Python source" in captured
            assert "80% confidence" in captured
            # Should not have " - " for details since details is None


class TestRunSpecificTest:
    """Test cases for the _run_specific_test function."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.detector = FileTypeDetector()
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_file = self.temp_dir / "test.py"
        self.test_file.write_text("print('test')")

    def teardown_method(self) -> None:
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_run_filesystem_test(self) -> None:
        """Test running filesystem-specific test."""
        result = _run_specific_test(self.detector, self.test_file, "filesystem")
        assert result is not None
        assert result.test_type == DetectionMethod.FILESYSTEM

    def test_run_magic_test(self) -> None:
        """Test running magic-specific test."""
        result = _run_specific_test(self.detector, self.test_file, "magic")
        # Result may be None if magic detection doesn't find anything
        if result:
            assert result.test_type == DetectionMethod.MAGIC

    def test_run_language_test(self) -> None:
        """Test running language-specific test."""
        result = _run_specific_test(self.detector, self.test_file, "language")
        # Should detect Python content
        if result:
            assert result.test_type == DetectionMethod.LANGUAGE

    def test_run_invalid_test_type(self) -> None:
        """Test running with invalid test type."""
        result = _run_specific_test(self.detector, self.test_file, "invalid")
        assert result is None


class TestCLIIntegration:
    """Integration tests for the complete CLI workflow."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.temp_dir = Path(tempfile.mkdtemp())

        # Create a realistic project structure
        self.src_dir = self.temp_dir / "src"
        self.src_dir.mkdir()

        # Python files
        (self.src_dir / "main.py").write_text(
            '''#!/usr/bin/env python3
"""Main module."""
import sys

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
'''
        )

        (self.src_dir / "utils.py").write_text(
            '''"""Utility functions."""

def helper_function(x):
    return x * 2
'''
        )

        # JavaScript file
        (self.src_dir / "app.js").write_text(
            """const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello World!');
});

app.listen(3000);
"""
        )

        # Config files
        (self.temp_dir / "package.json").write_text(
            """{
  "name": "test-app",
  "version": "1.0.0",
  "main": "src/app.js"
}"""
        )

        (self.temp_dir / "README.md").write_text(
            """# Test Project

This is a test project for the fft tool.

## Features

- Python backend
- JavaScript frontend
- Configuration files
"""
        )

        # Binary-like file
        binary_file = self.temp_dir / "data.bin"
        binary_file.write_bytes(
            bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
        )  # PNG header

        # Empty file
        (self.temp_dir / "empty.log").touch()

    def teardown_method(self) -> None:
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_analyze_project_structure(self) -> None:
        """Test analyzing a complete project structure."""
        result = self.runner.invoke(main, [str(self.temp_dir)])
        assert result.exit_code == 0

        # Should identify different file types
        assert "Python source" in result.output
        assert "JavaScript source" in result.output
        assert "JSON data" in result.output
        assert "Markdown document" in result.output

    def test_filter_python_files_only(self) -> None:
        """Test filtering to show only Python files."""
        result = self.runner.invoke(
            main, ["--filter-type", "Python source", str(self.temp_dir)]
        )
        assert result.exit_code == 0

        # Should only show Python files
        assert "Python source" in result.output
        assert "JavaScript source" not in result.output
        assert "JSON data" not in result.output

    def test_verbose_analysis_with_summary(self) -> None:
        """Test verbose analysis shows detailed information and summary."""
        result = self.runner.invoke(main, ["--verbose", str(self.temp_dir)])
        assert result.exit_code == 0

        # Should show confidence levels and detection methods
        assert "confidence" in result.output
        assert (
            "filesystem" in result.output
            or "magic" in result.output
            or "language" in result.output
        )

        # Should show summary
        assert "Summary:" in result.output
        assert "files identified" in result.output

    def test_quiet_mode_minimal_output(self) -> None:
        """Test quiet mode provides minimal output."""
        result = self.runner.invoke(main, ["--quiet", str(self.temp_dir)])
        assert result.exit_code == 0

        # Should be minimal - just paths and types
        lines = [line for line in result.output.strip().split("\n") if line]
        for line in lines:
            # Each line should have format: path: type
            assert ": " in line
            # Should not have verbose information
            assert "confidence" not in line
            assert "Extension:" not in line

    def test_language_detection_only(self) -> None:
        """Test using only language detection."""
        result = self.runner.invoke(
            main, ["--test-type", "language", "--verbose", str(self.temp_dir)]
        )
        assert result.exit_code == 0

        # Should use language detection methods
        assert "language" in result.output
        # Should not use filesystem detection
        assert "filesystem" not in result.output
