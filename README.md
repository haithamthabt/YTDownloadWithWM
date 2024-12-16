# YouTube Download and Watermark Tool

A Python-based desktop application that allows you to download YouTube videos with the best available quality and optionally add a moving watermark.

## Features
- Download YouTube videos in the highest quality
- Smart format selection based on resolution, FPS, and codec
- Automatic best audio quality selection
- Optional moving watermark
- User-friendly GUI interface

## Requirements
- Python 3.x
- FFmpeg
- yt-dlp
- Tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/YTDownloadWithWM.git
cd YTDownloadWithWM
```

2. Install Python dependencies:
```bash
pip install yt-dlp
```

3. Install FFmpeg:
- **macOS** (using Homebrew):
  ```bash
  brew install ffmpeg
  ```
- **Windows**: Download from [FFmpeg official website](https://ffmpeg.org/download.html)
- **Linux**:
  ```bash
  sudo apt-get install ffmpeg  # Ubuntu/Debian
  sudo dnf install ffmpeg      # Fedora
  ```

## Usage

1. Run the application:
```bash
python main.py
```

2. Enter a YouTube URL in the input field
3. Click "Fetch Best Video Formats" to see available options
4. Select your preferred format from the dropdown
5. Choose whether to add a watermark
6. Click "Download YouTube Video" and select the output folder

## How It Works

### Video Format Selection
1. **Resolution**: Finds formats with the highest available resolution
2. **FPS**: Among the best resolution, selects formats with the highest FPS
3. **Codec**: Prioritizes VP9 over AVC1 for better quality

### Audio Selection
- Automatically selects the audio format with the highest bitrate
- Merges with the selected video format during download

### Watermarking
- Uses FFmpeg to add a moving text watermark
- Preserves video quality while adding the watermark
- Optimized encoding settings for best quality/size ratio

## Project Structure

```
YTDownloadWithWM/
├── main.py          # GUI and main application logic
├── downloader.py    # YouTube download functionality
└── watermark.py     # FFmpeg watermarking implementation
```

### Components

#### main.py
- Tkinter-based GUI interface
- Handles user interactions and display
- Manages the download workflow

#### downloader.py
- YouTube video information extraction
- Format filtering and selection
- Download and merge functionality

#### watermark.py
- FFmpeg-based video processing
- Moving watermark implementation
- Video encoding optimization

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Credits
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube download functionality
- [FFmpeg](https://ffmpeg.org/) for video processing
