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

"""Tests for the FileTypeDetector class."""

import tempfile
from pathlib import Path

import pytest

from fft.detector import FileTypeDetector
from fft.types import DetectionMethod, FileType


class TestFileTypeDetector:
    """Test cases for FileTypeDetector."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = FileTypeDetector()
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_python_file_detection(self):
        """Test detection of Python files."""
        # Test extension-based detection
        python_file = self.temp_dir / "test.py"
        python_file.write_text("print('Hello, world!')")

        result = self.detector.detect_file_type(python_file)
        assert result.file_type == FileType.PYTHON
        assert result.test_type == DetectionMethod.FILESYSTEM
        assert result.confidence > 0.5

    def test_javascript_file_detection(self):
        """Test detection of JavaScript files."""
        js_file = self.temp_dir / "test.js"
        js_file.write_text("console.log('Hello, world!');")

        result = self.detector.detect_file_type(js_file)
        assert result.file_type == FileType.JAVASCRIPT
        assert result.test_type == DetectionMethod.FILESYSTEM

    def test_directory_detection(self):
        """Test detection of directories."""
        test_dir = self.temp_dir / "testdir"
        test_dir.mkdir()

        result = self.detector.detect_file_type(test_dir)
        assert result.file_type == FileType.DIRECTORY
        assert result.test_type == DetectionMethod.FILESYSTEM
        assert result.confidence == 1.0

    def test_empty_file_detection(self):
        """Test detection of empty files."""
        empty_file = self.temp_dir / "empty.txt"
        empty_file.touch()

        result = self.detector.detect_file_type(empty_file)
        assert result.file_type == FileType.EMPTY
        assert result.test_type == DetectionMethod.FILESYSTEM
        assert result.confidence == 1.0

    def test_nonexistent_file(self):
        """Test handling of non-existent files."""
        nonexistent = self.temp_dir / "does_not_exist.txt"

        result = self.detector.detect_file_type(nonexistent)
        assert result.file_type == FileType.UNKNOWN
        assert result.details == "File not found"
        assert result.confidence == 1.0

    def test_language_detection_python(self):
        """Test language-based detection for Python without extension."""
        python_content = """#!/usr/bin/env python3
import os
import sys

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
"""
        no_ext_file = self.temp_dir / "python_script"
        no_ext_file.write_text(python_content)

        result = self.detector.detect_file_type(no_ext_file)
        # Should be detected by shebang line
        assert result.file_type == FileType.PYTHON
        assert result.test_type == DetectionMethod.LANGUAGE

    def test_language_detection_javascript(self):
        """Test language-based detection for JavaScript without extension."""
        js_content = """function greet(name) {
    console.log(`Hello, ${name}!`);
}

const message = "Welcome";
let count = 0;

greet("World");
"""
        no_ext_file = self.temp_dir / "js_script"
        no_ext_file.write_text(js_content)

        result = self.detector.detect_file_type(no_ext_file)
        # Should be detected by language patterns
        assert result.file_type == FileType.JAVASCRIPT
        assert result.test_type == DetectionMethod.LANGUAGE

    def test_json_detection(self):
        """Test JSON file detection."""
        json_content = """
{
    "name": "test",
    "version": "1.0.0",
    "description": "A test file",
    "keywords": ["test", "json"]
}
"""
        json_file = self.temp_dir / "test.json"
        json_file.write_text(json_content)

        result = self.detector.detect_file_type(json_file)
        assert result.file_type == FileType.JSON
        # Could be detected by extension or language analysis
        assert result.test_type in [
            DetectionMethod.FILESYSTEM,
            DetectionMethod.LANGUAGE,
        ]

    def test_text_file_detection(self):
        """Test plain text file detection."""
        text_content = """This is a plain text file.
It contains multiple lines of text.
There are no special formatting or syntax elements.
Just regular sentences and paragraphs.
"""
        text_file = self.temp_dir / "readme.txt"
        text_file.write_text(text_content)

        result = self.detector.detect_file_type(text_file)
        assert result.file_type == FileType.TEXT
        assert result.test_type == DetectionMethod.FILESYSTEM

    def test_binary_content_detection(self):
        """Test detection of binary content."""
        # Create a file with binary data
        binary_data = bytes([0x00, 0x01, 0x02, 0x03, 0xFF, 0xFE, 0xFD])
        binary_file = self.temp_dir / "binary_file"
        binary_file.write_bytes(binary_data)

        result = self.detector.detect_file_type(binary_file)
        # Should be detected as binary during language tests
        assert result.file_type == FileType.BINARY
        assert result.test_type == DetectionMethod.LANGUAGE

    def test_shell_script_detection(self):
        """Test shell script detection."""
        shell_content = """#!/bin/bash
echo "This is a shell script"
for i in {1..5}; do
    echo "Count: $i"
done
"""
        shell_file = self.temp_dir / "script.sh"
        shell_file.write_text(shell_content)

        result = self.detector.detect_file_type(shell_file)
        assert result.file_type == FileType.SHELL
        # Could be detected by extension or shebang
        assert result.test_type in [
            DetectionMethod.FILESYSTEM,
            DetectionMethod.LANGUAGE,
        ]

    def test_csv_detection(self):
        """Test CSV file detection."""
        csv_content = """Name,Age,City
John,25,New York
Jane,30,Los Angeles
Bob,35,Chicago
"""
        csv_file = self.temp_dir / "data.csv"
        csv_file.write_text(csv_content)

        result = self.detector.detect_file_type(csv_file)
        assert result.file_type == FileType.CSV
        # Could be detected by extension or language analysis
        assert result.test_type in [
            DetectionMethod.FILESYSTEM,
            DetectionMethod.LANGUAGE,
        ]

    def test_string_path_input(self):
        """Test that string paths are converted to Path objects."""
        python_file = self.temp_dir / "test.py"
        python_file.write_text("print('test')")

        # Pass string path instead of Path object
        result = self.detector.detect_file_type(str(python_file))
        assert result.file_type == FileType.PYTHON
        assert isinstance(result.file_path, Path)

    def test_multiple_extensions(self):
        """Test files with multiple extensions like .tar.gz."""
        # Create a fake compressed tar file
        tar_gz_file = self.temp_dir / "archive.tar.gz"
        tar_gz_file.write_text("fake compressed content")

        result = self.detector.detect_file_type(tar_gz_file)
        assert result.file_type == FileType.GZIP
        assert ".tar.gz" in result.details

    def test_extension_map_completeness(self):
        """Test that the extension map includes common file types."""
        ext_map = self.detector._extension_map

        # Check for common programming languages
        assert ".py" in ext_map
        assert ".js" in ext_map
        assert ".java" in ext_map
        assert ".cpp" in ext_map
        assert ".html" in ext_map
        assert ".css" in ext_map

        # Check for common document types
        assert ".pdf" in ext_map
        assert ".txt" in ext_map
        assert ".md" in ext_map

        # Check for common image types
        assert ".jpg" in ext_map
        assert ".png" in ext_map
        assert ".gif" in ext_map
