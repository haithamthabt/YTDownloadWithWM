import tkinter as tk
from tkinter import filedialog
from downloader import extract_video_info, get_best_audio_format, get_best_video_format, filter_matching_video_formats, download_video

# Global variables
selected_format = None  # To store the selected video format

def handle_watermark():
    """
    Handles the watermarking process by calling the select_and_add_watermark function.
    """
    result = select_and_add_watermark()
    label.config(text=result)


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

    # Populate dropdown with matching video formats
    format_descriptions = [
        f"{f['format_note']},ID: {f['format_id']}, Res: {f.get('resolution', 'N/A')}, FPS: {f.get('fps', 'N/A')}, Size: {f.get('filesize', 0) / 1024 / 1024:.2f} MB"
        for f in filtered_video_formats
    ]
    format_ids = [f['format_id'] for f in filtered_video_formats]

    # Streamlined description-to-format mapping
    selected_format = tk.StringVar(value=None)

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
    Downloads the selected video format and best audio format.
    Adds watermark if the checkbox is enabled.
    """
    global best_audio, filtered_video_formats
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

    # Call the updated download function
    result = download_video(url, video_format_id, audio_format_id, output_path, watermark=add_watermark)
    label.config(text=result)




# Create the Tkinter app window
app = tk.Tk()
app.title("YouTube Download and Watermark Tool")
app.geometry("500x550")

# Add a label
label = tk.Label(app, text="YouTube Video Downloader and Watermarker", wraplength=450)
label.pack(pady=20)

# Add input field for YouTube URL
input_label = tk.Label(app, text="YouTube URL:")
input_label.pack(pady=5)

input_url = tk.Entry(app, width=50)
input_url.pack(pady=5)

# Add buttons for fetching formats and downloading
fetch_best_formats_button = tk.Button(app, text="Fetch Best Video Formats", command=fetch_best_formats)
fetch_best_formats_button.pack(pady=10)

download_button = tk.Button(app, text="Download YouTube Video", command=handle_download)
download_button.pack(pady=10)

# Variable to store watermark check state
watermark_enabled = tk.BooleanVar(value=True)  # Checked by default

# Checkbutton for watermark option
watermark_checkbutton = tk.Checkbutton(app, text="Add Watermark", variable=watermark_enabled)
watermark_checkbutton.pack(pady=5)


# Add a frame for the format dropdown
format_frame = tk.Frame(app)
format_frame.pack(pady=10)

# Add a copyright label
copyright_label = tk.Label(app, text="© 2024 Limitless Media", font=("Arial", 10), fg="gray")
copyright_label.pack(side=tk.BOTTOM, pady=5)

# Run the Tkinter main loop
app.mainloop()
