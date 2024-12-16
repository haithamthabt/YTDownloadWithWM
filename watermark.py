import subprocess

def add_moving_watermark(input_file, output_file, watermark_text, video_codec="libx264", video_bitrate=None):
    """
    Adds a moving watermark to the input video using FFmpeg and saves it to the output file.
    Handles re-encoding with forced keyframes and optimized buffer size for quality and performance.
    """
    try:
        # Configure codec and bitrate
        reencode_codec = "libvpx-vp9" if video_codec.lower().startswith("vp") else "libx264"
        bitrate_option = ["-b:v", f"{video_bitrate}k"] if video_bitrate else ["-crf", "22"]

        # FFmpeg command for moving watermark
        command = [
            "ffmpeg", "-i", input_file,
            "-vf", f"drawtext=text='{watermark_text}':font=Verdana:fontcolor=white:fontsize=24:"
            f"x='mod(t*10,w)':y='mod(t*5,h)'",
            "-c:v", reencode_codec,
            *bitrate_option,
            "-g", "60",  # Keyframe alignment every 60 frames (1 sec at 60 FPS)
            "-bufsize", "10M",
            "-maxrate", f"{video_bitrate}k" if video_bitrate else "1M",
            "-preset", "fast",
            "-movflags", "+faststart",
            "-c:a", "copy",  # Copy audio without re-encoding
            output_file
        ]

        # Run FFmpeg command
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to add watermark: {e}")
