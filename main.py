import tkinter as tk
from tkinter import filedialog
import subprocess
import os

def add_moving_watermark():
    video_file = filedialog.askopenfilename(title="Select Video File", filetypes=[("MP4 files", "*.mp4")])
    if video_file:
        output_file = os.path.splitext(video_file)[0] + "_moving_watermarked.mp4"
        
        command = [
            "ffmpeg",
            "-i", video_file,
            "-vf", "drawtext=text='LIMITLESS MEDIA':font=Verdana:fontcolor=white:fontsize=36:x='mod(t*100,w)':y='mod(t*50,h)'",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "veryfast",
            "-c:a", "copy",
            output_file
        ]
        try:
            subprocess.run(command, check=True)
            label.config(text=f"✅ Completed! Moving watermark video saved as:\n{output_file}")
        except subprocess.CalledProcessError as e:
            label.config(text="❌ Error adding watermark. Make sure FFmpeg is installed.")
    else:
        label.config(text="⚠️ No file selected.")

# Create the Tkinter app window
app = tk.Tk()
app.title("Watermark Tool")
app.geometry("500x250")

# Add a label
label = tk.Label(app, text="Add Moving Watermark with Verdana Font", wraplength=450)
label.pack(pady=20)

# Add a button to select video and apply watermark
button = tk.Button(app, text="Select Video and Add Moving Watermark", command=add_moving_watermark)
button.pack(pady=10)

# Add a copyright label at the bottom
copyright_label = tk.Label(app, text="© Limitless Media 2024", font=("Arial", 10), fg="gray")
copyright_label.pack(side="bottom", pady=10)  # Positioned at the bottom with padding


# Run the Tkinter main loop
app.mainloop()
