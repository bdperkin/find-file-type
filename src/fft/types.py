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

"""Type definitions for the fft file type detector."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class DetectionMethod(Enum):
    """Types of file detection tests."""

    FILESYSTEM = "filesystem"
    MAGIC = "magic"
    LANGUAGE = "language"


class FileType(Enum):
    """Common file types that can be detected."""

    # Programming languages
    PYTHON = "Python source"
    JAVASCRIPT = "JavaScript source"
    TYPESCRIPT = "TypeScript source"
    JAVA = "Java source"
    C = "C source"
    CPP = "C++ source"
    RUST = "Rust source"
    GO = "Go source"
    PHP = "PHP source"
    RUBY = "Ruby source"
    SHELL = "Shell script"
    POWERSHELL = "PowerShell script"
    BATCH = "Batch file"

    # Web technologies
    HTML = "HTML document"
    CSS = "CSS stylesheet"
    XML = "XML document"
    JSON = "JSON data"
    YAML = "YAML data"

    # Documents
    PDF = "PDF document"
    WORD = "Microsoft Word document"
    EXCEL = "Microsoft Excel spreadsheet"
    POWERPOINT = "Microsoft PowerPoint presentation"
    TEXT = "Text file"
    MARKDOWN = "Markdown document"

    # Images
    JPEG = "JPEG image"
    PNG = "PNG image"
    GIF = "GIF image"
    SVG = "SVG image"
    TIFF = "TIFF image"
    BMP = "BMP image"
    WEBP = "WebP image"

    # Audio/Video
    MP3 = "MP3 audio"
    MP4 = "MP4 video"
    AVI = "AVI video"
    WAV = "WAV audio"
    FLAC = "FLAC audio"

    # Archives
    ZIP = "ZIP archive"
    TAR = "TAR archive"
    GZIP = "GZIP archive"
    RAR = "RAR archive"
    SEVEN_ZIP = "7-Zip archive"

    # Executables
    ELF = "ELF executable"
    PE = "PE executable"
    MACH_O = "Mach-O executable"

    # Data formats
    CSV = "CSV data"
    TSV = "TSV data"
    LOG = "Log file"
    CONFIG = "Configuration file"

    # Special types
    BINARY = "Binary file"
    EMPTY = "Empty file"
    SYMLINK = "Symbolic link"
    DIRECTORY = "Directory"
    UNKNOWN = "Unknown file type"


@dataclass
class DetectionResult:
    """Result of file type detection."""

    file_path: Path
    file_type: FileType
    test_type: DetectionMethod
    confidence: float
    details: Optional[str] = None

    def __str__(self) -> str:
        """Return string representation of the detection result."""
        if self.details:
            return f"{self.file_path}: {self.file_type.value} ({self.details})"
        return f"{self.file_path}: {self.file_type.value}"
