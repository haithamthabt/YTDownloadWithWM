from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL

def download_video(url):
    """
    Fetches available formats, prompts the user to select one, and downloads the video.
    """
    if not url:
        return "⚠️ Please enter a valid YouTube URL."

    try:
        # Fetch video information and formats
        ydl_opts_info = {'quiet': True}
        with YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
        
        # Get video details
        title = info.get('title', 'Unknown Title')
        resolution = info.get('format_note', 'Unknown Resolution')
        
        # Ask for confirmation
        confirm = messagebox.askyesno(
            "Confirm Download",
            f"Video: {title}\nResolution: {resolution}\n\nDo you want to download this video?"
        )
        if not confirm:
            return "Download canceled."

        # Ask for download folder
        output_path = filedialog.askdirectory(title="Select Download Folder")
        if not output_path:
            return "⚠️ No folder selected."

        # Download the video
        ydl_opts_download = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }
        with YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([url])
        return f"✅ Video downloaded to: {output_path}"
    except Exception as e:
        return f"❌ Error: {e}"
