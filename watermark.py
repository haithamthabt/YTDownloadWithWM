import subprocess

def add_moving_watermark(input_file, output_file, watermark_text, video_codec="libx264", video_bitrate=None):
    """
    Adds a moving watermark to the input video using FFmpeg and saves it to the output file.
    
    Args:
        input_file (str): Path to the input video file
        output_file (str): Path where the watermarked video will be saved
        watermark_text (str): Text to be used as watermark
        video_codec (str): Video codec to use for encoding (default: "libx264")
        video_bitrate (int, optional): Video bitrate in kbps. If None, uses CRF mode
    
    Raises:
        RuntimeError: If FFmpeg fails to add the watermark
    """
    try:
        # Determine the codec based on input format
        # Use VP9 for WebM/VP9 inputs, H.264 for others
        reencode_codec = "libvpx-vp9" if video_codec.lower().startswith("vp") else "libx264"
        
        # Set quality control: either bitrate or CRF (Constant Rate Factor)
        bitrate_option = ["-b:v", f"{video_bitrate}k"] if video_bitrate else ["-crf", "22"]

        # Build FFmpeg command with optimized settings
        command = [
            "ffmpeg", 
            "-i", input_file,
            # Watermark filter with moving text
            "-vf", f"drawtext=text='{watermark_text}':font=Verdana:fontcolor=white:fontsize=24:"
                  f"x='mod(t*0.5,w)':y='mod(t*0.2,h)'",
            # Video encoding settings
            "-c:v", reencode_codec,
            *bitrate_option,
            "-g", "60",              # Keyframe interval (1 sec at 60 FPS)
            "-bufsize", "10M",       # Buffer size for rate control
            "-maxrate", f"{video_bitrate}k" if video_bitrate else "1M",
            "-c:a", "copy",          # Copy audio stream without re-encoding
            "-map_metadata", "0",    # Copy global metadata
            "-map_chapters", "0",    # Copy chapters
            output_file
        ]

        # Execute FFmpeg command
        subprocess.run(command, check=True)
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to add watermark: {e}")
