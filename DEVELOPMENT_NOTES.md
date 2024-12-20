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

## 3. UI Design and Implementation

### 3.1 Main Window Layout
- Initial window size set to 1200x800 for optimal content display
- Top section contains:
  - URL input field
  - Format selection for single videos
  - Watermark toggle
  - Download button
- Bottom section (playlist view) dynamically shows:
  - List of videos in scrollable frame
  - Individual format selections per video
  - Individual watermark toggles
  - Playlist download button

### 3.2 Playlist Integration
```python
def expand_window_for_playlist(playlist_info):
    """
    Expands main window to display playlist information and format selection
    Key features:
    - Cleans up existing playlist frame if present
    - Creates scrollable frame for video list
    - Adds format selection and watermark toggle per video
    - Maintains consistent UI with single video display
    """
```

### 3.3 UI Components
1. **Scrollable Frame Implementation**
   - Canvas with scrollbar for smooth navigation
   - Dynamic content sizing based on video count
   - Proper cleanup of previous content

2. **Format Selection**
   - Combobox with detailed format information
   - Shows resolution, FPS, and file size
   - Consistent width for better readability

3. **Progress Tracking**
   - Overall progress bar for playlist downloads
   - Status updates in main label
   - Clear feedback for ongoing operations

## 4. Implementation Details

### 4.1 Component Architecture
1. **GUI Layer** (`main.py`)
   - Tkinter-based interface
   - Threaded downloads for responsiveness

2. **Download Manager** (`downloader.py`)
   - Format selection logic
   - Download and merge operations

3. **Watermark Processor** (`watermark.py`)
   - FFmpeg integration
   - Watermark application

### 4.2 Dependencies
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

## 5. Development Decisions

### 5.1 Why Separate Audio/Video?
- Better quality control
- More format options
- Quality customization

### 5.2 Why FFmpeg for Watermarks?
- Industry standard
- High performance
- Quality preservation

### 5.3 Why Threaded Downloads?
- UI responsiveness
- Progress tracking
- Better UX

## 6. Future Enhancements

1. **User Interface**
   - Watermark customization
   - Video preview
   - Progress visualization

2. **Functionality**
   - Batch processing
   - Download queue

3. **Technical**
   - Format presets
   - Error handling
   - Logging system

## 7. Playlist Implementation Details

### 7.1 Detecting Playlists
- Check if URL is a playlist
- Extract all video URLs from playlist

### 7.2 Playlist GUI
- Create scrollable window showing:
  - Video titles
  - Format selection dropdown (matching single video quality)
  - Watermark toggle (synced with main window)

### 7.3 Downloading Playlists
- Download each video with selected format
- Apply watermark based on individual toggles
- Show progress for overall playlist

### 7.4 Format Selection for Playlists
- Uses yt-dlp to get available formats
- Filters to show best quality options:
  1. Highest resolution
  2. Best FPS
  3. Preferred codec (VP9 > AVC1)
- Shows detailed format info:
  - Resolution
  - FPS
  - File size
  - Format ID

### 7.5 Watermarking for Playlists
- Uses OpenCV for video processing
- Adds moving watermark text
- Configurable text and movement

## 8. Updated Development Notes

### 8.1 Project Structure
- `main.py`: Main GUI application using tkinter
- `downloader.py`: YouTube video downloading functionality using yt-dlp
- `watermark.py`: Video watermarking functionality

### 8.2 Features
- Download YouTube videos with format selection
- Add watermark to downloaded videos
- Full playlist support
  - Shows list of videos in playlist
  - Format selection per video
  - Watermark toggle per video
  - Downloads videos with selected settings
  - Creates timestamped playlist folders

### 8.3 Implementation Details

#### 8.3.1 Video Download Process
1. Extract video information using yt-dlp
2. Filter and present best quality formats
3. Download selected format
4. Add watermark if enabled

#### 8.3.2 Playlist Implementation
1. Detect if URL is a playlist
2. Extract all video URLs from playlist
3. Create scrollable window showing:
   - Video titles
   - Format selection dropdown (matching single video quality)
   - Watermark toggle (synced with main window)
4. Download functionality:
   - Downloads each video with selected format
   - Applies watermark based on individual toggles
   - Shows progress for overall playlist
   - Creates timestamped folder for playlist videos

#### 8.3.3 Format Selection
- Uses yt-dlp to get available formats
- Filters to show best quality options:
  1. Highest resolution
  2. Best FPS
  3. Preferred codec (VP9 > AVC1)
- Shows detailed format info:
  - Resolution
  - FPS
  - File size
  - Format ID

#### 8.3.4 Watermarking
- Uses OpenCV for video processing
- Adds moving watermark text
- Configurable text and movement

## 9. Future Improvements

### Playlist Enhancements

#### 1. User Interface
- Add folder name input field
  - Default to playlist title
  - Allow custom naming
  - Add timestamp option toggle
- Add location selection button
  - Remember last used location
  - Show current selected path
- Add download controls
  - Cancel button for ongoing downloads
  - Pause/Resume functionality
  - Select all/none for watermarks
- Improve progress display
  - Individual progress bars per video
  - Overall playlist progress
  - Download speed indicator
  - Time remaining estimation
  - Current video X of Y indicator

#### 2. Download Management
- Implement download queue system
  - Allow adding multiple playlists
  - Show queue status
  - Allow reordering queue
- Add error handling
  - Retry failed downloads
  - Skip option for problematic videos
  - Log errors for debugging
- Add download resumption
  - Save download state
  - Resume interrupted downloads
  - Handle network interruptions

#### 3. Settings and Preferences
- Save user preferences
  - Default download location
  - Default watermark settings
  - Format selection preferences
- Add playlist presets
  - Save format selections
  - Quick load previous settings
  - Batch apply settings

#### 4. Notifications
- Add system notifications
  - Download start/completion
  - Error notifications
  - Progress milestones
- Add in-app notifications
  - Status messages
  - Error reporting
  - Success confirmations

#### 5. Performance Optimization
- Implement concurrent downloads
  - Configurable number of simultaneous downloads
  - Bandwidth management
  - Progress tracking for parallel downloads
- Optimize memory usage
  - Clean up temporary files
  - Manage large playlists efficiently
