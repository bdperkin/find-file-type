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

"""Command line interface for the fft (Find File Type) tool."""

import sys
from pathlib import Path
from typing import Generator, List

import click

from . import __version__
from .detector import FileTypeDetector
from .types import DetectionResult, FileType


def walk_paths(paths: List[Path]) -> Generator[Path, None, None]:
    """
    Walk through paths, yielding individual files.

    Args:
        paths: List of file or directory paths

    Yields:
        Individual file paths
    """
    for path in paths:
        if not path.exists():
            click.echo(f"Error: Path '{path}' does not exist", err=True)
            continue

        if path.is_file():
            yield path
        elif path.is_dir():
            try:
                # Recursively walk directory
                for file_path in path.rglob("*"):
                    if file_path.is_file():
                        yield file_path
            except PermissionError:
                click.echo(f"Error: Permission denied accessing '{path}'", err=True)
        else:
            # Handle special files (symlinks, etc.)
            yield path


@click.command()
@click.version_option(version=__version__, prog_name="fft")
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed information about the detection process.",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Only show file paths and types, no additional information.",
)
@click.option(
    "--test-type",
    "-t",
    type=click.Choice(["filesystem", "magic", "language", "all"], case_sensitive=False),
    default="all",
    help="Specify which type of tests to run (default: all).",
)
@click.option(
    "--filter-type",
    "-f",
    multiple=True,
    help="Filter results to only show specific file types (can be used multiple times).",
)
@click.option(
    "--include-directories",
    "-d",
    is_flag=True,
    help="Include directories in the output.",
)
@click.option(
    "--max-depth",
    type=int,
    help="Maximum directory depth to recurse (default: unlimited).",
)
@click.argument("paths", nargs=-1, type=click.Path(exists=False), required=False)
def main(
    verbose: bool,
    quiet: bool,
    test_type: str,
    filter_type: List[str],
    include_directories: bool,
    max_depth: int,
    paths: tuple,
) -> None:
    """
    Find File Type (fft) - Determine file types using filesystem, magic, and language tests.

    Analyzes files and directories to determine their types using a three-stage approach:
    1. Filesystem tests (extensions, permissions, attributes)
    2. Magic tests (file signatures and magic bytes)
    3. Language tests (content analysis and pattern matching)

    If no paths are specified, analyzes the current directory.

    Examples:

        fft myfile.txt                    # Analyze a single file

        fft dir1/ dir2/ file.py           # Analyze directories and files

        fft --verbose /home/user/code     # Detailed analysis

        fft --filter-type "Python source" --filter-type "JavaScript source" .
                                          # Show only specific file types

        fft --test-type magic .           # Use only magic byte detection
    """
    # If no paths provided, use current directory
    if not paths:
        paths = ["."]

    # Convert string paths to Path objects
    path_objects = [Path(p) for p in paths]

    # Initialize detector
    detector = FileTypeDetector()

    # Track statistics
    total_files = 0
    detected_files = 0
    errors = 0

    # Process files
    try:
        for file_path in walk_paths(path_objects):
            total_files += 1

            # Apply max depth filter if specified
            if max_depth is not None:
                try:
                    relative_path = file_path.relative_to(Path.cwd())
                    if len(relative_path.parts) > max_depth + 1:
                        continue
                except ValueError:
                    # File is not relative to current directory
                    pass

            try:
                # Detect file type
                result = detector.detect_file_type(file_path)

                # Skip directories if not requested
                if result.file_type == FileType.DIRECTORY and not include_directories:
                    continue

                # Apply test type filter
                if test_type != "all":
                    if result.test_type.value != test_type:
                        # Re-run detection with specific test type
                        result = _run_specific_test(detector, file_path, test_type)
                        if not result:
                            continue

                # Apply file type filter
                if filter_type:
                    if result.file_type.value not in filter_type:
                        continue

                # Count successful detections
                if result.file_type != FileType.UNKNOWN:
                    detected_files += 1

                # Format and display result
                _display_result(result, verbose, quiet)

            except Exception as e:
                errors += 1
                if verbose:
                    click.echo(f"Error processing '{file_path}': {e}", err=True)

    except KeyboardInterrupt:
        click.echo("\nInterrupted by user", err=True)
        sys.exit(1)

    # Show summary if verbose
    if verbose and total_files > 1:
        click.echo(
            f"\nSummary: {detected_files}/{total_files} files identified"
            + (f", {errors} errors" if errors else ""),
            err=True,
        )


def _run_specific_test(
    detector: FileTypeDetector, file_path: Path, test_type: str
) -> DetectionResult:
    """Run a specific type of test on a file."""
    if test_type == "filesystem":
        return detector._filesystem_tests(file_path)
    elif test_type == "magic":
        return detector._magic_tests(file_path)
    elif test_type == "language":
        return detector._language_tests(file_path)
    return None


def _display_result(result: DetectionResult, verbose: bool, quiet: bool) -> None:
    """Display a detection result with appropriate formatting."""
    if quiet:
        # Minimal output: just path and type
        click.echo(f"{result.file_path}: {result.file_type.value}")
    elif verbose:
        # Detailed output with all information
        confidence_pct = int(result.confidence * 100)
        test_info = f"[{result.test_type.value}, {confidence_pct}% confidence]"

        if result.details:
            click.echo(
                f"{result.file_path}: {result.file_type.value} {test_info} - {result.details}"
            )
        else:
            click.echo(f"{result.file_path}: {result.file_type.value} {test_info}")
    else:
        # Standard output
        click.echo(str(result))


if __name__ == "__main__":
    main()
