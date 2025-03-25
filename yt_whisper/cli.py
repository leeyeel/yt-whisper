import argparse
import os
import tempfile
import yt_dlp
import whisper
import glob
import subprocess
from .utils import slugify, clean_url, write_srt, write_vtt

def parse_args():
    parser = argparse.ArgumentParser(description="YouTube video/audio/subtitle downloader with Whisper support")
    parser.add_argument("url", help="YouTube video URL")

    parser.add_argument("--download", nargs="+",
                        choices=["video", "audio", "video-only", "subtitles"],
                        required=True,
                        help="Content to download (video, audio, video-only, subtitles)")

    parser.add_argument("--model", default="small", choices=whisper.available_models(),
                        help="Whisper model for subtitle generation")
    parser.add_argument("--language", default=None, help="Language for Whisper (auto-detect by default)")
    parser.add_argument("--format", default="srt", choices=["srt", "vtt"],
                        help="Subtitle file format")
    parser.add_argument("--output_dir", default="./output", help="Output directory")
    parser.add_argument("--force_whisper", action="store_true",
                        help="Force subtitle generation with Whisper even if YouTube subtitles exist")

    return parser.parse_args()

def download_youtube(url, download_types, temp_dir, force_whisper):
    common_opts = {
        "quiet": False,
        "noplaylist": True,
        "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
        "writesubtitles": "subtitles" in download_types,
        "writeautomaticsub": "subtitles" in download_types,
        "subtitleslangs": ['en', 'auto'],
        "subtitlesformat": "srt/vtt",
        "extractor_args": {
            'youtube': {
                'player_client': ['web', 'android'],
            },
        },
    }

    title = video_path = audio_path = subtitle_path = None

    with yt_dlp.YoutubeDL(common_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = slugify(info.get("title", info["id"]))
        video_id = info["id"]

    # Step 1: Download video if requested or required for subtitles
    if "video" in download_types:
        video_opts = common_opts.copy()
        video_opts["format"] = "bestvideo+bestaudio/best"
        video_opts["merge_output_format"] = "mp4"
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = info["requested_downloads"][0]["filepath"]

    # Step 2: Download audio separately if explicitly requested
    if "audio" in download_types and not video_path:
        audio_opts = common_opts.copy()
        audio_opts["format"] = "bestaudio/best"
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_path = info["requested_downloads"][0]["filepath"]

            # If audio failed, fallback to video download
            if audio_path is None:
                print("⚠️ No audio stream available. Downloading video instead to extract audio...")
                video_opts = common_opts.copy()
                video_opts["format"] = "bestvideo+bestaudio/best"
                with yt_dlp.YoutubeDL(video_opts) as ydl_video:
                    info = ydl_video.extract_info(url, download=True)
                    video_path = info["requested_downloads"][0]["filepath"]

    # Step 3: Find subtitles if downloaded
    if "subtitles" in download_types:
        subtitle_files = glob.glob(os.path.join(temp_dir, f"{video_id}*.srt")) + \
                         glob.glob(os.path.join(temp_dir, f"{video_id}*.vtt"))
        if subtitle_files and not force_whisper:
            subtitle_path = subtitle_files[0]

        # If no subtitles, ensure audio is available for Whisper transcription
        elif audio_path is None:
            # Try extracting audio from previously downloaded video (do not download again)
            if video_path and os.path.exists(video_path):
                print("⚠️ No subtitles available, extracting audio from downloaded video...")
                audio_path = os.path.join(temp_dir, f"{video_id}.m4a")
                extract_audio_from_video(video_path, audio_path)
            else:
                # As a fallback, download audio separately
                print("⚠️ No subtitles and no downloaded video. Downloading audio directly...")
                audio_opts = common_opts.copy()
                audio_opts["format"] = "bestaudio/best"
                with yt_dlp.YoutubeDL(audio_opts) as ydl_audio:
                    info = ydl_audio.extract_info(url, download=True)
                    audio_path = info["requested_downloads"][0]["filepath"]

                    if audio_path is None:
                        raise RuntimeError("❌ Failed to download audio for subtitles generation.")

    return title, video_path, audio_path, subtitle_path

def extract_audio_from_video(video_path, audio_output):
    command = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "copy", audio_output
    ]
    subprocess.run(command, check=True)
    print(f"✅ Audio extracted: {audio_output}")

def generate_whisper_subtitles(audio_path, model_name, language, task):
    model = whisper.load_model(model_name)
    return model.transcribe(audio_path, language=language, task=task)

def main():
    args = parse_args()
    args.url = clean_url(args.url)
    os.makedirs(args.output_dir, exist_ok=True)

    title, video_path, audio_path, subtitle_path = download_youtube(args.url, args.download, args.output_dir, args.force_whisper)

    # Save video
    if video_path and ("video" in args.download or "video-only" in args.download):
        ext = video_path.split('.')[-1]
        final_video_path = os.path.join(args.output_dir, f"{title}.{ext}")
        os.rename(video_path, final_video_path)
        print(f"✅ Video saved: {final_video_path}")

    # Save audio
    if audio_path and "audio" in args.download:
        ext = os.path.splitext(audio_path)[-1]  # e.g. .webm
        final_audio_path = os.path.join(args.output_dir, f"{title}{ext}")
        os.rename(audio_path, final_audio_path)
        print(f"✅ Audio saved: {final_audio_path}")

    # Handle subtitles
    if "subtitles" in args.download:
        final_sub_path = os.path.join(args.output_dir, f"{title}.{args.format}")

        if subtitle_path:
            os.rename(subtitle_path, final_sub_path)
            print(f"✅ Official YouTube subtitles saved: {final_sub_path}")
        else:
            if not audio_path:
                print("⚠️ No audio found. Downloading audio for subtitle generation...")
                args.download.append("audio")
                _, _, audio_path, _ = download_youtube(args.url, ["audio"], args.output_dirt, args.force_whisper)

            if audio_path:
                print("🤖 Generating subtitles with Whisper...")
                result = generate_whisper_subtitles(audio_path, args.model, args.language, "transcribe")
                with open(final_sub_path, "w", encoding="utf-8") as f:
                    if args.format == "srt":
                        write_srt(result["segments"], f)
                    else:
                        write_vtt(result["segments"], f)
                print(f"✅ Whisper subtitles generated: {final_sub_path}")
            else:
                print("❌ Failed to generate subtitles (audio download failed)")

if __name__ == "__main__":
    main()

