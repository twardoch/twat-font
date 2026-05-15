# twat-video

`twat-video` is the video domain package for the `twat` plugin ecosystem. It builds reusable, testable ffmpeg command wrappers and delegates AI video generation to `twat_genai` when such provider engines are available.

## Font-organizer preservation

This repository used to package `font_organizer`. The canonical copy now exists in `plugins/repos/twat_font` as `twat_font`, with the same organizer/core modules and CLI surface. The old source tree is left in this repo only as historical material; the build now packages `src/twat_video`.

## Requirements

Install `ffmpeg` and `ffprobe` for real media processing. Tests exercise command construction with `dry_run=True` and do not require media binaries.

## Python API

```python
from twat_video import crop_scale, import_audio, split_segment

crop_scale("input.mp4", "square.mp4", crop="1080:1080:420:0", scale="720:720")
split_segment("input.mp4", "clip.mp4", start=12.5, duration=4.0)
import_audio("silent.mp4", "voice.wav", "dubbed.mp4")
```

Implemented deterministic helpers:

- ffmpeg boundary: `run_command`, `run_ffmpeg`, `probe_video`.
- video geometry/timing: `crop_scale`, `change_fps`, `split_segment`, `reverse_video`.
- composition: `merge_by_gap`, `ken_burns`.
- audio/subtitle operations: `import_audio`, `extract_subtitles`, `repair_srt_text`, `add_reverb`.
- visual effect: `add_grain`.

## CLI

```bash
python -m twat_video --help
python -m twat_video crop-scale in.mp4 out.mp4 --crop 1080:1080:420:0 --scale 720:720 --dry-run
python -m twat_video fps in.mp4 out.mp4 24 --dry-run
python -m twat_video split in.mp4 clip.mp4 --start 1.5 --duration 3 --dry-run
python -m twat_video import-audio silent.mp4 voice.wav dubbed.mp4 --dry-run
python -m twat_video ken-burns still.png out.mp4 --duration 5 --dry-run
```

## AI video boundary

`generate_video()` is a narrow adapter. It imports `twat_genai` and calls a future `twat_genai.generate_video` provider API if present; it does not embed SkyReels, WAN, Chutes, or other provider clients.

## Reference scripts

Reusable patterns from `vidcropscale.py`, `vidfps`, `vidframedrop.py`, `vidsplit.py`, `vidreverse`, `vidmergebygap.py`, `vidkenburns.py`, `vidgrainer.py`, `vidreverb.py`, `vidimportaudio`, `mkv2srt.py`, and `srtmultifix.py` are represented as package APIs.

Watermark removal, menu-bar automation, JSON presets, batch shell wrappers, and local renaming/upload workflows remain in `reference/bin-img-vid/` because they are workstation-specific one-offs or policy-sensitive scripts rather than reusable package behavior.
