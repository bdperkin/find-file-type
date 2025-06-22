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

"""Core file type detection logic."""

import os
import re
import stat
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    import magic

    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

from .types import DetectionMethod, DetectionResult, FileType


class FileTypeDetector:
    """Main file type detector using filesystem, magic, and language tests."""

    def __init__(self) -> None:
        """Initialize the file type detector."""
        self._extension_map = self._build_extension_map()
        self._shebang_map = self._build_shebang_map()
        self._language_patterns = self._build_language_patterns()

        # Initialize magic detector if available
        self._magic = None
        if MAGIC_AVAILABLE:
            try:
                self._magic = magic.Magic(mime=True)
            except Exception:
                # Fallback to basic magic
                try:
                    self._magic = magic.Magic()
                except Exception:
                    self._magic = None

    def detect_file_type(self, file_path: Path) -> DetectionResult:
        """
        Detect file type using the three-stage approach.

        Args:
            file_path: Path to the file to analyze

        Returns:
            DetectionResult with detected file type and metadata
        """
        # Convert to Path object if string
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # Check if path exists
        if not file_path.exists():
            return DetectionResult(
                file_path=file_path,
                file_type=FileType.UNKNOWN,
                test_type=DetectionMethod.FILESYSTEM,
                confidence=1.0,
                details="File not found",
            )

        # Stage 1: Filesystem tests
        result = self._filesystem_tests(file_path)
        if result:
            return result

        # Stage 2: Magic tests
        result = self._magic_tests(file_path)
        if result:
            return result

        # Stage 3: Language tests
        result = self._language_tests(file_path)
        if result:
            return result

        # Final fallback - check if it's a regular file with content
        try:
            if file_path.is_file() and file_path.stat().st_size > 0:
                # Try to read a small sample to see if it's binary
                with open(file_path, "rb") as f:
                    sample = f.read(512)

                # Check for null bytes or high ratio of non-printable characters
                null_bytes = sample.count(0)
                if null_bytes > 0 or self._appears_binary(sample):
                    return DetectionResult(
                        file_path=file_path,
                        file_type=FileType.BINARY,
                        test_type=DetectionMethod.LANGUAGE,
                        confidence=0.8,
                        details="Binary content detected",
                    )
        except OSError:
            pass

        # Default fallback
        return DetectionResult(
            file_path=file_path,
            file_type=FileType.UNKNOWN,
            test_type=DetectionMethod.FILESYSTEM,
            confidence=0.1,
        )

    def _filesystem_tests(self, file_path: Path) -> Optional[DetectionResult]:
        """Perform filesystem-based tests."""
        try:
            file_stat = file_path.stat()
        except OSError:
            return None

        # Check if it's a directory
        if stat.S_ISDIR(file_stat.st_mode):
            return DetectionResult(
                file_path=file_path,
                file_type=FileType.DIRECTORY,
                test_type=DetectionMethod.FILESYSTEM,
                confidence=1.0,
            )

        # Check if it's a symbolic link
        if file_path.is_symlink():
            return DetectionResult(
                file_path=file_path,
                file_type=FileType.SYMLINK,
                test_type=DetectionMethod.FILESYSTEM,
                confidence=1.0,
            )

        # Check if file is empty
        if file_stat.st_size == 0:
            return DetectionResult(
                file_path=file_path,
                file_type=FileType.EMPTY,
                test_type=DetectionMethod.FILESYSTEM,
                confidence=1.0,
            )

        # Check executable permissions (Unix-like systems)
        if hasattr(stat, "S_IXUSR") and file_stat.st_mode & stat.S_IXUSR:
            # Check for common executable file types based on extension
            suffix = file_path.suffix.lower()
            if suffix in {".exe", ".dll", ".so", ".app"}:
                file_type = self._extension_map.get(suffix)
                if file_type:
                    return DetectionResult(
                        file_path=file_path,
                        file_type=file_type,
                        test_type=DetectionMethod.FILESYSTEM,
                        confidence=0.9,
                        details="Executable file",
                    )

        # Multiple extensions first (e.g., .tar.gz) - check before single extensions
        if len(file_path.suffixes) > 1:
            combined_suffix = "".join(file_path.suffixes).lower()
            if combined_suffix in self._extension_map:
                return DetectionResult(
                    file_path=file_path,
                    file_type=self._extension_map[combined_suffix],
                    test_type=DetectionMethod.FILESYSTEM,
                    confidence=0.8,
                    details=f"Extension: {combined_suffix}",
                )

            # Also try combinations of the last two suffixes
            if len(file_path.suffixes) >= 2:
                last_two = "".join(file_path.suffixes[-2:]).lower()
                if last_two in self._extension_map:
                    return DetectionResult(
                        file_path=file_path,
                        file_type=self._extension_map[last_two],
                        test_type=DetectionMethod.FILESYSTEM,
                        confidence=0.8,
                        details=f"Extension: {last_two}",
                    )

        # Single extension-based detection
        suffix = file_path.suffix.lower()
        if suffix in self._extension_map:
            return DetectionResult(
                file_path=file_path,
                file_type=self._extension_map[suffix],
                test_type=DetectionMethod.FILESYSTEM,
                confidence=0.8,
                details=f"Extension: {suffix}",
            )

        return None

    def _magic_tests(self, file_path: Path) -> Optional[DetectionResult]:
        """Perform magic byte tests."""
        if not self._magic:
            return None

        try:
            # Read magic bytes
            magic_result = self._magic.from_file(str(file_path))

            # Map magic results to our file types
            magic_lower = magic_result.lower()

            # Common magic patterns
            magic_mappings = {
                "pdf": FileType.PDF,
                "jpeg": FileType.JPEG,
                "png": FileType.PNG,
                "gif": FileType.GIF,
                "zip": FileType.ZIP,
                "gzip": FileType.GZIP,
                "tar": FileType.TAR,
                "rar": FileType.RAR,
                "elf": FileType.ELF,
                "pe32": FileType.PE,
                "mach-o": FileType.MACH_O,
                "mp3": FileType.MP3,
                "mp4": FileType.MP4,
                "avi": FileType.AVI,
                "wav": FileType.WAV,
                "html": FileType.HTML,
                "xml": FileType.XML,
                "json": FileType.JSON,
            }

            for pattern, file_type in magic_mappings.items():
                if pattern in magic_lower:
                    return DetectionResult(
                        file_path=file_path,
                        file_type=file_type,
                        test_type=DetectionMethod.MAGIC,
                        confidence=0.9,
                        details=f"Magic: {magic_result}",
                    )

            # Check for text vs binary
            if "text" in magic_lower:
                return DetectionResult(
                    file_path=file_path,
                    file_type=FileType.TEXT,
                    test_type=DetectionMethod.MAGIC,
                    confidence=0.6,
                    details=f"Magic: {magic_result}",
                )
            elif any(
                keyword in magic_lower for keyword in ["binary", "data", "executable"]
            ):
                return DetectionResult(
                    file_path=file_path,
                    file_type=FileType.BINARY,
                    test_type=DetectionMethod.MAGIC,
                    confidence=0.7,
                    details=f"Magic: {magic_result}",
                )

        except Exception:
            pass

        return None

    def _language_tests(self, file_path: Path) -> Optional[DetectionResult]:
        """Perform language and content analysis tests."""
        try:
            # Try to read file as text
            content = self._read_file_safely(file_path)
            if content is None:
                return DetectionResult(
                    file_path=file_path,
                    file_type=FileType.BINARY,
                    test_type=DetectionMethod.LANGUAGE,
                    confidence=0.8,
                    details="Non-text content",
                )

            # Check shebang line
            lines = content.split("\n")
            if lines and lines[0].startswith("#!"):
                shebang = lines[0].strip()
                for pattern, file_type in self._shebang_map.items():
                    if pattern in shebang:
                        return DetectionResult(
                            file_path=file_path,
                            file_type=file_type,
                            test_type=DetectionMethod.LANGUAGE,
                            confidence=0.9,
                            details=f"Shebang: {shebang}",
                        )

            # Pattern-based language detection
            for file_type, patterns in self._language_patterns.items():
                score = 0
                matches = []

                for pattern, weight in patterns.items():
                    if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                        score += weight
                        matches.append(pattern)

                if score >= 3:  # Threshold for confident detection
                    return DetectionResult(
                        file_path=file_path,
                        file_type=file_type,
                        test_type=DetectionMethod.LANGUAGE,
                        confidence=min(score / 10.0, 1.0),
                        details=f"Language patterns: {len(matches)} matches",
                    )

            # Generic text file detection
            if self._is_text_content(content):
                # Check for specific text formats
                if content.strip().startswith("{") and content.strip().endswith("}"):
                    try:
                        import json

                        json.loads(content)
                        return DetectionResult(
                            file_path=file_path,
                            file_type=FileType.JSON,
                            test_type=DetectionMethod.LANGUAGE,
                            confidence=0.8,
                            details="Valid JSON structure",
                        )
                    except (json.JSONDecodeError, ImportError):
                        pass

                # Check for YAML
                if re.search(r"^[a-zA-Z_][a-zA-Z0-9_]*:\s*", content, re.MULTILINE):
                    return DetectionResult(
                        file_path=file_path,
                        file_type=FileType.YAML,
                        test_type=DetectionMethod.LANGUAGE,
                        confidence=0.7,
                        details="YAML-like structure",
                    )

                # Check for CSV
                if "," in content and "\n" in content:
                    lines_sample = content.split("\n")[:5]
                    if all("," in line for line in lines_sample if line.strip()):
                        return DetectionResult(
                            file_path=file_path,
                            file_type=FileType.CSV,
                            test_type=DetectionMethod.LANGUAGE,
                            confidence=0.7,
                            details="CSV-like structure",
                        )

                # Default to text
                return DetectionResult(
                    file_path=file_path,
                    file_type=FileType.TEXT,
                    test_type=DetectionMethod.LANGUAGE,
                    confidence=0.6,
                )

        except Exception:
            pass

        return None

    def _read_file_safely(
        self, file_path: Path, max_size: int = 1024 * 1024
    ) -> Optional[str]:
        """Safely read file content, handling encoding and size limits."""
        try:
            # Check file size
            if file_path.stat().st_size > max_size:
                # Read only the beginning for large files
                with open(file_path, "rb") as f:
                    content_bytes = f.read(8192)  # Read first 8KB
            else:
                with open(file_path, "rb") as f:
                    content_bytes = f.read()

            # Try different encodings
            encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
            for encoding in encodings:
                try:
                    return content_bytes.decode(encoding)
                except UnicodeDecodeError:
                    continue

            return None

        except OSError:
            return None

    def _is_text_content(self, content: str) -> bool:
        """Check if content appears to be text."""
        if not content:
            return True

        # Check for high ratio of printable characters
        printable_chars = sum(1 for c in content if c.isprintable() or c.isspace())
        ratio = printable_chars / len(content)

        return ratio > 0.7

    def _appears_binary(self, data: bytes) -> bool:
        """Check if byte data appears to be binary."""
        if not data:
            return False

        # Count printable ASCII characters
        printable_count = 0
        for byte in data:
            if 32 <= byte <= 126 or byte in (
                9,
                10,
                13,
            ):  # printable ASCII + tab, LF, CR
                printable_count += 1

        # If less than 70% printable characters, consider it binary
        ratio = printable_count / len(data)
        return ratio < 0.7

    def _build_extension_map(self) -> Dict[str, FileType]:
        """Build mapping of file extensions to file types."""
        return {
            # Programming languages
            ".py": FileType.PYTHON,
            ".js": FileType.JAVASCRIPT,
            ".ts": FileType.TYPESCRIPT,
            ".java": FileType.JAVA,
            ".c": FileType.C,
            ".cpp": FileType.CPP,
            ".cxx": FileType.CPP,
            ".cc": FileType.CPP,
            ".h": FileType.C,
            ".hpp": FileType.CPP,
            ".rs": FileType.RUST,
            ".go": FileType.GO,
            ".php": FileType.PHP,
            ".rb": FileType.RUBY,
            ".sh": FileType.SHELL,
            ".bash": FileType.SHELL,
            ".zsh": FileType.SHELL,
            ".fish": FileType.SHELL,
            ".ps1": FileType.POWERSHELL,
            ".bat": FileType.BATCH,
            ".cmd": FileType.BATCH,
            # Web technologies
            ".html": FileType.HTML,
            ".htm": FileType.HTML,
            ".css": FileType.CSS,
            ".xml": FileType.XML,
            ".json": FileType.JSON,
            ".yaml": FileType.YAML,
            ".yml": FileType.YAML,
            # Documents
            ".pdf": FileType.PDF,
            ".doc": FileType.WORD,
            ".docx": FileType.WORD,
            ".xls": FileType.EXCEL,
            ".xlsx": FileType.EXCEL,
            ".ppt": FileType.POWERPOINT,
            ".pptx": FileType.POWERPOINT,
            ".txt": FileType.TEXT,
            ".md": FileType.MARKDOWN,
            ".markdown": FileType.MARKDOWN,
            # Images
            ".jpg": FileType.JPEG,
            ".jpeg": FileType.JPEG,
            ".png": FileType.PNG,
            ".gif": FileType.GIF,
            ".svg": FileType.SVG,
            ".tif": FileType.TIFF,
            ".tiff": FileType.TIFF,
            ".bmp": FileType.BMP,
            ".webp": FileType.WEBP,
            # Audio/Video
            ".mp3": FileType.MP3,
            ".mp4": FileType.MP4,
            ".avi": FileType.AVI,
            ".wav": FileType.WAV,
            ".flac": FileType.FLAC,
            # Archives
            ".zip": FileType.ZIP,
            ".tar": FileType.TAR,
            ".gz": FileType.GZIP,
            ".tar.gz": FileType.GZIP,
            ".tgz": FileType.GZIP,
            ".rar": FileType.RAR,
            ".7z": FileType.SEVEN_ZIP,
            # Data formats
            ".csv": FileType.CSV,
            ".tsv": FileType.TSV,
            ".log": FileType.LOG,
            ".conf": FileType.CONFIG,
            ".config": FileType.CONFIG,
            ".ini": FileType.CONFIG,
            ".cfg": FileType.CONFIG,
        }

    def _build_shebang_map(self) -> Dict[str, FileType]:
        """Build mapping of shebang patterns to file types."""
        return {
            "python": FileType.PYTHON,
            "node": FileType.JAVASCRIPT,
            "bash": FileType.SHELL,
            "sh": FileType.SHELL,
            "zsh": FileType.SHELL,
            "fish": FileType.SHELL,
            "php": FileType.PHP,
            "ruby": FileType.RUBY,
            "perl": FileType.TEXT,  # Could add PERL type
        }

    def _build_language_patterns(self) -> Dict[FileType, Dict[str, int]]:
        """Build language detection patterns with weights."""
        return {
            FileType.PYTHON: {
                r"^\s*import\s+\w+": 3,
                r"^\s*from\s+\w+\s+import": 3,
                r"^\s*def\s+\w+\s*\(": 3,
                r"^\s*class\s+\w+": 3,
                r'if\s+__name__\s*==\s*["\']__main__["\']': 5,
                r"^\s*@\w+": 2,  # decorators
                r"print\s*\(": 2,
            },
            FileType.JAVASCRIPT: {
                r"^\s*function\s+\w+\s*\(": 3,
                r"^\s*var\s+\w+\s*=": 2,
                r"^\s*let\s+\w+\s*=": 2,
                r"^\s*const\s+\w+\s*=": 2,
                r"console\.log\s*\(": 3,
                r'require\s*\(["\']': 3,
                r"module\.exports\s*=": 3,
                r"=>": 2,  # arrow functions
            },
            FileType.JAVA: {
                r"^\s*public\s+class\s+\w+": 5,
                r"^\s*import\s+java\.": 3,
                r"^\s*package\s+\w+": 3,
                r"public\s+static\s+void\s+main": 5,
                r"System\.out\.print": 3,
                r"^\s*@Override": 2,
            },
            FileType.C: {
                r"#include\s*<[^>]+>": 3,
                r'#include\s*"[^"]+"': 3,
                r"^\s*int\s+main\s*\(": 4,
                r"printf\s*\(": 3,
                r"malloc\s*\(": 2,
                r"free\s*\(": 2,
            },
            FileType.CPP: {
                r"#include\s*<[^>]+>": 3,
                r"using\s+namespace\s+std": 4,
                r"std::": 3,
                r"cout\s*<<": 3,
                r"cin\s*>>": 3,
                r"^\s*class\s+\w+": 3,
            },
            FileType.HTML: {
                r"<!DOCTYPE\s+html>": 5,
                r"<html[^>]*>": 4,
                r"<head[^>]*>": 3,
                r"<body[^>]*>": 3,
                r"<div[^>]*>": 2,
                r"<p[^>]*>": 2,
            },
            FileType.CSS: {
                r"[^{]+\{[^}]+\}": 4,
                r"@media\s": 3,
                r"@import\s": 3,
                r"color\s*:\s*[^;]+;": 2,
                r"background\s*:\s*[^;]+;": 2,
            },
        }
