# YTDownloadWithWM
# **YouTube Download and Watermark Tool**

This project is a Python-based YouTube downloader and watermark tool that allows users to:
- Fetch and filter video formats based on resolution, FPS, and codec.
- Select the best video format and combine it with the best audio format.
- Download the selected content and optionally apply a watermark to the downloaded video.

---

## **Features**
- Fetch all available formats for a YouTube video URL.
- Automatically filter video formats using a structured approach:
  1. **Best Resolution**.
  2. **Best FPS** among the best resolution.
  3. **Best Codec** (prioritizing VP9 over AVC1) among the best FPS.
- Display all video options matching the best FPS and codec.
- Allow users to choose from the filtered options.
- Download and merge the selected video with the best audio.
- Add a watermark to the downloaded video (optional).

---

## **Logic Overview**

The tool determines the best video options in **3 major steps**:

1. **Best Resolution**:
   - Find all video formats with the **highest resolution** available.
   - Example: If 1920x1080 is the highest resolution, all formats with 1080p are selected.

2. **Best FPS**:
   - From the best resolution formats, select the format(s) with the **highest FPS** (frames per second).
   - Example: If 60 FPS is the highest among the 1080p formats, only those with 60 FPS are considered.

3. **Best Codec**:
   - Among the best resolution and FPS formats, prioritize codecs:
     - **VP9 (or VP09)** is preferred for better compression and quality.
     - If VP9 is unavailable, fall back to **AVC1**.
   - Example: If there are multiple 1080p/60 FPS formats, VP9 formats are chosen over AVC1.

### **Result**:
The tool filters all formats that match the **best FPS** and **best codec** properties. These filtered formats are displayed in a dropdown menu for the user to select.

---

## **Detailed Code Workflow**

The following steps outline the tool's workflow:

### **Step 1: Extract Video Information**
- Use `yt_dlp` to fetch all formats for a given YouTube URL.
- Separate the formats into:
  - **Audio-only formats**.
  - **Video-only formats**.

**Code Reference**: `extract_video_info(video_url)`

---

### **Step 2: Determine the Best Formats**

1. **Best Audio**:
   - Audio-only formats are filtered, and the one with the **highest bitrate (abr)** is chosen.
   - Example: Audio with 128 kbps is better than 64 kbps.

   **Code Reference**: `get_best_audio_format(formats)`

2. **Best Video**:
   - **Find Best Resolution**:
     - Identify the **highest resolution** (e.g., 1080p, 720p).
   - **Find Best FPS**:
     - Among the highest resolution formats, select the one(s) with the **highest FPS** (e.g., 60 FPS).
   - **Find Best Codec**:
     - Prioritize **VP9** (or VP09) over **AVC1** formats for better quality.

   **Code Reference**: `get_best_video_format(formats)`

---

### **Step 3: Filter Matching Video Options**
After identifying the best video format:
- Filter all video formats that share the same:
  - **FPS** as the best video.
  - **Codec** as the best video.
- Exclude formats without a known file size.

**Code Reference**: `filter_matching_video_formats(formats, best_video)`

**Example Filtering**:
| **Format**      | **Resolution** | **FPS** | **Codec** | **Filesize** |
|------------------|----------------|---------|-----------|-------------|
| Format A        | 1080p          | 60      | VP9       | 3 MB        |
| Format B        | 1080p          | 60      | AVC1      | 4 MB        |
| Format C        | 720p           | 30      | VP9       | 2 MB        |

**Result**: Only **Format A and B** are displayed, as they share the best **FPS** and **codec**.

---

### **Step 4: Download Selected Video and Best Audio**
- Users select one of the filtered video formats from a dropdown menu.
- The tool downloads:
  - The selected video format.
  - The best audio format.
- `yt_dlp` merges the video and audio into a single file.

**Code Reference**: `download_video(video_url, video_format_id, audio_format_id, output_path)`

---

### **Step 5: Add Watermark (Optional)**
- Users can add a watermark to the downloaded video using FFmpeg.
- The watermark text can be customized, and the watermark moves across the screen dynamically.

**Code Reference**: `select_and_add_watermark()` (from `watermark.py`)

---

## **Code Structure**

### **Files**
1. **`main.py`**:
   - Handles the user interface with Tkinter.
   - Allows users to fetch formats, select options, and download videos.
2. **`downloader.py`**:
   - Handles the backend logic:
     - Extracting formats.
     - Determining the best audio and video options.
     - Filtering matching formats.
     - Downloading content.
3. **`watermark.py`**:
   - Adds a watermark to the downloaded video using FFmpeg.

---

## **Requirements**

### **Dependencies**
- Python 3.x
- **yt_dlp**: For fetching formats and downloading content.
- **FFmpeg**: For adding watermarks.
- **Tkinter**: For the graphical user interface.

### **Installation**
Install dependencies using:
```bash
pip install yt-dlp

