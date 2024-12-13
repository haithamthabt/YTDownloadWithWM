from yt_dlp import YoutubeDL

def fetch_formats(url):
    """
    Fetches available formats for the given YouTube URL and returns a list of tuples.
    Each tuple contains the format ID and description.
    """
    try:
        ydl_opts_info = {'quiet': True}
        with YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
        
        formats = info.get('formats', [])
        format_options = [
            (fmt['format_id'], f"{fmt['format_note']} - {fmt['ext']} ({fmt.get('filesize', 'Unknown size')} bytes)")
            for fmt in formats if fmt.get('format_note') and fmt.get('filesize') is not None
        ]
        return format_options
    except Exception as e:
        return f"❌ Error fetching formats: {e}"

def download_video(url, format_id, output_path):
    """
    Downloads the selected format for the given YouTube URL.
    """
    if not url:
        return "⚠️ Please enter a valid YouTube URL."
    if not format_id:
        return "⚠️ Please select a format."
    if not output_path:
        return "⚠️ Please select an output folder."

    try:
        # Download the selected format
        ydl_opts_download = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'format': format_id
        }
        with YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([url])
        return f"✅ Video downloaded to: {output_path}"
    except Exception as e:
        return f"❌ Error: {e}"
