# Find File Type (fft)

A modern Python command line tool for determining file types using comprehensive detection methods.

## Overview

`fft` (Find File Type) searches for files in directory hierarchies and determines their types using a systematic approach. The tool tests each argument to classify files by performing three sets of tests in order:

1. **Filesystem tests** - Extension-based and file attribute analysis
2. **Magic tests** - File signature and magic byte detection  
3. **Language tests** - Programming language and content analysis

The first successful test determines the file type that gets printed.

## Features

- 🔍 **Recursive directory traversal** - Search entire directory trees
- 📁 **Multiple detection methods** - Filesystem, magic bytes, and language analysis
- ⚡ **Fast and efficient** - Optimized file scanning with early termination
- 🎯 **Accurate detection** - Comprehensive file type database
- 📊 **Detailed output** - Clear file type classification results
- 🛠️ **Modern Python** - Built with Python 3.8+ and type hints

## Installation

### From PyPI (when published)
```bash
pip install find-file-type
```

### From Source
```bash
git clone https://github.com/example/find-file-type.git
cd find-file-type
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/example/find-file-type.git
cd find-file-type
pip install -e ".[dev]"
```

## Usage

### Basic Usage

Analyze a single file:
```bash
fft myfile.txt
```

Analyze multiple files:
```bash
fft file1.py file2.js file3.bin
```

Analyze a directory (recursive):
```bash
fft /path/to/directory
```

Analyze multiple directories and files:
```bash
fft dir1/ dir2/ file.txt
```

### Examples

```bash
# Analyze current directory
fft .

# Analyze specific files
fft script.py image.jpg document.pdf

# Analyze with verbose output
fft --verbose /home/user/projects

# Show help
fft --help
```

## Detection Methods

### 1. Filesystem Tests
- File extension analysis
- File permissions and attributes
- Symbolic link detection
- File size characteristics

### 2. Magic Tests  
- Magic byte signatures
- File headers and footers
- Binary format detection
- Archive and container formats

### 3. Language Tests
- Programming language detection
- Syntax pattern matching
- Shebang line analysis
- Language-specific markers

## Supported File Types

The tool can detect hundreds of file types including:

- **Programming Languages**: Python, JavaScript, Java, C/C++, Go, Rust, etc.
- **Documents**: PDF, Word, Excel, PowerPoint, etc.
- **Images**: JPEG, PNG, GIF, SVG, TIFF, etc.
- **Audio/Video**: MP3, MP4, AVI, WAV, etc.
- **Archives**: ZIP, TAR, RAR, 7Z, etc.
- **Data Formats**: JSON, XML, CSV, YAML, etc.
- **System Files**: Config files, logs, executables, etc.

## Development

### Setup Development Environment
```bash
git clone https://github.com/example/find-file-type.git
cd find-file-type
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest
pytest --cov=fft  # with coverage
```

### Code Formatting
```bash
black src/fft/
```

### Type Checking
```bash
mypy src/fft/
```

### Linting
```bash
flake8 src/fft/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Dependencies

- `python-magic` - For magic byte detection
- `click` - For command line interface

## Requirements

- Python 3.8 or higher
- libmagic (system dependency for python-magic)

### Installing libmagic

**Ubuntu/Debian:**
```bash
sudo apt-get install libmagic1
```

**macOS:**
```bash
brew install libmagic
```

**Windows:**
```bash
# python-magic-bin includes Windows binaries
pip install python-magic-bin
``` 
