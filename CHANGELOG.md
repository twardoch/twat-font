---
this_file: CHANGELOG.md
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Fixed `cli.py` to use `LegacyConfig` (generic `name`/`value`/`options` API) instead of the
  font-specific `core.Config`, resolving a `TypeError` in the `process` and `config` CLI commands.
- Fixed `tests/test_font_organizer.py` to import `LegacyConfig as Config` so that tests for
  the legacy `process_data` workflow continue to pass after `core.Config` was promoted to the
  primary `Config` export.
- Updated `CHANGELOG.md` with accurate project history (previous content was erroneously
  copied from the `twat-video` project).

## [v0.1.0] - 2025-06-01

### Added

- `src/twat_font/core/` sub-package with production-quality font management:
  - `Config` dataclass with `OrganizeConfig`, `ScanConfig`, and `SubsetConfig` sub-configs
  - `FontInfo` class for extracting metadata from TTF/OTF/WOFF/WOFF2 files
  - `FontManager` class for scanning, organising, and subsetting font collections
  - `FontMetadata` dataclass with `FontStyle` and `FontWeight` enums
  - Custom exceptions: `FontOrganizerError`, `FontNotFoundError`, `FontParseError`,
    `InvalidConfigError`
  - `load_config` / `save_config` helpers (YAML and JSON)
- Fire-based CLI entry point (`python -m twat_font`): `version`, `info`, `convert`, `subset`
  sub-commands via `fontTools`
- Click-based legacy CLI (`twat_font.cli`): `process`, `demo`, `config`, `version` commands
- `py.typed` marker — package is fully typed
- MkDocs + Material theme site (`mkdocs.yml`) with `mkdocstrings` API reference
- `pyproject.toml` with `hatchling` + `hatch-vcs` build system, `ruff`, `mypy`, and full
  test-extra dependency groups
- GitHub Actions CI (`push.yml`, `release.yml`)
- `twat.plugins` entry-point registration (`font = "twat_font"`)
- Comprehensive test suite: `test_cli.py`, `test_font_info.py`, `test_font_manager.py`,
  `test_font_organizer.py`, `test_integration.py`

## [v0.0.1] - 2025-02-15

### Added

- Initial project skeleton based on the standard `twat` plugin template
- Basic `font_organizer.py` module with placeholder `Config` dataclass and `process_data`
  function
- MIT Licence

[Unreleased]: https://github.com/twardoch/twat_font/compare/v0.1.0...HEAD
[v0.1.0]: https://github.com/twardoch/twat_font/compare/v0.0.1...v0.1.0
[v0.0.1]: https://github.com/twardoch/twat_font/releases/tag/v0.0.1
