# import imageio
# imageio.plugins.ffmpeg.download()

import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy import VideoFileClip  # Correct import for moviepy
# from moviepy.editor import *
import os

def download_video_with_yt_dlp(url, output_dir="downloads"):
    """
    Downloads the full video from YouTube using yt-dlp.
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Options for yt-dlp to download the best quality video
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'best',
        }

        # Use yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("Download complete!")
        return os.path.join(output_dir, f'{yt_dlp.YoutubeDL().extract_info(url, download=False)["title"]}.mp4')

    except Exception as e:
        print(f"An error occurred while downloading: {e}")
        return None

def download_youtube_snippet(url, start_time, end_time, output_dir="snippets", snippet_name="snippet.mp4"):
    """
    Downloads the video and extracts a snippet based on start_time and end_time.
    """
    try:
        # Step 1: Download full video
        print(f"Downloading full video from {url}...")
        video_path = download_video_with_yt_dlp(url, output_dir)

        if not video_path:
            print("Failed to download video.")
            return

        # Step 2: Trim the video to create the snippet
        print(f"Processing snippet from {start_time} to {end_time}...")
        try:
            with VideoFileClip(video_path) as video:
                print(video_path)
                print(video)
                snippet = video.subclip(start_time, end_time)  # Ensure subclip is called correctly
                snippet_output_path = rf'{output_dir}/{snippet_name}'
                print(snippet_output_path)
                # snippet_output_path = os.path.join(output_dir, snippet_name)
                snippet.write_videofile(snippet_output_path, codec="libx264")
            print(f"Snippet saved: {snippet_output_path}")
        except Exception as e:
            print(f"Error processing the video with moviepy: {e}")

        # Optionally delete the full video after trimming
        os.remove(video_path)

    except Exception as e:
        print(f"An error occurred while processing the snippet: {e}")

def time_to_seconds(t):
    """
    Converts a time in HH:MM:SS or seconds format to total seconds.
    """
    if ":" in t:
        parts = list(map(int, t.split(":")))
        return sum(p * 60**i for i, p in enumerate(reversed(parts)))
    return int(t)

if __name__ == "__main__":
    # Example usage
    video_url = input("Enter the YouTube video URL: ").strip()
    start = input("Enter the start time (in seconds or HH:MM:SS): ").strip()
    end = input("Enter the end time (in seconds or HH:MM:SS): ").strip()
    # output_directory = input(r"Enter the output directory (leave blank for default 'snippets'): ").strip() or "snippets"
    output_directory = r'C:\Users\jpmar\OneDrive\Documents\Temp_Work_Folder_DAI\Code\test'
    snippet_filename = input("Enter the snippet file name (e.g., 'snippet.mp4'): ").strip() or "snippet.mp4"
    # output_directory = output_directory.replace("\","/""

    # Convert start and end times to seconds
    start_seconds = time_to_seconds(start)
    end_seconds = time_to_seconds(end)

    # Download the snippet
    download_youtube_snippet(video_url, start_seconds, end_seconds, output_directory, snippet_filename)
 