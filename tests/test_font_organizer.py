"""Deprecated font-organizer test replaced by twat_video smoke coverage."""
# this_file: tests/test_font_organizer.py

import twat_video


def test_twat_video_imports() -> None:
    assert twat_video.__version__
    assert callable(twat_video.crop_scale)
