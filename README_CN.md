# yt-whisper

### 📌 项目简介

**yt-whisper** 是一个命令行工具，用于下载 YouTube 视频、音频以及字幕。它会自动优先使用 YouTube 自带字幕，如果没有字幕，则使用 OpenAI 的 [Whisper](https://github.com/openai/whisper) 语音识别模型自动生成字幕。

该工具基于 [m1guelpf/yt-whisper](https://github.com/m1guelpf/yt-whisper) 项目进行改进，增强了字幕优先选择逻辑、格式控制、自动提取音频等功能，适用于个人整理视频资料或内容创作者批量处理字幕。

---

### ✨ 功能特性

- 🎥 下载完整视频（含音频）
- 🔊 下载音频（保持原始格式，如 `.webm`, `.m4a`）
- 🎬 下载仅视频轨道（无音频）
- 📝 字幕下载：
  - 优先使用 YouTube 官方或自动字幕
  - 无字幕时，使用 Whisper 自动生成
- 🧠 支持 OpenAI Whisper 多种模型（tiny ~ large）
- 🌐 支持自动语言检测，也可手动指定语言
- 📄 字幕格式支持 `.srt` 和 `.vtt`
- 💡 易用的 CLI 接口，适合自动化任务

---

### 📦 安装方法

```bash
# 克隆仓库
git clone https://github.com/your-username/yt-whisper.git
cd yt-whisper

# 安装依赖
pip install -r requirements.txt

# 注册命令行工具
pip install -e .
```

---

### 🚀 使用示例

#### 下载视频和字幕（优先使用 YouTube 原字幕）

```bash
yt-whisper "https://www.youtube.com/watch?v=xxxx" --download video subtitles
```

#### 下载音频 + 自动生成字幕

```bash
yt-whisper "https://www.youtube.com/watch?v=xxxx" --download audio subtitles
```

#### 下载纯视频（无音轨）

```bash
yt-whisper "https://www.youtube.com/watch?v=xxxx" --download video-only
```

#### 指定 Whisper 模型、语言、字幕格式

```bash
yt-whisper "https://www.youtube.com/watch?v=xxxx" \
  --download subtitles \
  --model medium \
  --format vtt
```

---

### 📁 输出文件说明

| 文件名             | 说明                       |
|--------------------|----------------------------|
| `xxx.mp4`          | 下载的视频文件（含音频）    |
| `xxx.webm` / `.m4a`| 音频文件（原始格式）       |
| `xxx.srt` / `.vtt` | 字幕文件（YouTube或Whisper）|

默认输出到 `./output` 目录，可通过 `--output_dir` 修改。

---

### 🧠 Whisper 模型提示

- 模型从 `tiny` 到 `large`，推荐使用 `base` 或以上模型提升识别准确率。
- 支持 GPU 加速（CUDA）。
- Whisper 输出字幕为英文（`--task translate`）或原语言（`--task transcribe`）。

---

### 🙏 致谢

- 基础项目：[m1guelpf/yt-whisper](https://github.com/m1guelpf/yt-whisper)
- 语音识别：[openai/whisper](https://github.com/openai/whisper)
- 视频下载：[yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

## 🔗 导航回英文版本

[⬆ Back to English version](./README.md)
