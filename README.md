

<h1 align="center">MultiThreadedYT-Sync</h1>
<h3 align="center">
  <b>Advanced YouTube Playlist Downloader implementing Multithreading</b>
</h3>

<p align="center">
  ![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-v3.7+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>


## Overview:

`MultiThreadedYT-Sync` is a powerful Command-Line Interface (CLI) application for downloading YouTube playlists with unprecedented speed and efficiency. Leveraging Python's multithreading capabilities, this tool revolutionizes the process of acquiring large video collections.This application is designed to significantly accelerate the process of acquiring large video collections while providing a rich, interactive console interface.

## Key Features:

- **Concurrent Downloads**: Utilizes Python's threading module to download multiple videos simultaneously.
- **Adaptive Quality Selection**: Supports various video qualities (360p, 720p, 1080p) with automatic fallback to the highest available quality.
- **Format Flexibility**: Offers both video (MP4) and audio-only (MP3) download options.
- **Subtitle Integration**: Option to download video subtitles (if available) in SRT Format alongside the main content.
- **Rich Console Interface**: Implements the `rich` library for an enhanced, colorful command-line experience.
- **Real-time Progress Tracking**: Displays download progress, speed, and estimated time remaining for each video.
- **Robust Error Handling**: Implements retry mechanisms and comprehensive logging for troubleshooting.
- **Customizable Output**: Allows users to specify custom output directories and filename patterns.
- **Detailed Logging Facility**: Maintains a log file for troubleshooting and tracking download history.
- **Input Validation** : Checks for valid YouTube playlist URLs and ensures the output directory exists or can be created.
- **Informative Feedback** : Provides real-time updates on download progress, including download speed and completion status for each video.


## How It Works:

- The application starts by displaying an attractive ASCII art banner.
- It prompts the user for a YouTube playlist URL and validates the input.
- Users can specify the output directory, desired format (video or audio), video quality, and whether to download subtitles.
- The application then fetches the playlist information and initiates concurrent downloads of the videos.
- A progress bar and status updates are displayed for each video and the overall playlist download.
- Upon completion, a summary of the download session is presented.
- Users can choose to download another playlist or exit the application.

## Technical Highlights:

- Concurrent Processing: Uses ThreadPoolExecutor for efficient parallel downloads.
- YouTube Integration: Leverages the pytube library for interacting with YouTube and downloading content.
- Rich UI Components: Utilizes various rich library components like Progress, Panel, Table, and Live for a dynamic and informative CLI.
- Resource Management: Implements proper exception handling and resource cleanup to ensure smooth operation even in case of errors.

## Prerequisites:

- Python 3.7+
- pip (Python package manager)

## Installation:

1. Clone the repository:
   ```
   git clone https://github.com/NayakSubhransu/MultiThreadedYT-Sync.git
   cd MultiThreaded-Tube
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage:

Run the script with the following command:

```
python MultiThreadedYT-Sync.py
```

Follow the interactive prompts to:
1. Enter the YouTube playlist URL
2. Specify the output directory
3. Select download format (MP4/MP3) and video quality
4. Choose whether to download subtitles
5. Set the number of concurrent download threads

## Configuration:

Advanced users can modify `config.py` to adjust default settings:

- `DEFAULT_QUALITY`: Default video quality
- `MAX_RETRIES`: Maximum number of retry attempts for failed downloads
- `CHUNK_SIZE`: Size of chunks for buffered downloading
- `LOG_LEVEL`: Logging verbosity

## Contributing:

We welcome contributions to MultiThreadedYT-Sync! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code adheres to our coding standards and includes appropriate tests.

## Acknowledgements:

- [pytube](https://github.com/pytube/pytube) for YouTube video downloading functionality
- [rich](https://github.com/Textualize/rich) for the enhanced console interface


## Contact:

Mail - `subhransu.nayak.connect@gmail.com`

`Project Link` : [https://github.com/NayakSubhransu/MultiThreadedYT-Sync](https://github.com/yourusername/MultiThreadedYT-Sync)


------------

