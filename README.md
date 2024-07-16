


# MultiThreadedYT-Sync: Advanced YouTube Playlist Downloader

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

`MultiThreadedYT-Sync` is a high-performance, concurrent YouTube playlist downloader leveraging Python's multithreading capabilities. This application is designed to significantly accelerate the process of acquiring large video collections while providing a rich, interactive console interface.

## Features

- **Concurrent Downloads**: Utilizes Python's threading module to download multiple videos simultaneously.
- **Adaptive Quality Selection**: Supports various video qualities (360p, 720p, 1080p) with automatic fallback to the highest available quality.
- **Format Flexibility**: Offers both video (MP4) and audio-only (MP3) download options.
- **Subtitle Integration**: Optional download of available subtitles in SRT format.
- **Rich Console Interface**: Implements the `rich` library for an enhanced, colorful command-line experience.
- **Real-time Progress Tracking**: Displays download progress, speed, and estimated time remaining for each video.
- **Robust Error Handling**: Implements retry mechanisms and comprehensive logging for troubleshooting.
- **Customizable Output**: Allows users to specify custom output directories and filename patterns.

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

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

## Usage

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

## Configuration

Advanced users can modify `config.py` to adjust default settings:

- `DEFAULT_QUALITY`: Default video quality
- `MAX_RETRIES`: Maximum number of retry attempts for failed downloads
- `CHUNK_SIZE`: Size of chunks for buffered downloading
- `LOG_LEVEL`: Logging verbosity

## Contributing

We welcome contributions to MultiThreadedYT-Sync! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code adheres to our coding standards and includes appropriate tests.

## Acknowledgements

- [pytube](https://github.com/pytube/pytube) for YouTube video downloading functionality
- [rich](https://github.com/Textualize/rich) for the enhanced console interface


## Contact

Mail - `subhransu.nayak.connect@gmail.com`

`Project Link` : [https://github.com/NayakSubhransu/MultiThreadedYT-Sync](https://github.com/yourusername/MultiThreadedYT-Sync)


------------
/yourusername/MultiThreaded-Tube](https://github.com/yourusername/MultiThreaded-Tube)
