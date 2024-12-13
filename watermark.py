import subprocess
from tkinter import filedialog

def add_watermark(input_file, output_file, text="LIMITLESS MEDIA"):
    """
    Adds a moving watermark to the input video and saves it as the output file.
    """
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"drawtext=text='{text}':font=Verdana:fontcolor=white:fontsize=36:x='mod(t*100,w)':y='mod(t*50,h)'",
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "veryfast",
        "-c:a", "copy",
        output_file
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to add watermark: {e}")

def select_and_add_watermark():
    """
    Opens file dialogs to let the user select an input video and choose a location to save the output video.
    Adds a watermark to the selected video.
    """
    input_file = filedialog.askopenfilename(title="Select Video File", filetypes=[("MP4 files", "*.mp4")])
    if not input_file:
        return "No file selected."

    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", title="Save Watermarked Video As", filetypes=[("MP4 files", "*.mp4")])
    if not output_file:
        return "No output location selected."

    try:
        add_watermark(input_file, output_file)
        return f"✅ Completed! Watermarked video saved as: {output_file}"
    except RuntimeError as e:
        return f"❌ {e}"
