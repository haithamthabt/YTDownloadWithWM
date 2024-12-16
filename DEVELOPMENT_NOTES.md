# YouTube Downloader with Watermark - Development Notes

## 1. Project Overview

This Python-based YouTube downloader and watermark tool enables users to:
- Download YouTube videos in their preferred quality
- Automatically select the best audio quality
- Apply customizable moving watermarks to videos
- Choose from available video formats based on resolution, FPS, and codec

## 2. Core Logic Flow

### 2.1 Step 1: Fetch All Available Formats
```python
def extract_video_info(video_url):
    with YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info.get('formats', [])
```
- Uses yt-dlp to fetch all available formats
- Returns list of formats with their properties (resolution, FPS, codec, etc.)

### 2.2 Step 2: Select Best Audio Format
```python
def get_best_audio_format(formats):
    audio_formats = [f for f in formats if f.get('acodec', 'none') != 'none' 
                    and f.get('vcodec', 'none') == 'none']
    best_audio = max(audio_formats, key=lambda f: f.get('abr', 0))
    return best_audio
```
- Filters audio-only formats
- Selects highest bitrate automatically
- Example: 128 kbps chosen over 64 kbps

### 2.3 Step 3: Determine Best Video Properties
First, we analyze all video formats to find the best possible properties:

1. **Find Best Resolution**
   ```python
   max_height = max(f.get('height', 0) for f in video_formats)
   highest_res_videos = [f for f in video_formats if f.get('height', 0) == max_height]
   ```
   - Identifies the highest available resolution
   - Example: 1080p if that's the maximum

2. **Find Best FPS**
   ```python
   max_fps = max(f.get('fps', 0) for f in highest_res_videos)
   highest_res_and_fps_videos = [f for f in highest_res_videos if f.get('fps', 0) == max_fps]
   ```
   - From highest resolution formats
   - Gets the highest frame rate
   - Example: 60 FPS if available

3. **Determine Best Codec**
   ```python
   if any(f.get('vcodec', '').lower().startswith("vp9") for f in highest_res_and_fps_videos):
       best_codec = "vp9"
   else:
       best_codec = "avc1"
   ```
   - From highest resolution/FPS formats
   - Prefers VP9 over AVC1
   - Example: VP9 if available at best resolution/FPS

### 2.4 Step 4: Filter Available Options
```python
def filter_matching_video_formats(formats, best_video):
    # Filter formats matching best video's properties
    matching_formats = [f for f in formats if (
        f.get('fps', 0) == best_video.get('fps', 0) and
        f.get('vcodec', '').startswith(best_video.get('vcodec', '')) and
        f.get('filesize', 0) > 0
    )]
    return matching_formats
```
- Uses best properties as reference
- Returns all formats matching these properties
- Example: If best is 1080p/60fps/VP9, might return:
  - Format 1: 1080p/60fps/VP9 (248MB)
  - Format 2: 1080p/60fps/VP9 (302MB)
  - Format 3: 1080p/60fps/VP9 (156MB)
  - Format 4: 1080p/60fps/VP9 (189MB)

### 2.5 Step 5: User Selection
- Display filtered formats to user
- Show relevant info (size, format ID, etc.)
- User selects preferred format

### 2.6 Step 6: Download and Merge
```python
def download_video(video_url, video_format_id, audio_format_id, output_path):
    # Download selected video format and best audio
    # Merge them using yt-dlp
```
- Downloads user's chosen video format
- Downloads best audio format
- Automatically merges streams
- Handles temporary files

### 2.7 Step 7: Apply Watermark
```python
def add_moving_watermark(input_file, output_file, watermark_text):
    # Use FFmpeg to add moving watermark
    # Preserve video quality
```
- Adds customizable moving text
- Uses FFmpeg for processing
- Maintains video quality

## 3. Implementation Details

### 3.1 Component Architecture
1. **GUI Layer** (`main.py`)
   - Tkinter-based interface
   - Threaded downloads for responsiveness

2. **Download Manager** (`downloader.py`)
   - Format selection logic
   - Download and merge operations

3. **Watermark Processor** (`watermark.py`)
   - FFmpeg integration
   - Watermark application

### 3.2 Dependencies
- **Core Requirements**
  - Python 3.x
  - yt-dlp: Video extraction and downloading
  - FFmpeg: Video processing and watermarking
  - Tkinter: GUI framework

- **Installation**
  ```bash
  pip install yt-dlp
  ```
  Note: FFmpeg must be installed separately on the system

## 4. Development Decisions

### 4.1 Why Separate Audio/Video?
- Better quality control
- More format options
- Quality customization

### 4.2 Why FFmpeg for Watermarks?
- Industry standard
- High performance
- Quality preservation

### 4.3 Why Threaded Downloads?
- UI responsiveness
- Progress tracking
- Better UX

## 5. Future Enhancements

1. **User Interface**
   - Watermark customization
   - Video preview
   - Progress visualization

2. **Functionality**
   - Playlist support
   - Batch processing
   - Download queue

3. **Technical**
   - Format presets
   - Error handling
   - Logging system
