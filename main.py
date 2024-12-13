import tkinter as tk
from downloader import fetch_formats, download_video
from watermark import select_and_add_watermark
from tkinter import filedialog

selected_format = None  # To store the selected format ID from the dropdown


def handle_watermark():
    """
    Handles the watermarking process by calling the select_and_add_watermark function.
    """
    result = select_and_add_watermark()
    label.config(text=result)


def handle_download():
    """
    Handles the video downloading process by calling the download_video function.
    """
    url = input_url.get()
    if not selected_format or not selected_format.get():
        label.config(text="⚠️ Please fetch formats and select one first.")
        return
    format_id = selected_format.get()  # Fetch the selected format ID
    output_path = filedialog.askdirectory(title="Select Download Folder")
    if not output_path:
        label.config(text="⚠️ No folder selected.")
        return

    result = download_video(url, format_id, output_path)
    label.config(text=result)


def fetch_example_formats():
    """
    Fetches available formats for a default example URL and displays them in a dropdown menu.
    """
    global selected_format
    default_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with your example URL
    formats = fetch_formats(default_url)
    if isinstance(formats, str):  # If an error message is returned
        label.config(text=formats)
        return

    # Clear previous dropdown menu
    for widget in format_frame.winfo_children():
        widget.destroy()

    # Add dropdown for example formats
    format_ids = [fmt[0] for fmt in formats]  # Extract format IDs
    format_descriptions = [f"{fmt[1]} (ID: {fmt[0]})" for fmt in formats]  # Create descriptions
    selected_format = tk.StringVar(value=format_ids[0])  # Default to the first format ID
    dropdown = tk.OptionMenu(format_frame, selected_format, *format_ids)
    dropdown.pack()
    label.config(text="Example formats fetched! Select a format and click 'Download Example'.")


def handle_example_download():
    """
    Downloads the selected format for the default example URL.
    """
    global selected_format
    default_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with your example URL
    if not selected_format or not selected_format.get():
        label.config(text="⚠️ Please fetch example formats and select one first.")
        return

    format_id = selected_format.get()  # Fetch the selected format ID
    output_path = filedialog.askdirectory(title="Select Download Folder")
    if not output_path:
        label.config(text="⚠️ No folder selected.")
        return

    result = download_video(default_url, format_id, output_path)
    label.config(text=result)


def fetch_and_display_formats():
    """
    Fetches available formats for the URL entered by the user and displays them in a dropdown menu.
    """
    global selected_format
    url = input_url.get()
    formats = fetch_formats(url)
    if isinstance(formats, str):  # If an error message is returned
        label.config(text=formats)
        return

    # Clear previous dropdown menu
    for widget in format_frame.winfo_children():
        widget.destroy()

    # Add dropdown for user-provided formats
    format_ids = [fmt[0] for fmt in formats]  # Extract format IDs
    format_descriptions = [f"{fmt[1]} (ID: {fmt[0]})" for fmt in formats]  # Create descriptions
    selected_format = tk.StringVar(value=format_ids[0])  # Default to the first format ID
    dropdown = tk.OptionMenu(format_frame, selected_format, *format_ids)
    dropdown.pack()
    label.config(text="Formats fetched! Select a format and click 'Download YouTube Video'.")


# Create the Tkinter app window
app = tk.Tk()
app.title("YouTube Download and Watermark Tool")
app.geometry("500x450")

# Add a label
label = tk.Label(app, text="YouTube Video Downloader and Watermarker", wraplength=450)
label.pack(pady=20)

# Add input field for YouTube URL
input_label = tk.Label(app, text="YouTube URL:")
input_label.pack(pady=5)

input_url = tk.Entry(app, width=50)
input_url.pack(pady=5)

# Add buttons for fetching formats and downloading
fetch_formats_button = tk.Button(app, text="Fetch Formats", command=fetch_and_display_formats)
fetch_formats_button.pack(pady=10)

download_button = tk.Button(app, text="Download YouTube Video", command=handle_download)
download_button.pack(pady=10)

fetch_example_button = tk.Button(app, text="Fetch Example Formats", command=fetch_example_formats)
fetch_example_button.pack(pady=10)

example_download_button = tk.Button(app, text="Download Example", command=handle_example_download)
example_download_button.pack(pady=10)

watermark_button = tk.Button(app, text="Add Watermark to Video", command=handle_watermark)
watermark_button.pack(pady=10)

# Add a frame for the format dropdown
format_frame = tk.Frame(app)
format_frame.pack(pady=10)

# Add a copyright label
copyright_label = tk.Label(app, text="© 2024 Limitless Media", font=("Arial", 10), fg="gray")
copyright_label.pack(side=tk.BOTTOM, pady=5)

# Run the Tkinter main loop
app.mainloop()
