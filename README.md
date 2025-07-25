# Font Organizer: Modern Font Management Tool

[![Build & Test](https://github.com/twardoch/font-organizer/actions/workflows/push.yml/badge.svg)](https://github.com/twardoch/font-organizer/actions/workflows/push.yml)
[![Release](https://github.com/twardoch/font-organizer/actions/workflows/release.yml/badge.svg)](https://github.com/twardoch/font-organizer/actions/workflows/release.yml)
[![PyPI version](https://badge.fury.io/py/font-organizer.svg)](https://badge.fury.io/py/font-organizer)

**Font Organizer is a powerful Python-based tool for managing and organizing font collections. It provides intelligent font detection, automated organization, subsetting capabilities, and comprehensive analysis features to help you manage large font libraries efficiently.**

## 🚀 Features

- 🔍 **Smart Font Detection**: Automatically discover fonts across your system
- 📁 **Intelligent Organization**: Sort and categorize fonts by various criteria (family, style, weight)
- 🔤 **Font Subsetting**: Extract specific character sets for optimized web fonts
- 📊 **Analysis Tools**: Examine font metrics, character coverage, and OpenType features
- 🚀 **High Performance**: Efficient processing of large font collections with multi-threading support
- 🔄 **Duplicate Detection**: Find and manage duplicate fonts by hash and metadata
- 📈 **Reporting**: Generate detailed HTML/PDF reports about your font collection

## 📦 Installation

### Using pip (Recommended)

```bash
pip install font-organizer
```

### Using uv (Fast Alternative)

```bash
uv pip install font-organizer
```

### From Source

```bash
git clone https://github.com/twardoch/font-organizer.git
cd font-organizer
pip install -e .
```

## 🎯 Quick Start

### Basic Usage

```bash
# Scan a directory for fonts
font-organizer scan ~/Fonts

# Organize fonts by family
font-organizer organize ~/Fonts --by family --output ~/OrganizedFonts

# Get information about a specific font
font-organizer info ~/Fonts/Arial.ttf

# Find duplicate fonts
font-organizer duplicates ~/Fonts

# Create a subset with basic Latin characters
font-organizer subset input.ttf output.woff2 --text "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
```

### Command Overview

```bash
font-organizer --help
```

Available commands:
- `scan` - Scan directories for font files
- `organize` - Organize fonts using various criteria
- `analyze` - Analyze font collections and generate reports
- `subset` - Create font subsets with specific characters
- `duplicates` - Find and manage duplicate fonts
- `info` - Display detailed font information
- `config` - Manage configuration settings

## 🔧 Configuration

Font Organizer can be configured using a YAML configuration file:

```yaml
# ~/.font-organizer/config.yaml
organize:
  default_scheme: family  # family, style, weight, or custom
  copy_mode: true  # true for copy, false for move
  
scan:
  include_system_fonts: true
  recursive: true
  font_extensions:
    - .ttf
    - .otf
    - .woff
    - .woff2
    
subset:
  default_format: woff2
  optimize: true
```

## 📚 Advanced Usage

### Organizing Fonts

```bash
# Organize by multiple criteria
font-organizer organize ~/Fonts --by family,weight --output ~/Organized

# Use custom organization rules
font-organizer organize ~/Fonts --rules my-rules.yaml --output ~/Organized

# Dry run to preview organization
font-organizer organize ~/Fonts --dry-run
```

### Font Analysis

```bash
# Generate comprehensive analysis report
font-organizer analyze ~/Fonts --output report.html

# Export font list to CSV
font-organizer analyze ~/Fonts --format csv --output fonts.csv

# Check character coverage
font-organizer analyze ~/Fonts --coverage "Latin,Cyrillic"
```

### Subsetting Fonts

```bash
# Create subset with Unicode ranges
font-organizer subset input.ttf output.woff2 --unicodes "U+0020-007F,U+00A0-00FF"

# Subset for specific language
font-organizer subset input.ttf output.woff2 --language en,es,fr

# Keep specific OpenType features
font-organizer subset input.ttf output.woff2 --features "kern,liga"
```

## 🐍 Python API

```python
from font_organizer import FontOrganizer, FontInfo

# Initialize organizer
organizer = FontOrganizer()

# Scan for fonts
fonts = organizer.scan_directory("~/Fonts")

# Get font information
for font_path in fonts:
    info = FontInfo(font_path)
    print(f"{info.family} - {info.style} ({info.weight})")
    print(f"  Characters: {len(info.characters)}")
    print(f"  Features: {', '.join(info.features)}")

# Organize fonts
organizer.organize(
    source="~/Fonts",
    destination="~/OrganizedFonts",
    scheme="family"
)

# Find duplicates
duplicates = organizer.find_duplicates("~/Fonts")
for group in duplicates:
    print(f"Duplicate group ({len(group)} files):")
    for font in group:
        print(f"  - {font}")
```

## 🛠️ Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/twardoch/font-organizer.git
cd font-organizer

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
ruff check src tests
mypy src tests
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=font_organizer --cov-report=html

# Run specific test file
pytest tests/test_font_info.py
```

## 📖 Documentation

Full documentation is available at [https://twardoch.github.io/font-organizer/](https://twardoch.github.io/font-organizer/)

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [fonttools](https://github.com/fonttools/fonttools) for font manipulation
- Uses [rich](https://github.com/Textualize/rich) for beautiful terminal output
- Powered by [fire](https://github.com/google/python-fire) for CLI interface

## 📬 Contact

Adam Twardoch - [@adamtwar](https://twitter.com/adamtwar) - adam+github@twardoch.com

Project Link: [https://github.com/twardoch/font-organizer](https://github.com/twardoch/font-organizer)