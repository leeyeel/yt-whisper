## 🌐 Language | 语言选择

- 🇺🇸 [English](#yt-whisper)（default）
- 🇨🇳 [中文](./README_CN.md)

# yt-whisper

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**yt-whisper** is a command-line tool for downloading YouTube videos, audio, and subtitles — with automatic subtitle generation powered by OpenAI's [Whisper](https://github.com/openai/whisper).

> ✅ Based on [m1guelpf/yt-whisper](https://github.com/m1guelpf/yt-whisper), modernized and extended with new features such as audio-only/video-only downloading, YouTube subtitle detection fallback, format selection, and CLI flexibility.

---

## ✨ Features

- 🎥 Download full YouTube videos
- 🔊 Extract audio as `.m4a`
- 🎬 Download video-only (no audio)
- 📝 Download subtitles:
  - Prefer official YouTube captions
  - Fallback to Whisper-generated subtitles when unavailable
- 🧠 Supports OpenAI Whisper models (`tiny` to `large`)
- 🌍 Auto-detect or manually specify spoken language
- 💬 Output in `.srt` or `.vtt` format
- 🧪 Simple CLI for scripting and automation

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/yt-whisper.git
cd yt-whisper

# Install dependencies
pip install -r requirements.txt

# Register CLI tool
pip install -e .
```

You can now use `yt-whisper` as a global command:

```bash
yt-whisper --help
```

---

## 🚀 Usage

### Download full video and subtitles
```bash
yt-whisper "https://youtube.com/watch?v=XXXX" --download video subtitles
```

### Download audio and generate subtitles (if YouTube has none)
```bash
yt-whisper "https://youtube.com/watch?v=XXXX" --download audio subtitles
```

### Download video-only (no audio)
```bash
yt-whisper "https://youtube.com/watch?v=XXXX" --download video-only
```

### Specify subtitle format and Whisper model
```bash
yt-whisper "https://youtube.com/watch?v=XXXX" \
  --download subtitles \
  --format vtt \
  --model base
```

---

## 🧠 Whisper Dependency

This project uses [openai/whisper](https://github.com/openai/whisper) under the hood for speech-to-text generation. You may benefit from GPU acceleration (via `CUDA`) if available.

---

## 📁 Output

All files are saved to the `--output_dir` directory (default: `./output/`):

- `title.mp4` – downloaded video
- `title.m4a` – extracted audio
- `title.srt` or `title.vtt` – subtitles (YouTube or Whisper-generated)

---

## 🙏 Credits

- Original project: [m1guelpf/yt-whisper](https://github.com/m1guelpf/yt-whisper)
- Audio transcription: [openai/whisper](https://github.com/openai/whisper)
- YouTube download: [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)

---
