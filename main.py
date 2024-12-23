import tkinter as tk
from tkinter import filedialog, ttk
import threading
from downloader import extract_video_info, get_best_audio_format, get_best_video_format, filter_matching_video_formats, download_video, process_url
import os
import time
from version_variable import VERSION

# Global variables and constants
filtered_video_formats = None  # To store filtered video formats
format_vars = {}  # To store format variables for playlist videos
watermark_vars = {}  # To store watermark variables for playlist videos
video_selected_vars = {}  # To store video selection variables for playlist videos
stop_animation = threading.Event()  # Event to control loading animation

# Global variables for storing video format information
selected_format = None  # To store the selected video format
best_audio = None  # To store the best audio format

def validate_url(url):
    if not url:
        raise ValueError("Please enter a valid YouTube URL.")


def extract_formats(url):
    formats = extract_video_info(url)
    if not formats:
        raise RuntimeError("Failed to fetch formats.")
    return formats


def select_best_formats(formats):
    best_audio = get_best_audio_format(formats)
    best_video = get_best_video_format(formats)
    return best_audio, best_video


def filter_formats(formats, best_video):
    return filter_matching_video_formats(formats, best_video)


def fetch_best_formats():
    global best_audio, filtered_video_formats, selected_format
    url = input_url.get()
    
    try:
        validate_url(url)
        formats = extract_formats(url)
        best_audio, best_video = select_best_formats(formats)
        filtered_video_formats = filter_formats(formats, best_video)
    except Exception as e:
        label.config(text=f"⚠️ {str(e)}")
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
    print("Starting playlist download...")
    print(f"Format vars: {format_vars}")
    print(f"Watermark vars: {watermark_vars}")
    print(f"Video selected vars: {video_selected_vars}")
    
    def threaded_playlist_download():
        total_videos = len(format_vars)
        print(f"Total videos to download: {total_videos}")
        
        # Get download path
        download_path = filedialog.askdirectory(title="Select Playlist Download Folder")
        if not download_path:
            label.config(text="⚠️ Download cancelled.")
            return
        
        # Create a playlist directory with timestamp
        playlist_dir = os.path.join(download_path, "Videos")
        os.makedirs(playlist_dir, exist_ok=True)
        
        success_count = 0  # Initialize success counter
        
        for i, (video_url, format_var) in enumerate(format_vars.items(), 1):
            if not video_selected_vars[video_url].get():
                continue  # Skip if video is not selected
            
            selected_format_str = format_var['format_var'].get()
            # Extract format ID from the string (format is "format_note => ID: format_id, Res: resolution, FPS: fps, Size: filesize MB")
            format_id = selected_format_str.split("ID: ")[1].split(",")[0].strip() if "ID: " in selected_format_str else selected_format_str
            
            audio_format_id = format_var['audio_format_id']
            watermark = watermark_vars[video_url].get() if video_url in watermark_vars else False
            print(f"Downloading video {i}: {video_url}")
            print(f"Selected format ID: {format_id}")
            print(f"Audio format ID: {audio_format_id}")
            print(f"Watermark: {watermark}")
            
            # Update label to show which video is being downloaded
            label.config(text=f"Downloading video {i} of {total_videos}...")
            
            try:
                # Use existing download function's core logic
                download_success = download_video(video_url, format_id, audio_format_id, playlist_dir, watermark)
                
                if download_success:
                    success_count += 1  # Increment success count if download was successful
                
                # Update progress for this video
                progress_bar["value"] = (i / total_videos) * 100
                root.update_idletasks()
            except Exception as e:
                print(f"Error downloading video {i}: {str(e)}")
                label.config(text=f"Error downloading video {i}: {str(e)}")
                continue
        
        # Update final message based on success count
        if success_count == 0:
            label.config(text="⚠️ No videos were selected for download.")
        elif success_count == len([v for v in video_selected_vars.values() if v.get()]):
            label.config(text="✅ All selected videos downloaded! ✅", foreground='green', font=('Helvetica', 12, 'bold'))
        else:
            label.config(text=f"❌ Downloaded {success_count} out of {len([v for v in video_selected_vars.values() if v.get()])} selected videos. Try downloading later. ❌ ")
        progress_bar["value"] = 0
    
    # Reset progress bar
    progress_bar["value"] = 0
    
    # Start download in a new thread
    threading.Thread(target=threaded_playlist_download, daemon=True).start()

def expand_window_for_playlist(playlist_info):
    """
    Show playlist information and format selection in the main window
    """
    global format_vars, watermark_vars, video_selected_vars
    # Clear previous variables
    format_vars.clear()
    watermark_vars.clear()
    video_selected_vars.clear()
    
    # Clear any existing playlist frame
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Frame) and widget.winfo_name() == 'playlist_frame':
            widget.destroy()
    
    # Create main frame with scrollbar for playlist content
    playlist_frame = ttk.Frame(root, name='playlist_frame')
    playlist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Add canvas and scrollbar
    canvas = tk.Canvas(playlist_frame)
    scrollbar = ttk.Scrollbar(playlist_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack scrollbar components
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    # Add header
    header = ttk.Label(scrollable_frame, text=(f"Playlist Videos (Total: {len(playlist_info['videos'])})" if playlist_info['is_playlist'] else "Video Information"), font=('Helvetica', 12, 'bold'))
    header.pack(pady=10)
    
    # Dictionary to store format variables for each video
    format_vars = {}
    watermark_vars = {}  # Add dictionary for watermark variables
    video_selected_vars = {}  # Add dictionary for video selection variables
    
    # Add video entries
    for i, video in enumerate(playlist_info['videos'], 1):
        video_frame = ttk.LabelFrame(scrollable_frame, text=f"Video {i}")
        video_frame.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5)
        
        # Checkbox for video selection
        video_selected = tk.BooleanVar(value=True)  # Default to checked
        checkbox = ttk.Checkbutton(video_frame, text="Select for Download", variable=video_selected)
        checkbox.pack(anchor="w")
        
        # Store the video selection variable in a dictionary
        video_selected_vars[video['url']] = video_selected
        
        # Video title
        title_label = ttk.Label(video_frame, text=f"Title: {video['title']}", wraplength=700)
        title_label.pack(anchor="w")
        
        if video['status'] == 'ready' and video['formats']:
            # Format selection
            format_frame = ttk.Frame(video_frame)
            format_frame.pack(fill="x", pady=5)
            
            format_label = ttk.Label(format_frame, text="Format:")
            format_label.pack(side="left", padx=5)
            
            # Create format selection dropdown
            format_var = tk.StringVar()
            format_vars[video['url']] = {
                'format_var': format_var,
                'audio_format_id': get_best_audio_format(video['formats'])['format_id']
            }
            
            # Get best video format first to determine properties
            best_video = get_best_video_format(video['formats'])
            
            if best_video:
                # Get matching video formats based on best video properties
                matching_formats = filter_matching_video_formats(video['formats'], best_video)
                
                # Format the combo box values
                format_combo = ttk.Combobox(format_frame, textvariable=format_var, state="readonly", width=80)  # Made combobox wider
                format_combo['values'] = [
                    f"{fmt['format_note']} => ID: {fmt['format_id']}, Res: {fmt.get('resolution', 'N/A')}, FPS: {fmt.get('fps', 'N/A')}, Size: {fmt.get('filesize', 0) / 1024 / 1024:.2f} MB"
                    for fmt in matching_formats
                ]
                
                # Set default selection to first format
                if format_combo['values']:
                    format_combo.set(format_combo['values'][0])
            else:
                format_combo = ttk.Combobox(format_frame, textvariable=format_var, state="readonly", width=80)  # Made combobox wider
                format_combo['values'] = ["No suitable formats found"]
                
            format_combo.pack(side="left", padx=5)
            
            # Add watermark checkbox
            watermark_var = tk.BooleanVar(value=watermark_enabled.get())
            watermark_vars[video['url']] = watermark_var  # Store the watermark variable
            watermark_check = ttk.Checkbutton(format_frame, text="Add Watermark", variable=watermark_var, style='Switch.TCheckbutton')
            watermark_check.pack(side="left", padx=20)
        else:
            error_label = ttk.Label(video_frame, text=f"Status: {video['status']}", foreground="red")
            error_label.pack(anchor="w")
    
    # Download button
    download_button = tk.Button(scrollable_frame, text="Download Selected Videos", command=download_playlist_videos)
    download_button.pack(pady=10)

def check_url():
    url = input_url.get()
    if not url:
        return
    
    try:
        # Clear previous format selection
        for widget in format_frame.winfo_children():
            widget.destroy()
        
        # Process URL (could be video or playlist)
        result = process_url(url, "downloads", watermark=watermark_enabled.get())  # Pass watermark state
        
        expand_window_for_playlist(result)
        
    except Exception as e:
        label.config(text=f"Error: {str(e)}")

def animate_loading(label, animated_text):
    """Animate the loading dots."""
    while not stop_animation.is_set():
        for dots in ['', '.', '..', '...']:
            if stop_animation.is_set():
                break
            label.config(text=animated_text + dots)
            time.sleep(0.5)

def stop_animating_loading():
    """Stop the loading animation."""
    stop_animation.set()

def threaded_check_url():
    try:
        # Reset the stop event and disable button
        stop_animation.clear()
        fetch_best_formats_button.config(state=tk.DISABLED)
        
        # Start loading animation in a separate thread
        animation_thread = threading.Thread(target=animate_loading, args=(label, "Processing URL"), daemon=True)
        animation_thread.start()

        # Run the existing check_url function
        check_url()

    finally:
        # Stop the animation and update UI
        stop_animating_loading()
        label.config(text="Formats fetched successfully!")
        fetch_best_formats_button.config(state=tk.NORMAL)

# Create the Tkinter app window
root = tk.Tk()
root.title("YouTube Download and Watermark Tool")
root.geometry("1200x800")

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
fetch_best_formats_button = tk.Button(root, text="Fetch Best Video Formats", command=lambda: threading.Thread(target=threaded_check_url, daemon=True).start())
fetch_best_formats_button.pack(pady=10)

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

# Add version label next to copyright
version_label = tk.Label(root, text=VERSION, font=("Arial", 10), fg="gray")
version_label.pack(side=tk.BOTTOM, pady=5)

# Add a copyright label
copyright_label = tk.Label(root, text=" 2024 Limitless Media - Magid", font=("Arial", 10), fg="gray")
copyright_label.pack(side=tk.BOTTOM, pady=5)

# Run the Tkinter main loop
root.mainloop()
