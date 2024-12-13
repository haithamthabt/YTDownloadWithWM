from yt_dlp import YoutubeDL
from tkinter import filedialog

def download_video(url):
    """
    Downloads a YouTube video and saves it in the user-specified folder.
    """
    if not url:
        return "⚠️ Please enter a valid YouTube URL."
    
    output_path = filedialog.askdirectory(title="Select Download Folder")
    if not output_path:
        return "⚠️ No folder selected."
    
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"✅ Video downloaded to: {output_path}"
    except Exception as e:
        return f"❌ Error: {e}"
