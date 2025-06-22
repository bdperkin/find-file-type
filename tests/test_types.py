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

"""Tests for the types module."""

from pathlib import Path

from fft.types import DetectionMethod, DetectionResult, FileType

# import pytest  # Used by test runner


class TestDetectionMethodEnum:
    """Test cases for the DetectionMethod enum."""

    def test_test_type_values(self) -> None:
        """Test that DetectionMethod enum has correct values."""
        assert DetectionMethod.FILESYSTEM.value == "filesystem"
        assert DetectionMethod.MAGIC.value == "magic"
        assert DetectionMethod.LANGUAGE.value == "language"

    def test_test_type_enum_members(self) -> None:
        """Test that DetectionMethod enum has all expected members."""
        expected_members = {"FILESYSTEM", "MAGIC", "LANGUAGE"}
        actual_members = {member.name for member in DetectionMethod}
        assert actual_members == expected_members

    def test_test_type_string_representation(self) -> None:
        """Test string representation of DetectionMethod enum members."""
        assert str(DetectionMethod.FILESYSTEM) == "DetectionMethod.FILESYSTEM"
        assert str(DetectionMethod.MAGIC) == "DetectionMethod.MAGIC"
        assert str(DetectionMethod.LANGUAGE) == "DetectionMethod.LANGUAGE"

    def test_test_type_equality(self) -> None:
        """Test equality comparison of DetectionMethod enum members."""
        assert DetectionMethod.FILESYSTEM == DetectionMethod.FILESYSTEM
        assert DetectionMethod.FILESYSTEM != DetectionMethod.MAGIC
        assert DetectionMethod.FILESYSTEM != DetectionMethod.LANGUAGE

    def test_test_type_iteration(self) -> None:
        """Test iterating over DetectionMethod enum."""
        test_types = list(DetectionMethod)
        assert len(test_types) == 3
        assert DetectionMethod.FILESYSTEM in test_types
        assert DetectionMethod.MAGIC in test_types
        assert DetectionMethod.LANGUAGE in test_types


class TestFileTypeEnum:
    """Test cases for the FileType enum."""

    def test_programming_language_file_types(self) -> None:
        """Test programming language file type values."""
        assert FileType.PYTHON.value == "Python source"
        assert FileType.JAVASCRIPT.value == "JavaScript source"
        assert FileType.TYPESCRIPT.value == "TypeScript source"
        assert FileType.JAVA.value == "Java source"
        assert FileType.C.value == "C source"
        assert FileType.CPP.value == "C++ source"
        assert FileType.RUST.value == "Rust source"
        assert FileType.GO.value == "Go source"
        assert FileType.PHP.value == "PHP source"
        assert FileType.RUBY.value == "Ruby source"
        assert FileType.SHELL.value == "Shell script"
        assert FileType.POWERSHELL.value == "PowerShell script"
        assert FileType.BATCH.value == "Batch file"

    def test_web_technology_file_types(self) -> None:
        """Test web technology file type values."""
        assert FileType.HTML.value == "HTML document"
        assert FileType.CSS.value == "CSS stylesheet"
        assert FileType.XML.value == "XML document"
        assert FileType.JSON.value == "JSON data"
        assert FileType.YAML.value == "YAML data"

    def test_document_file_types(self) -> None:
        """Test document file type values."""
        assert FileType.PDF.value == "PDF document"
        assert FileType.WORD.value == "Microsoft Word document"
        assert FileType.EXCEL.value == "Microsoft Excel spreadsheet"
        assert FileType.POWERPOINT.value == "Microsoft PowerPoint presentation"
        assert FileType.TEXT.value == "Text file"
        assert FileType.MARKDOWN.value == "Markdown document"

    def test_image_file_types(self) -> None:
        """Test image file type values."""
        assert FileType.JPEG.value == "JPEG image"
        assert FileType.PNG.value == "PNG image"
        assert FileType.GIF.value == "GIF image"
        assert FileType.SVG.value == "SVG image"
        assert FileType.TIFF.value == "TIFF image"
        assert FileType.BMP.value == "BMP image"
        assert FileType.WEBP.value == "WebP image"

    def test_audio_video_file_types(self) -> None:
        """Test audio/video file type values."""
        assert FileType.MP3.value == "MP3 audio"
        assert FileType.MP4.value == "MP4 video"
        assert FileType.AVI.value == "AVI video"
        assert FileType.WAV.value == "WAV audio"
        assert FileType.FLAC.value == "FLAC audio"

    def test_archive_file_types(self) -> None:
        """Test archive file type values."""
        assert FileType.ZIP.value == "ZIP archive"
        assert FileType.TAR.value == "TAR archive"
        assert FileType.GZIP.value == "GZIP archive"
        assert FileType.RAR.value == "RAR archive"
        assert FileType.SEVEN_ZIP.value == "7-Zip archive"

    def test_executable_file_types(self) -> None:
        """Test executable file type values."""
        assert FileType.ELF.value == "ELF executable"
        assert FileType.PE.value == "PE executable"
        assert FileType.MACH_O.value == "Mach-O executable"

    def test_data_format_file_types(self) -> None:
        """Test data format file type values."""
        assert FileType.CSV.value == "CSV data"
        assert FileType.TSV.value == "TSV data"
        assert FileType.LOG.value == "Log file"
        assert FileType.CONFIG.value == "Configuration file"

    def test_special_file_types(self) -> None:
        """Test special file type values."""
        assert FileType.BINARY.value == "Binary file"
        assert FileType.EMPTY.value == "Empty file"
        assert FileType.SYMLINK.value == "Symbolic link"
        assert FileType.DIRECTORY.value == "Directory"
        assert FileType.UNKNOWN.value == "Unknown file type"

    def test_file_type_enum_completeness(self) -> None:
        """Test that FileType enum contains expected number of members."""
        # Count all the file types to ensure none are missing
        programming_langs = 13  # PYTHON through BATCH
        web_tech = 5  # HTML through YAML
        documents = 6  # PDF through MARKDOWN
        images = 7  # JPEG through WEBP
        audio_video = 5  # MP3 through FLAC
        archives = 5  # ZIP through SEVEN_ZIP
        executables = 3  # ELF through MACH_O
        data_formats = 4  # CSV through CONFIG
        special = 5  # BINARY through UNKNOWN

        expected_total = (
            programming_langs
            + web_tech
            + documents
            + images
            + audio_video
            + archives
            + executables
            + data_formats
            + special
        )

        actual_total = len(list(FileType))
        assert actual_total == expected_total

    def test_file_type_string_representation(self) -> None:
        """Test string representation of FileType enum members."""
        assert str(FileType.PYTHON) == "FileType.PYTHON"
        assert str(FileType.JAVASCRIPT) == "FileType.JAVASCRIPT"
        assert str(FileType.UNKNOWN) == "FileType.UNKNOWN"

    def test_file_type_equality(self) -> None:
        """Test equality comparison of FileType enum members."""
        assert FileType.PYTHON == FileType.PYTHON
        assert FileType.PYTHON != FileType.JAVASCRIPT
        assert FileType.PYTHON != FileType.UNKNOWN

    def test_file_type_unique_values(self) -> None:
        """Test that all FileType enum values are unique."""
        values = [file_type.value for file_type in FileType]
        assert len(values) == len(set(values))  # No duplicates

    def test_file_type_categories(self) -> None:
        """Test that we can categorize file types."""
        programming_types = {
            FileType.PYTHON,
            FileType.JAVASCRIPT,
            FileType.JAVA,
            FileType.C,
            FileType.CPP,
            FileType.RUST,
            FileType.GO,
        }

        for file_type in programming_types:
            assert "source" in file_type.value or "script" in file_type.value

        image_types = {
            FileType.JPEG,
            FileType.PNG,
            FileType.GIF,
            FileType.SVG,
            FileType.TIFF,
            FileType.BMP,
            FileType.WEBP,
        }

        for file_type in image_types:
            assert "image" in file_type.value


class TestDetectionResult:
    """Test cases for the DetectionResult dataclass."""

    def test_detection_result_creation(self) -> None:
        """Test creating a DetectionResult instance."""
        file_path = Path("test.py")
        result = DetectionResult(
            file_path=file_path,
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.9,
        )

        assert result.file_path == file_path
        assert result.file_type == FileType.PYTHON
        assert result.test_type == DetectionMethod.FILESYSTEM
        assert result.confidence == 0.9
        assert result.details is None

    def test_detection_result_with_details(self) -> None:
        """Test creating a DetectionResult with details."""
        file_path = Path("test.py")
        result = DetectionResult(
            file_path=file_path,
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.8,
            details="Extension: .py",
        )

        assert result.file_path == file_path
        assert result.file_type == FileType.PYTHON
        assert result.test_type == DetectionMethod.FILESYSTEM
        assert result.confidence == 0.8
        assert result.details == "Extension: .py"

    def test_detection_result_str_without_details(self) -> None:
        """Test string representation without details."""
        result = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.9,
        )

        expected = "test.py: Python source"
        assert str(result) == expected

    def test_detection_result_str_with_details(self) -> None:
        """Test string representation with details."""
        result = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.8,
            details="Extension: .py",
        )

        expected = "test.py: Python source (Extension: .py)"
        assert str(result) == expected

    def test_detection_result_str_with_empty_details(self) -> None:
        """Test string representation with empty details."""
        result = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.8,
            details="",
        )

        # Empty string is falsy, so should not show details
        expected = "test.py: Python source"
        assert str(result) == expected

    def test_detection_result_equality(self) -> None:
        """Test equality comparison of DetectionResult instances."""
        result1 = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.9,
        )

        result2 = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.9,
        )

        result3 = DetectionResult(
            file_path=Path("test.js"),
            file_type=FileType.JAVASCRIPT,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.9,
        )

        assert result1 == result2
        assert result1 != result3

    def test_detection_result_dataclass_fields(self) -> None:
        """Test that DetectionResult has the expected dataclass fields."""
        result = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.9,
            details="test details",
        )

        # Test that we can access all fields
        assert hasattr(result, "file_path")
        assert hasattr(result, "file_type")
        assert hasattr(result, "test_type")
        assert hasattr(result, "confidence")
        assert hasattr(result, "details")

    def test_detection_result_confidence_range(self) -> None:
        """Test DetectionResult with various confidence values."""
        # Test boundary values
        for confidence in [0.0, 0.1, 0.5, 0.9, 1.0]:
            result = DetectionResult(
                file_path=Path("test.py"),
                file_type=FileType.PYTHON,
                test_type=DetectionMethod.FILESYSTEM,
                confidence=confidence,
            )
            assert result.confidence == confidence

    def test_detection_result_with_different_file_types(self) -> None:
        """Test DetectionResult with various file types."""
        test_cases = [
            (FileType.PYTHON, "Python source"),
            (FileType.JAVASCRIPT, "JavaScript source"),
            (FileType.JSON, "JSON data"),
            (FileType.BINARY, "Binary file"),
            (FileType.DIRECTORY, "Directory"),
            (FileType.UNKNOWN, "Unknown file type"),
        ]

        for file_type, expected_value in test_cases:
            result = DetectionResult(
                file_path=Path("test"),
                file_type=file_type,
                test_type=DetectionMethod.FILESYSTEM,
                confidence=0.8,
            )
            assert result.file_type == file_type
            assert file_type.value == expected_value

    def test_detection_result_with_different_test_types(self) -> None:
        """Test DetectionResult with different test types."""
        test_types = [
            DetectionMethod.FILESYSTEM,
            DetectionMethod.MAGIC,
            DetectionMethod.LANGUAGE,
        ]

        for test_type in test_types:
            result = DetectionResult(
                file_path=Path("test.py"),
                file_type=FileType.PYTHON,
                test_type=test_type,
                confidence=0.8,
            )
            assert result.test_type == test_type

    def test_detection_result_with_complex_path(self) -> None:
        """Test DetectionResult with complex file paths."""
        complex_paths = [
            Path("simple.py"),
            Path("path/to/file.js"),
            Path("/absolute/path/to/file.json"),
            Path("../relative/path/file.txt"),
            Path("file.with.multiple.dots.py"),
            Path("no_extension"),
        ]

        for path in complex_paths:
            result = DetectionResult(
                file_path=path,
                file_type=FileType.PYTHON,
                test_type=DetectionMethod.FILESYSTEM,
                confidence=0.8,
            )
            assert result.file_path == path
            assert str(result).startswith(str(path))

    def test_detection_result_repr(self) -> None:
        """Test repr representation of DetectionResult."""
        result = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.8,
            details="Extension: .py",
        )

        # Should be a valid Python expression
        repr_str = repr(result)
        assert "DetectionResult" in repr_str
        assert "file_path" in repr_str
        assert "file_type" in repr_str
        assert "test_type" in repr_str
        assert "confidence" in repr_str


class TestTypesIntegration:
    """Integration tests for types working together."""

    def test_all_test_types_with_all_file_types(self) -> None:
        """Test that any DetectionMethod can be used with any FileType."""
        # This tests that our type system is consistent
        for test_type in DetectionMethod:
            for file_type in FileType:
                result = DetectionResult(
                    file_path=Path("test"),
                    file_type=file_type,
                    test_type=test_type,
                    confidence=0.5,
                )
                # Should be able to create any combination
                assert result.test_type == test_type
                assert result.file_type == file_type

    def test_realistic_detection_scenarios(self) -> None:
        """Test realistic file detection scenarios."""
        scenarios = [
            # Filesystem detection scenarios
            (
                Path("script.py"),
                FileType.PYTHON,
                DetectionMethod.FILESYSTEM,
                0.8,
                "Extension: .py",
            ),
            (
                Path("app.js"),
                FileType.JAVASCRIPT,
                DetectionMethod.FILESYSTEM,
                0.8,
                "Extension: .js",
            ),
            (
                Path("data.json"),
                FileType.JSON,
                DetectionMethod.FILESYSTEM,
                0.8,
                "Extension: .json",
            ),
            # Magic detection scenarios
            (
                Path("image"),
                FileType.PNG,
                DetectionMethod.MAGIC,
                0.9,
                "Magic: PNG image data",
            ),
            (
                Path("archive"),
                FileType.ZIP,
                DetectionMethod.MAGIC,
                0.9,
                "Magic: Zip archive data",
            ),
            # Language detection scenarios
            (
                Path("script"),
                FileType.PYTHON,
                DetectionMethod.LANGUAGE,
                0.7,
                "Shebang: #!/usr/bin/python3",
            ),
            (
                Path("program"),
                FileType.SHELL,
                DetectionMethod.LANGUAGE,
                0.8,
                "Language patterns: 3 matches",
            ),
            # Special cases
            (
                Path("unknown_file"),
                FileType.UNKNOWN,
                DetectionMethod.FILESYSTEM,
                0.1,
                None,
            ),
            (Path("empty_file"), FileType.EMPTY, DetectionMethod.FILESYSTEM, 1.0, None),
            (
                Path("binary_data"),
                FileType.BINARY,
                DetectionMethod.LANGUAGE,
                0.9,
                "Binary content detected",
            ),
        ]

        for file_path, file_type, test_type, confidence, details in scenarios:
            result = DetectionResult(
                file_path=file_path,
                file_type=file_type,
                test_type=test_type,
                confidence=confidence,
                details=details,
            )

            # Verify the result makes sense
            assert result.file_path == file_path
            assert result.file_type == file_type
            assert result.test_type == test_type
            assert result.confidence == confidence
            assert result.details == details

            # Verify string representation
            str_repr = str(result)
            assert str(file_path) in str_repr
            assert file_type.value in str_repr
            if details:
                assert details in str_repr

    def test_enum_membership(self) -> None:
        """Test that enum values are proper members."""
        # Test that we can check membership
        assert FileType.PYTHON in FileType
        assert DetectionMethod.FILESYSTEM in DetectionMethod

        # Test that enum names work
        file_types_by_name = [member.name for member in FileType]
        assert "PYTHON" in file_types_by_name
        assert "JAVASCRIPT" in file_types_by_name

        test_types_by_name = [member.name for member in DetectionMethod]
        assert "FILESYSTEM" in test_types_by_name
        assert "MAGIC" in test_types_by_name

    def test_enum_iteration_order(self) -> None:
        """Test that enum iteration is consistent."""
        # Test that iteration order is deterministic
        file_types_1 = list(FileType)
        file_types_2 = list(FileType)
        assert file_types_1 == file_types_2

        test_types_1 = list(DetectionMethod)
        test_types_2 = list(DetectionMethod)
        assert test_types_1 == test_types_2

    def test_enum_hashability(self) -> None:
        """Test that enum members are hashable and can be used in sets/dicts."""
        # FileType enum members should be hashable
        file_type_set = {FileType.PYTHON, FileType.JAVASCRIPT, FileType.PYTHON}
        assert len(file_type_set) == 2  # PYTHON should only appear once

        file_type_dict = {FileType.PYTHON: "py", FileType.JAVASCRIPT: "js"}
        assert file_type_dict[FileType.PYTHON] == "py"
        assert file_type_dict[FileType.JAVASCRIPT] == "js"

        # DetectionMethod enum members should be hashable
        test_type_set = {
            DetectionMethod.FILESYSTEM,
            DetectionMethod.MAGIC,
            DetectionMethod.FILESYSTEM,
        }
        assert len(test_type_set) == 2  # FILESYSTEM should only appear once

        test_type_dict = {
            DetectionMethod.FILESYSTEM: 1,
            DetectionMethod.MAGIC: 2,
            DetectionMethod.LANGUAGE: 3,
        }
        assert test_type_dict[DetectionMethod.FILESYSTEM] == 1
        assert test_type_dict[DetectionMethod.MAGIC] == 2
        assert test_type_dict[DetectionMethod.LANGUAGE] == 3

    def test_detection_result_immutability(self) -> None:
        """Test that DetectionResult behaves as expected with dataclass."""
        result = DetectionResult(
            file_path=Path("test.py"),
            file_type=FileType.PYTHON,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.8,
            details="Extension: .py",
        )

        # Should be able to modify mutable fields
        result.confidence = 0.9
        assert result.confidence == 0.9

        # Should be able to modify details
        result.details = "New details"
        assert result.details == "New details"

        # Should be able to replace enum fields
        result.file_type = FileType.JAVASCRIPT
        assert result.file_type == FileType.JAVASCRIPT

        result.test_type = DetectionMethod.MAGIC
        assert result.test_type == DetectionMethod.MAGIC
