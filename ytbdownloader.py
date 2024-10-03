import os
import sys
import time
import threading  # Import threading per gestire i thread
import tkinter
import pytube
from tkinter import messagebox

root = tkinter.Tk()
title_label = tkinter.Label(root, text="Title:")
duration_label = tkinter.Label(root, text="Duration:")
status_label = tkinter.Label(root, text="Status: Ready")


def sanitize_filename(filename: str) -> str:
    # remove ",',\,/,*,<,>,|,?,:,; from the filename
    return "".join(c for c in filename if c not in r'\/:*?"<>|')

    

def setup_folders():
    if not os.path.exists("downloads"):
        global status_label
        status_label = tkinter.Label(root, text="Status: Ready")
        os.makedirs("downloads")
        status_label = tkinter.Label(root, text="Status: Created downloads folder")

def download_media(url: str, format: str, start_time):
    global status_label
    global title_label
    global duration_label
    try:
        yt = pytube.YouTube(url)

        title_label.config(text=f"Title: {yt.title}")
        duration_label.config(text=f"Duration: {yt.length} seconds")

        if format == "mp3":

            stream = yt.streams.filter(only_audio=True).first()

            status_label.config(text="Downloading audio...")

            if not os.path.exists("downloads/audios"):
                os.makedirs("downloads/audios")
            # download as mp3
            path = stream.download("downloads/audios", filename="audio.mp4")

            # convert to mp3 using ffmpeg opening a mp4

            name = sanitize_filename(yt.title)
            os.system(f'ffmpeg -y -i "{path}" "downloads/audios/{name}.mp3"')
            os.remove(path)

            status_label.config(text="Download complete")
            path = f"downloads/audios/{yt.title}.mp3"


        else:
            stream = yt.streams.filter(adaptive=True, file_extension="mp4").first()
            status_label.config(text="Downloading video...")
            if not os.path.exists("downloads/videos"):
                os.makedirs("downloads/videos")

            stream_video = yt.streams.filter(only_video=True).first()
            stream_video.download("downloads/videos", filename="video.mp4")          

            status_label.config(text="Downloading audio (for merging)...")
            stream_audio = yt.streams.filter(only_audio=True).first()
            stream_audio.download("downloads/videos", filename="audio.mp4")

            # Merge the audio and video
            name = sanitize_filename(yt.title)
            os.system(f'ffmpeg -y -i "downloads/videos/video.mp4" -i "downloads/videos/audio.mp4" -c copy "downloads/videos/{name}.mp4"')
            os.remove("downloads/videos/video.mp4")
            os.remove("downloads/videos/audio.mp4")

            status_label.config(text="Download complete")
            path = f"downloads/videos/{yt.title}.mp4"



        elapsed_time = time.time() - start_time
        print(f"Download completed in {elapsed_time:.2f} seconds.")
        return path, elapsed_time
    except Exception as e:
        print(e)
        return False, 0


def gui():
    root.title("YouTube Downloader")
    root.geometry("500x500")
    root.resizable(False, False)

    # Posizioniamo la finestra al centro dello schermo
    def center_window():
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
        x = screen_width // 2 - size[0] // 2
        y = screen_height // 2 - size[1] // 2
        root.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

    center_window()  # Centra la finestra

    setup_folders()

    title = tkinter.Label(root, text="YouTube Downloader", font=("Arial", 20))
    title.pack()

    url_label = tkinter.Label(root, text="URL:")
    url_label.pack()

    url_entry = tkinter.Entry(root, width=50)
    url_entry.pack()

    # Dropdown menu for selecting the format
    format_var = tkinter.StringVar()
    format_var.set("mp4")
    format_label = tkinter.Label(root, text="Format:")
    format_label.pack()

    format_menu = tkinter.OptionMenu(root, format_var, "mp4", "mp3")
    format_menu.pack()

    status_label.pack()

    title_label.pack()

    duration_label.pack()

    elapsed_time_label = tkinter.Label(root, text="")
    elapsed_time_label.pack()

    def threaded_download():
        url = url_entry.get()
        format = format_var.get()
        if not url:
            messagebox.showerror("Error", "URL cannot be empty")
            return

        start_time = time.time()
        path, elapsed_time = download_media(url, format, start_time)
        if path:
            messagebox.showinfo("Success", f"Downloaded to {path}")
            elapsed_time_label.config(text=f"Elapsed Time: {elapsed_time:.2f}s")
        else:
            messagebox.showerror("Error", "Failed to download")

        status_label.config(text="Download complete")

        # FOOTBAR with github link redirect
        footbar = tkinter.Label(root, text="Made by @danieleavolio", font=("Arial", 10))
        footbar.pack()


    def download():
        # Esegui il download in un thread separato
        download_thread = threading.Thread(target=threaded_download)
        download_thread.start()

    download_button = tkinter.Button(root, text="Download", command=download)
    download_button.pack()

    # When the download starts, change the status label to "Downloading..."
    def on_download():
        elapsed_time_label.config(text="Elapsed Time: 0s")  # Reset elapsed time
        root.update()

    download_button.bind("<Button-1>", lambda e: on_download())

    # Close the window when the close button is clicked
    def on_closing():
        root.destroy()
        root.quit()
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


if __name__ == "__main__":
    gui()
