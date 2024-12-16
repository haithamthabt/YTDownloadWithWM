from yt_dlp import YoutubeDL
import subprocess
import os
from watermark import add_moving_watermark

#testing url https://youtu.be/wpJnigMKFmQ?feature=shared
#another url longer https://youtu.be/CdTtTCK2EPU?feature=shared

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
    Excludes formats with audio and formats without a file size.
    """
    matching_formats = [
        f for f in formats
        if f.get('fps', 0) == best_video.get('fps', 0) and
           f.get('acodec', 'none') == 'none' and  # Exclude formats with audio
           (
               f.get('vcodec', '').lower().startswith("vp")  # VP9 or variants like vp09.xxx
               if best_video.get('vcodec', '').lower().startswith("vp")
               else "avc1" in f.get('vcodec', '').lower()  # Match avc1 codec
           ) and
           f.get('filesize') is not None  # Ensure file size exists
    ]
    return matching_formats

def download_video(video_url, video_format_id, audio_format_id, output_path, watermark=True, watermark_text="LIMITLESS MEDIA", progress_callback=None):
    """
    Downloads the selected video and audio formats, merges them, applies a watermark if enabled,
    and removes the temporary merged file after successfully creating the watermarked file.
    Also adds audio bitrate metadata to the output file.
    """
    try:
        # Progress hook function for yt_dlp
        def progress_hook(d):
            if d['status'] == 'downloading':
                downloaded_bytes = d.get('downloaded_bytes', 0)
                total_bytes = d.get('total_bytes', 1)
                percentage = (downloaded_bytes / total_bytes) * 100
                if progress_callback:
                    progress_callback(percentage)  # Update the progress bar
            elif d['status'] == 'finished':
                if progress_callback:
                    progress_callback(100)  # Ensure progress reaches 100% at the end

        # Extract video properties
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_format = next(f for f in info['formats'] if f['format_id'] == video_format_id)
            audio_format = next(f for f in info['formats'] if f['format_id'] == audio_format_id)

        video_title = info.get('title', 'downloaded_video').replace("/", "_")  # Prevent invalid filename characters
        video_codec = video_format.get('vcodec', 'libx264')
        video_bitrate = video_format.get('tbr', 0)
        audio_bitrate = audio_format.get('abr', 0)  # Get audio bitrate for metadata

        # File paths
        merged_input = f"{output_path}/{video_title}_temp.mkv"  # Temporary merged video
        output_watermarked = f"{output_path}/{video_title}.mkv"

        # Step 1: Download video and audio into a temporary merged file
        ydl_opts = {
            'format': f"{video_format_id}+{audio_format_id}",
            'outtmpl': merged_input,
            'merge_output_format': 'mkv',
            'progress_hooks': [progress_hook],  # Attach the progress hook
            'postprocessor_args': [
                # Add metadata during merge
                '-metadata', f'audio_bitrate={audio_bitrate}kbps',
                '-metadata', f'video_bitrate={video_bitrate}kbps',
                '-metadata', f'description=Video Bitrate: {video_bitrate}kbps, Audio Bitrate: {audio_bitrate}kbps',
                # Add metadata specifically to audio stream
                '-metadata:s:a:0', f'title={video_title} audio',
                '-metadata:s:a:0', f'bitrate={audio_bitrate}',
                # Add metadata specifically to video stream
                '-metadata:s:v:0', f'title={video_title} video',
                '-metadata:s:v:0', f'bitrate={video_bitrate}',
                # Clear any existing metadata that might interfere
                '-map_metadata', '-1'
            ],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Step 2: Apply watermark if enabled
        if watermark:
            try:
                add_moving_watermark(
                    input_file=merged_input,
                    output_file=output_watermarked,
                    watermark_text=watermark_text,
                    video_codec=video_codec,
                    video_bitrate=video_bitrate
                )

                # Delete the temporary merged file only after successful watermarking
                if os.path.exists(merged_input):
                    os.remove(merged_input)

                return f" Video downloaded and watermarked: {output_watermarked}"

            except Exception as e:
                return f" Error during watermarking: {e}. Temporary file saved as {merged_input}"

        # If watermarking is disabled, rename the temporary file to the final output
        final_output = f"{output_path}/{video_title}.mkv"
        os.rename(merged_input, final_output)
        return f" Video downloaded successfully: {final_output}"

    except Exception as e:
        return f" Error: {e}"
