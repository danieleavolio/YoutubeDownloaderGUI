# YouTube Downloader

![](https://i.imgur.com/Yl3hDLf.png)
This project is a simple YouTube downloader application with a graphical user interface (GUI) built using Tkinter. It allows users to download audio and video files from YouTube.

### Project Structure

app.bat
downloads/
    audios/
    videos/
README.md
requirements.txt
ytbdownloader.py

- app.bat: A batch script to install required dependencies and run the application.
- downloads/: Directory where downloaded media files are stored.
  - audios/: Subdirectory for downloaded audio files.
  - videos/: Subdirectory for downloaded video files.
- README.md: This file.
- requirements.txt: Lists the Python dependencies required for the project.
- ytbdownloader.py: The main Python script for the YouTube downloader application.

### Setup

1. Install Dependencies:
   Run the following command to install the required Python packages:
   pip install -r requirements.txt

2. Run the Application:
   You can start the application by running the batch script:
   app.bat

### Usage

![GUI](https://i.imgur.com/7gLoPe1.png)
1. GUI:
   - The application opens a GUI window with labels for the title, duration, and status.
   - Enter the YouTube URL and select the format (audio or video) to download.

2. Download:
   - The downloaded files will be saved in the downloads/audios or downloads/videos directory based on the selected format.

### Dependencies

- pytube: A lightweight, dependency-free Python library (and command-line utility) for downloading YouTube videos.

### License

This project is licensed under the MIT License.