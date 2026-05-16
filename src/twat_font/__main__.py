# this_file: src/twat_font/__main__.py
"""Fire CLI entry point for twat-font."""

from __future__ import annotations

import fire


def _version() -> str:
    """Print the installed twat-font version."""
    from twat_font.__version__ import __version__

    return __version__


def _info(font_path: str) -> dict:
    """Show metadata for the font file at FONT_PATH.

    Args:
        font_path: Path to a .ttf/.otf/.woff/.woff2 font file.
    """
    from pathlib import Path

    from twat_font.core.font_info import FontInfo

    info = FontInfo(Path(font_path).expanduser().resolve())
    return info.get_info_dict()


def _convert(
    font_path: str,
    output: str,
    *,
    flavor: str | None = None,
) -> str:
    """Convert a font file to another format using fontTools.

    Args:
        font_path: Path to the source font file.
        output: Destination path (extension determines target format).
        flavor: Optional woff/woff2 flavor override.
    """
    from pathlib import Path

    from fontTools.ttLib import TTFont

    src = Path(font_path).expanduser().resolve()
    dst = Path(output).expanduser().resolve()
    font = TTFont(src, recalcBBoxes=False)
    if flavor:
        font.flavor = flavor
    font.save(str(dst))
    return str(dst)


def _subset(
    font_path: str,
    output: str,
    *,
    text: str = "",
    unicodes: str = "",
    glyphs: str = "",
) -> str:
    """Subset a font to the given characters/unicodes/glyphs via fontTools.

    Args:
        font_path: Path to the source font file.
        output: Destination path for the subsetted font.
        text: Characters to keep (e.g. "Hello world").
        unicodes: Comma-separated hex codepoints (e.g. "0041,0042").
        glyphs: Space-separated glyph names (e.g. "A B C").
    """
    from pathlib import Path

    from fontTools import subset as ft_subset

    src = Path(font_path).expanduser().resolve()
    dst = Path(output).expanduser().resolve()

    args = [str(src), f"--output-file={dst}"]
    if text:
        args.append(f"--text={text}")
    if unicodes:
        args.append(f"--unicodes={unicodes}")
    if glyphs:
        args.append(f"--glyphs={glyphs}")

    ft_subset.main(args)
    return str(dst)


COMMANDS: dict[str, object] = {
    "version": _version,
    "info": _info,
    "convert": _convert,
    "subset": _subset,
}


def main() -> None:
    """twat-font: font inspection and transformation utilities."""
    fire.Fire(COMMANDS, name="twat-font")


def cmd_version() -> None:
    """twat-font version."""
    fire.Fire(_version, name="twat-font-version")


def cmd_info() -> None:
    """Show font metadata."""
    fire.Fire(_info, name="twat-font-info")


def cmd_convert() -> None:
    """Convert a font to another format."""
    fire.Fire(_convert, name="twat-font-convert")


def cmd_subset() -> None:
    """Subset a font to specific characters."""
    fire.Fire(_subset, name="twat-font-subset")


if __name__ == "__main__":
    main()
