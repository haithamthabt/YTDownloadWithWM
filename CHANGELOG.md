# Changelog

## [1.0.0] - 2024-06-16
### Added
- Initial release of the YouTube downloader and watermark tool.
- Added audio and video bitrate metadata to output files:
  - In general file metadata
  - In video stream metadata
  - In audio stream metadata
  - Custom title for both streams

### TODO
- make sure of quality that is lossless
- add progress bar for watermarking

## [Unreleased]

### Added
- Complete playlist functionality implementation
  - Added playlist detection and video listing
  - Created playlist window with scrollable interface
  - Added format selection dropdowns for each video
  - Added watermark toggle option for each video (syncs with main window)
  - Improved format display with resolution, FPS, and file size
  - Implemented playlist download with selected formats and watermark options
  - Videos are downloaded to a timestamped playlist folder

### Changed
- Enhanced UI for playlist view
  - Made format dropdowns wider for better readability
  - Added proper scrolling for multiple videos
  - Organized format options to match single video display
  - Added progress tracking for playlist downloads

### TODO
- Playlist Improvements:
  - Add custom naming for playlist folders
  - Add location selection for playlist downloads
  - Improve progress tracking for individual videos
  - Add completion notifications
  - Add option to cancel downloads
  - Show estimated time remaining
  - Show download speed
  - Add option to select all/none for watermarks
  - Remember last used settings
  - Add error recovery for failed downloads
- make sure of quality that is lossless
- add progress bar for watermarking
- Progress tracking for multiple video downloads

#### Suggestions for Improvement
- Code Organization: Consider breaking down larger functions into smaller, more manageable ones. For example, the download_playlist_videos function could be split into separate functions for downloading individual videos and updating the UI.
- Error Handling: While there is some error handling in place, you might want to add more specific error messages or logging to help diagnose issues during downloads.
- Input Validation: Ensure that the input URL is validated more thoroughly before attempting to fetch formats. This could include checking for valid URL formats.
- Documentation: Adding docstrings to all functions would improve code readability and provide context for future developers (or yourself) revisiting the code.
- User Feedback: Consider providing more feedback to the user during long operations, such as displaying a loading spinner or disabling buttons while processing.