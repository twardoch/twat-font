"""twat-font: Font organization and management."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("twat-font")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

from twat_font.font_organizer import Config as LegacyConfig, main as _legacy_main, process_data
from twat_font.core import (
    Config,
    FontInfo,
    FontManager,
    FontMetadata,
    FontStyle,
    FontWeight,
    FontOrganizerError,
    FontNotFoundError,
    FontParseError,
    InvalidConfigError,
    load_config,
    save_config,
)

try:
    from twat_font.cli import main
except ImportError:

    def main() -> None:
        """CLI entry point for the twat font plugin."""
        _legacy_main()


__all__ = [
    "Config",
    "FontInfo",
    "FontManager",
    "FontMetadata",
    "FontNotFoundError",
    "FontOrganizerError",
    "FontParseError",
    "FontStyle",
    "FontWeight",
    "InvalidConfigError",
    "LegacyConfig",
    "__version__",
    "load_config",
    "main",
    "process_data",
    "save_config",
]
