import tkinter as tk
from watermark import select_and_add_watermark
from downloader import download_video

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
    result = download_video(input_url.get())
    label.config(text=result)

def handle_example_download():
    """
    Downloads a video using a default example URL.
    """
    default_url = "https://youtu.be/wpJnigMKFmQ?feature=shared"  # Replace with your example URL
    result = download_video(default_url)
    label.config(text=result)

# Create the Tkinter app window
app = tk.Tk()
app.title("YouTube Download and Watermark Tool")
app.geometry("500x300")

# Add a label
label = tk.Label(app, text="YouTube Video Downloader and Watermarker", wraplength=450)
label.pack(pady=20)

example_button = tk.Button(app, text="Download Example", command=handle_example_download)
example_button.pack(pady=10)

# Add input field for YouTube URL
input_label = tk.Label(app, text="YouTube URL:")
input_label.pack(pady=5)

input_url = tk.Entry(app, width=50)
input_url.pack(pady=5)

# Add buttons for downloading and watermarking
download_button = tk.Button(app, text="Download YouTube Video", command=handle_download)
download_button.pack(pady=10)

watermark_button = tk.Button(app, text="Add Watermark to Video", command=handle_watermark)
watermark_button.pack(pady=10)

# Add a copyright label
copyright_label = tk.Label(app, text="© 2024 Limitless Media", font=("Arial", 10), fg="gray")
copyright_label.pack(side=tk.BOTTOM, pady=5)

# Run the Tkinter main loop
app.mainloop()
