import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
from downloader import extract_video_info, get_best_audio_format, get_best_video_format, filter_matching_video_formats, download_video, process_url
import os
import time

# Global variables for storing video format information
selected_format = None  # To store the selected video format
best_audio = None  # To store the best audio format
filtered_video_formats = None  # To store filtered video formats
format_vars = {}  # To store format variables for playlist videos
watermark_vars = {}  # To store watermark variables for playlist videos

def fetch_best_formats():
    """
    Fetches the best audio format and video options for the given YouTube URL.
    Displays the video options in a dropdown for user selection.
    """
    global best_audio, filtered_video_formats, selected_format
    url = input_url.get()
    if not url:
        label.config(text="⚠️ Please enter a valid YouTube URL.")
        return

    # Fetch formats
    formats = extract_video_info(url)
    if not formats:
        label.config(text="❌ Failed to fetch formats.")
        return

    # Get best audio and video
    best_audio = get_best_audio_format(formats)
    best_video = get_best_video_format(formats)

    # Filter matching video formats
    filtered_video_formats = filter_matching_video_formats(formats, best_video)

    if not filtered_video_formats:
        label.config(text="❌ No suitable video formats found.")
        return

    # Clear previous dropdown menu
    for widget in format_frame.winfo_children():
        widget.destroy()

    # Initialize selected_format if not already set
    if selected_format is None:
        selected_format = tk.StringVar()

    # Populate dropdown with matching video formats
    format_id_map = {
        f"{f['format_note']} => ID: {f['format_id']}, Res: {f.get('resolution', 'N/A')}, FPS: {f.get('fps', 'N/A')}, Size: {f.get('filesize', 0) / 1024 / 1024:.2f} MB": f['format_id']
        for f in filtered_video_formats
    }

    selected_format.set(list(format_id_map.keys())[0])  # Default to the first format
    dropdown = tk.OptionMenu(format_frame, selected_format, *format_id_map.keys())
    dropdown.pack()

    # Attach the format ID map to the dropdown for later retrieval
    dropdown.format_id_map = format_id_map
    label.config(text="Matching video formats fetched! Select one and click 'Download Video'.")

def handle_download():
    """
    Starts the download process in a separate thread to keep the GUI responsive.
    """
    url = input_url.get()
    if not url:
        label.config(text="⚠️ Please enter a valid YouTube URL.")
        return
    if not selected_format or not selected_format.get():
        label.config(text="⚠️ Please fetch formats and select a video option.")
        return
    if not best_audio:
        label.config(text="⚠️ Best audio format not found. Fetch formats again.")
        return

    # Retrieve the selected video format ID
    dropdown = format_frame.winfo_children()[0]  # Get the dropdown widget
    selected_description = selected_format.get()
    video_format_id = dropdown.format_id_map[selected_description]
    audio_format_id = best_audio['format_id']

    # Ask user to select output folder
    output_path = filedialog.askdirectory(title="Select Download Folder")
    if not output_path:
        label.config(text="⚠️ No folder selected.")
        return

    # Check if watermark is enabled
    add_watermark = watermark_enabled.get()

    # Progress update callback
    def progress_callback(progress):
        progress_bar['value'] = progress  # Update progress bar
        app.update_idletasks()

    # Threaded download function
    def threaded_download():
        progress_bar['value'] = 0  # Reset progress bar before download starts
        result = download_video(
            url, video_format_id, audio_format_id, output_path,
            watermark=add_watermark, progress_callback=progress_callback
        )
        label.config(text=result)
        progress_bar['value'] = 0  # Reset progress bar after completion

    # Start download in a new thread
    threading.Thread(target=threaded_download, daemon=True).start()

def download_playlist_videos():
    """
    Download all videos in the playlist with their selected formats and watermark settings
    """
    def threaded_download():
        # Get download path
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Create a playlist directory with timestamp
        playlist_dir = os.path.join(download_path, f"playlist_{int(time.time())}")
        os.makedirs(playlist_dir, exist_ok=True)
        
        # Create progress frame
        progress_frame = ttk.Frame(playlist_window)
        progress_frame.pack(pady=10, padx=10, fill='x')
        
        # Overall progress
        overall_label = ttk.Label(progress_frame, text="Overall Progress:")
        overall_label.pack(pady=(0, 5))
        
        overall_progress = ttk.Progressbar(progress_frame, mode='determinate', length=300)
        overall_progress.pack(fill='x')
        
        # Current video progress
        current_label = ttk.Label(progress_frame, text="Current Video Progress:")
        current_label.pack(pady=(10, 5))
        
        current_progress = ttk.Progressbar(progress_frame, mode='determinate', length=300)
        current_progress.pack(fill='x')
        
        status_label = ttk.Label(progress_frame, text="")
        status_label.pack(pady=5)

        total_videos = len(format_vars)
        completed_videos = 0

        def update_progress(d):
            if d['status'] == 'downloading':
                try:
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                    if total > 0:
                        percent = (downloaded / total) * 100
                        current_progress['value'] = percent
                        status_label.config(text=f"Downloading: {percent:.1f}% ({downloaded/1024/1024:.1f}MB / {total/1024/1024:.1f}MB)")
                        playlist_window.update_idletasks()
                except Exception as e:
                    print(f"Error updating progress: {e}")

        for i, (video_url, format_var) in enumerate(format_vars.items(), 1):
            # Reset current video progress
            current_progress['value'] = 0
            status_label.config(text=f"Starting video {i} of {total_videos}")
            
            # Get selected format
            selected_format_str = format_var['format_var'].get()
            format_id = selected_format_str.split("ID: ")[1].split(",")[0].strip() if "ID: " in selected_format_str else selected_format_str
            
            audio_format_id = format_var['audio_format_id']
            watermark = watermark_vars[video_url].get() if video_url in watermark_vars else False
            
            try:
                # Configure yt-dlp options with progress hooks
                ydl_opts = {
                    'progress_hooks': [update_progress],
                }
                
                # Download the video
                result = download_video(
                    video_url=video_url,
                    video_format_id=format_id,
                    audio_format_id=audio_format_id,
                    output_path=playlist_dir,
                    watermark=watermark,
                    watermark_text="LIMITLESS MEDIA",
                    ydl_opts=ydl_opts
                )
                completed_videos += 1
                
                # Update overall progress
                overall_progress['value'] = (completed_videos / total_videos) * 100
                status_label.config(text=f"Completed video {i} of {total_videos}")
                playlist_window.update_idletasks()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to download video {i}: {str(e)}")

        # Show completion message
        status_label.config(text=f"Download Complete! {completed_videos}/{total_videos} videos downloaded successfully")
        messagebox.showinfo("Download Complete", 
                          f"Successfully downloaded {completed_videos} out of {total_videos} videos!")

        # Clean up progress bars
        current_progress['value'] = 0
        overall_progress['value'] = 0

    # Start download in a new thread
    threading.Thread(target=threaded_download, daemon=True).start()

def show_playlist_window(playlist_info):
    """
    Show a new window with playlist information and format selection
    """
    global playlist_window, format_vars, watermark_vars
    
    # Create new window
    playlist_window = tk.Toplevel(root)
    playlist_window.title("Playlist Download")
    playlist_window.geometry("600x800")
    
    # Create main frame with scrollbar
    main_frame = ttk.Frame(playlist_window)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Add canvas and scrollbar
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack scrollbar and canvas
    scrollbar.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    
    # Clear previous variables
    format_vars.clear()
    watermark_vars.clear()
    
    # Add videos to scrollable frame
    for video in playlist_info.get('videos', []):
        video_url = video.get('url', '')
        if not video_url:
            continue
            
        # Create frame for this video
        video_frame = ttk.Frame(scrollable_frame)
        video_frame.pack(fill='x', padx=5, pady=5)
        
        # Add video title
        title_label = ttk.Label(video_frame, text=video.get('title', 'Unknown Title'), wraplength=500)
        title_label.pack(fill='x')
        
        try:
            # Get formats for this video
            formats = extract_video_info(video_url)
            if not formats:
                continue
                
            # Get best formats
            best_video = get_best_video_format(formats)
            best_audio = get_best_audio_format(formats)
            filtered_formats = filter_matching_video_formats(formats, best_video)
            
            if not filtered_formats:
                continue
                
            # Create format selection dropdown
            format_var = tk.StringVar()
            format_vars[video_url] = {
                'format_var': format_var,
                'audio_format_id': best_audio['format_id']
            }
            
            # Create format options
            format_options = [
                f"{f['format_note']} => ID: {f['format_id']}, Res: {f.get('resolution', 'N/A')}, "
                f"FPS: {f.get('fps', 'N/A')}, Size: {f.get('filesize', 0)/1024/1024:.2f} MB"
                for f in filtered_formats
            ]
            
            if format_options:
                format_var.set(format_options[0])
                format_dropdown = ttk.OptionMenu(video_frame, format_var, format_options[0], *format_options)
                format_dropdown.pack(fill='x', pady=2)
                
                # Add watermark checkbox
                watermark_var = tk.BooleanVar(value=watermark_enabled.get())  # Sync with main window
                watermark_vars[video_url] = watermark_var
                watermark_check = ttk.Checkbutton(video_frame, text="Add Watermark", variable=watermark_var)
                watermark_check.pack(pady=2)
                
        except Exception as e:
            error_label = ttk.Label(video_frame, text=f"Error loading formats: {str(e)}", foreground='red')
            error_label.pack()
    
    # Add download button at the bottom
    download_button = ttk.Button(playlist_window, text="Download All", command=download_playlist_videos)
    download_button.pack(pady=10)

def check_url():
    url = input_url.get()
    if not url:
        return
    
    try:
        # Clear previous format selection
        for widget in format_frame.winfo_children():
            widget.destroy()
        label.config(text="Processing URL...")
        
        # Process URL (could be video or playlist)
        result = process_url(url, "downloads", watermark=watermark_enabled.get())  # Pass watermark state
        
        if result['is_playlist']:
            # Show playlist window
            show_playlist_window(result)
        else:
            # Single video - use existing format display
            video = result['videos'][0]
            if video['status'] == 'ready' and video['formats']:
                # Initialize selected_format if not already set
                global selected_format
                if selected_format is None:
                    selected_format = tk.StringVar()

                # Populate dropdown with matching video formats
                format_id_map = {
                    f"{f['format_note']} => ID: {f['format_id']}, Res: {f.get('resolution', 'N/A')}, FPS: {f.get('fps', 'N/A')}, Size: {f.get('filesize', 0) / 1024 / 1024:.2f} MB": f['format_id']
                    for f in video['formats']
                }

                selected_format.set(list(format_id_map.keys())[0])  # Default to the first format
                dropdown = tk.OptionMenu(format_frame, selected_format, *format_id_map.keys())
                dropdown.pack()

                # Attach the format ID map to the dropdown for later retrieval
                dropdown.format_id_map = format_id_map
                label.config(text="Matching video formats fetched! Select one and click 'Download Video'.")
            else:
                label.config(text=f"Error: {video['status']}")
    
    except Exception as e:
        label.config(text=f"Error: {str(e)}")

# Create the Tkinter app window
root = tk.Tk()
root.title("YouTube Download and Watermark Tool")
root.geometry("500x600")

# Add a label for app title and status messages
label = tk.Label(root, text="YouTube Video Downloader and Watermarker", wraplength=450)
label.pack(pady=20)

# Add input field for YouTube URL
input_label = tk.Label(root, text="YouTube URL:")
input_label.pack(pady=5)

input_url = tk.Entry(root, width=50)
input_url.insert(0, "https://www.youtube.com/playlist?list=PLHc88y3ww4WCWc4kcXdQkEyo7zoGj7_uh")
input_url.pack(pady=5)

# Add buttons for fetching formats and downloading
fetch_best_formats_button = tk.Button(root, text="Fetch Best Video Formats", command=check_url)
fetch_best_formats_button.pack(pady=10)

download_button = tk.Button(root, text="Download YouTube Video", command=handle_download)
download_button.pack(pady=10)

# Add watermark checkbox
watermark_enabled = tk.BooleanVar(value=True)  # Checked by default
watermark_checkbox = tk.Checkbutton(root, text="Add Watermark", variable=watermark_enabled)
watermark_checkbox.pack(pady=5)

# Add a frame for the format dropdown
format_frame = tk.Frame(root)
format_frame.pack(pady=10)

# Add a progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Add a copyright label
copyright_label = tk.Label(root, text=" 2024 Limitless Media", font=("Arial", 10), fg="gray")
copyright_label.pack(side=tk.BOTTOM, pady=5)

# Run the Tkinter main loop
root.mainloop()
