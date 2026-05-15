"""twat-video: video processing helpers and optional AI video adapters."""
# this_file: src/twat_video/__init__.py

from importlib.metadata import PackageNotFoundError, version

from twat_video.__main__ import main as cli_main

try:
    __version__ = version("twat-video")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

from twat_video.ffmpeg import CommandResult, ffprobe_json, run_command, run_ffmpeg
from twat_video.genai import generate_video
from twat_video.operations import (
    VideoClip,
    add_grain,
    add_reverb,
    change_fps,
    crop_scale,
    extract_subtitles,
    import_audio,
    ken_burns,
    merge_by_gap,
    probe_video,
    repair_srt_text,
    reverse_video,
    split_segment,
)


def main() -> None:
    """CLI entry point for twat-video."""
    cli_main()


__all__ = [
    "CommandResult",
    "VideoClip",
    "__version__",
    "add_grain",
    "add_reverb",
    "change_fps",
    "crop_scale",
    "extract_subtitles",
    "ffprobe_json",
    "generate_video",
    "import_audio",
    "ken_burns",
    "main",
    "merge_by_gap",
    "probe_video",
    "repair_srt_text",
    "reverse_video",
    "run_command",
    "run_ffmpeg",
    "split_segment",
]
