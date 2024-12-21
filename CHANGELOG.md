# Changelog


## [2.0.6] - 2024-12-21
### Added
- Added support for hardware-accelerated gpu encoding
- Moved Version variable to a separate file

## [2.0.5] - 2024-12-20
### Added
- Added version display at the bottom of the window
- Organized global variables and constants section

## [2.0.4] - 2024-12-20
### Added
- Implemented universal loading animation system with customizable text
- Added visual feedback during URL processing with animated dots
### Changed
- Replaced global boolean flag with threading.Event for better animation control
- Improved thread safety in loading animations
### Fixed
- Fixed loading animation not stopping cleanly after operations complete

## [2.0.3] - 2024-12-20
### Added
- Implemented threading for the `fetch_best_formats_button` to improve GUI responsiveness.
- Ensured that the fetching operation runs in a separate thread without altering existing functionality.

## [2.0.2] - 2024-12-20
### Added
- Implemented threading for the `fetch_best_formats_button` to improve GUI responsiveness.
- Ensured that the fetching operation runs in a separate thread without altering existing functionality.

## [2.0.1] - 2024-12-20
### Added
- Implemented threading for the `fetch_best_formats_button` to improve GUI responsiveness.
- Ensured that the fetching operation runs in a separate thread without altering existing functionality.

## [2.0.0] - 2024-12-20
### Major UI Enhancements and Playlist Integration
- Increased initial window size for better usability.
- Integrated playlist view directly into the main window, improving user experience.
- Enhanced format selection and watermark options for each video in the playlist.
- Improved overall layout and scrolling functionality for better content management.
- Most functionalities are now fully operational, providing a seamless experience for users.

## [1.0.0] - 2024-06-16
### Added
- Initial release of the YouTube downloader and watermark tool.
- Added audio and video bitrate metadata to output files:
  - In general file metadata
  - In video stream metadata
  - In audio stream metadata
  - Custom title for both streams

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
- Improved main window layout
  - Increased initial window size to 1200x800
  - Integrated playlist view into main window instead of separate window
  - Better space utilization for playlist content