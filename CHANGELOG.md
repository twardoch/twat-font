# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure and scaffolding
- Core module architecture for font management
  - `FontInfo` class for extracting font metadata
  - `FontManager` class for coordinating font operations
  - `Config` system with YAML/JSON support
  - Custom exceptions for better error handling
- Font information extraction capabilities
  - Font family, subfamily, and style detection
  - Weight classification (100-900 scale)
  - Character coverage analysis
  - OpenType feature detection
  - File hash calculation for duplicate detection
- MkDocs documentation setup with Material theme
- Comprehensive test suite with pytest
- CI/CD workflows for automated testing and releases
- Pre-commit hooks for code quality
- Binary build support with PyInstaller

### Changed
- Renamed project from twat-video to font-organizer
- Updated all documentation to reflect font management focus
- Restructured package to use modular architecture

### Planned Features
- Font detection and scanning functionality
- Intelligent font organization by family, style, and weight
- Font subsetting capabilities
- Duplicate font detection
- Font analysis and reporting tools
- Web font optimization
- Character coverage analysis
- OpenType feature extraction

## [0.1.0] - TBD

Initial release (planned)

[Unreleased]: https://github.com/twardoch/font-organizer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/twardoch/font-organizer/releases/tag/v0.1.0