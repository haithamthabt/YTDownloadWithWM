from yt_dlp import YoutubeDL
import subprocess


#testing url https://youtu.be/wpJnigMKFmQ?feature=shared
def extract_video_info(video_url):
    """
    Extracts video information and formats using yt_dlp.
    """
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info.get('formats', [])
    except Exception as e:
        print(f"An error occurred while extracting info: {e}")
        return None

def get_best_audio_format(formats):
    """
    Finds the best audio format based on bitrate (abr).
    """
    audio_formats = [f for f in formats if f.get('acodec', 'none') != 'none' and f.get('vcodec', 'none') == 'none']
    best_audio = max(audio_formats, key=lambda f: f.get('abr', 0))
    return best_audio

def get_best_video_format(formats):
    """
    Finds the best video format based on resolution, FPS, and codec (VP9 > AVC1).
    """
    video_formats = [f for f in formats if f.get('acodec', 'none') == 'none' and f.get('vcodec', 'none') != 'none']

    # Step 1: Highest resolution
    max_height = max(f.get('height', 0) for f in video_formats)
    highest_res_videos = [f for f in video_formats if f.get('height', 0) == max_height]

    # Step 2: Highest FPS among highest resolution
    max_fps = max(f.get('fps', 0) for f in highest_res_videos)
    highest_res_and_fps_videos = [f for f in highest_res_videos if f.get('fps', 0) == max_fps]

    # Step 3: Best codec (VP9 > AVC1)
    if any(f.get('vcodec', '').lower().startswith("vp9") or f.get('vcodec', '').lower().startswith("vp09") for f in highest_res_and_fps_videos):
        best_codec_videos = [f for f in highest_res_and_fps_videos if "vp9" in f.get('vcodec', '').lower() or "vp09" in f.get('vcodec', '').lower()]
    else:
        best_codec_videos = [f for f in highest_res_and_fps_videos if "avc1" in f.get('vcodec', '').lower()]

    # Select the best video format
    best_video = best_codec_videos[0] if best_codec_videos else highest_res_and_fps_videos[0]
    return best_video

def filter_matching_video_formats(formats, best_video):
    """
    Filters video formats matching the best video's FPS and codec.
    Excludes formats without a file size.
    """
    matching_formats = [
    f for f in formats
    if f.get('fps', 0) == best_video.get('fps', 0) and
       (
           any(codec in f.get('vcodec', '').lower() for codec in ["vp9", "vp09"])
           if "vp9" in best_video.get('vcodec', '').lower() or "vp09" in best_video.get('vcodec', '').lower()
           else "avc1" in f.get('vcodec', '').lower()
       ) and
       f.get('filesize') is not None
]

    return matching_formats

def download_video(video_url, video_format_id, audio_format_id, output_path):
    """
    Downloads the selected video and audio formats and injects bitrate metadata.
    """
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_format = next(f for f in info['formats'] if f['format_id'] == video_format_id)
            audio_format = next(f for f in info['formats'] if f['format_id'] == audio_format_id)

        # Extract video and audio bitrates
        video_bitrate = video_format.get('tbr', 0)
        audio_bitrate = audio_format.get('abr', 0)

        # yt-dlp options
        output_file = f"{output_path}/%(title)s.%(ext)s"
        ydl_opts = {
            'format': f"{video_format_id}+{audio_format_id}",
            'outtmpl': output_file,
            'merge_output_format': 'mkv',
            'postprocessor_args': [
                '-metadata', f'VIDEO_BITRATE={video_bitrate} kbps',
                '-metadata', f'AUDIO_BITRATE={audio_bitrate} kbps',
            ]
        }

        # Start the download
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return f"✅ Video downloaded Successfully"
    except Exception as e:
        return f"❌ Error: {e}"





