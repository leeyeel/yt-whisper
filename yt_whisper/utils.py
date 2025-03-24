from typing import Iterator, TextIO
import re

def str2bool(string):
    str2val = {"True": True, "False": False}
    if string in str2val:
        return str2val[string]
    else:
        raise ValueError(
            f"Expected one of {set(str2val.keys())}, got {string}")


def break_line(line: str, length: int):
    break_index = min(len(line)//2, length) # split evenly or at maximum length

    # work backwards from that guess to split between words
    # if break_index <= 1, we've hit the beginning of the string and can't split
    while break_index > 1:
        if line[break_index - 1] == " ":
            break # break at space
        else:
            break_index -= 1
    if break_index > 1:
        # split the line, not including the space at break_index
        return line[:break_index - 1] + "\n" + line[break_index:]
    else:
        return line

def process_segment(segment: dict, line_length: int = 0):
    segment["text"] = segment["text"].strip()
    if line_length > 0 and len(segment["text"]) > line_length:
        # break at N characters as per Netflix guidelines
        segment["text"] = break_line(segment["text"], line_length)
    
    return segment

def write_vtt(transcript: Iterator[dict], file: TextIO, line_length: int = 0):
    print("WEBVTT\n", file=file)
    for segment in transcript:
        segment = process_segment(segment, line_length=line_length)

        print(
            f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n"
            f"{segment['text'].strip().replace('-->', '->')}\n",
            file=file,
            flush=True,
        )

def format_timestamp(seconds: float):
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    millis = (secs - int(secs)) * 1000
    return f"{int(hours):02}:{int(minutes):02}:{int(secs):02},{int(millis):03}"

def write_srt(segments, file, min_duration=2.0, auto_merge=True):
    """
    Writes improved SRT subtitles to the given file.
    Automatically merges short segments and enforces a minimum display duration.
    """

    # --- Step 1: Auto-merge short segments ---
    if auto_merge:
        merged = []
        buffer = segments[0]
        for seg in segments[1:]:
            buffer_duration = buffer["end"] - buffer["start"]
            if buffer_duration < min_duration:
                # Merge this segment into buffer
                buffer["text"] = buffer["text"].strip() + " " + seg["text"].strip()
                buffer["end"] = seg["end"]
            else:
                merged.append(buffer)
                buffer = seg
        merged.append(buffer)
    else:
        merged = segments

    # --- Step 2: Enforce min duration + avoid overlap ---
    for i, seg in enumerate(merged):
        seg["text"] = re.sub(r"\s+", " ", seg["text"].strip())

        seg_start = seg["start"]
        seg_end = seg["end"]
        duration = seg_end - seg_start

        # Enforce minimum duration
        if duration < min_duration:
            seg_end = seg_start + min_duration

        # Avoid overlapping with next segment
        if i + 1 < len(merged):
            next_start = merged[i + 1]["start"]
            if seg_end > next_start:
                seg_end = next_start - 0.1

        seg["end"] = round(seg_end, 3)

    # --- Step 3: Write to file ---
    for i, seg in enumerate(merged, start=1):
        file.write(f"{i}\n")
        file.write(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}\n")
        file.write(f"{seg['text']}\n\n")

def slugify(value):
    value = str(value)
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)

def clean_url(url: str) -> str:
    if url.startswith("http://") or url.startswith("https://"):
        return url.replace("\\", "")
    return url

