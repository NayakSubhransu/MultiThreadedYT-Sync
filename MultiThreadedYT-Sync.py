import os
import sys
import re
import requests
import time
import concurrent.futures
import logging
from pytube import YouTube, Playlist
from colorama import init
from pyfiglet import Figlet
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.live import Live
from rich.style import Style
from rich.text import Text
from rich.layout import Layout
from threading import Lock
from datetime import timedelta
from art import text2art
from ffmpeg_progress_yield import FfmpegProgress

# Initialize colorama and rich console
init(autoreset=True)
console = Console()
progress_lock = Lock()

# Set up logging
logging.basicConfig(filename='YT_downloader.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def print_banner(yt_size="small", pd_size="small"):
    layout = Layout()
    layout.split_column(
        Layout(name="upper"),
        Layout(name="lower")
    )

    # YT text
    f_yt = Figlet(font='block')
    if yt_size == "small":
        yt_text = f_yt.renderText('YOUTUBE')
    elif yt_size == "medium":
        yt_text = f_yt.renderText('YOUTUBE')
    else:  # large
        yt_text = f_yt.renderText('YOUTUBE')
    
    yt_styled = Text(yt_text, style="red bold")
    
    pd_text = Figlet(font='slant', width=100).renderText('Playlist Downloader')
    pd_styled = Text(pd_text, style="red")

    # Adjust panel sizes based on content
    yt_panel = Panel(yt_styled, border_style="yellow", expand=False, padding=(2, 0))
    pd_panel = Panel(pd_styled, border_style="yellow", expand=False, padding=(2,0))

    layout["upper"].update(yt_panel)
    layout["lower"].update(pd_panel)

    console.print(layout)
    console.print("=" * console.width, style="red bold")
    console.print("\n[bold cyan]Welcome to the Ultimate YouTube Playlist Downloader![/bold cyan]")
    console.print("[italic]Crafted with ❤️ for seamless video downloads[/italic]\n")


def check_internet_connection():
    with console.status("[bold yellow]Checking internet connection...", spinner="dots") as status:
        try:
            requests.get("https://www.google.com", timeout=5)
            console.print("\n[bold green]✓ Internet Connection Established![/bold green]")
            console.print("[dim]Ready to fetch your favorite YouTube content[/dim]\n")
            return True
        except requests.ConnectionError:
            console.print("\n[bold red]✗ Internet Connection Failed![/bold red]")
            console.print("[dim]Please check your network and try again[/dim]\n")
            return False


def is_valid_youtube_playlist_url(url):
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/playlist\?list=[\w-]+$'
    return re.match(pattern, url) is not None


def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def get_video_metadata(yt):
    return f"[cyan]Title:[/cyan] {yt.title}\n[cyan]Views:[/cyan] {yt.views:,}\n[cyan]Uploaded:[/cyan] {yt.publish_date.strftime('%Y-%m-%d')}\n[cyan]Duration:[/cyan] {timedelta(seconds=yt.length)}"

def download_video(video_url, output_path, index, total, progress, task_id, quality='highest', format='mp4', download_subtitles=False, max_retries=3):
    for attempt in range(max_retries):
        try:
            yt = YouTube(video_url)
            metadata = get_video_metadata(yt)
            console.print(f"\n[yellow]Downloading video {index}/{total}:")
            console.print(Panel(metadata, title="[bold green]Video Metadata", border_style="cyan", expand=False))

            if format == 'mp3':
                stream = yt.streams.get_audio_only()
            else:
                if quality == 'highest':
                    stream = yt.streams.get_highest_resolution()
                else:
                    stream = yt.streams.filter(progressive=True, resolution=quality).first()
                    if not stream:
                        console.print(f"[yellow]Quality {quality} not available. Choosing highest available quality.[/yellow]")
                        stream = yt.streams.get_highest_resolution()

            filename = sanitize_filename(f"{index:03d}_{yt.title}.{format}")
            output_file = os.path.join(output_path, filename)

            start_time = time.time()

            def progress_callback(stream, chunk, bytes_remaining):
                with progress_lock:
                    downloaded = stream.filesize - bytes_remaining
                    progress.update(task_id, completed=downloaded, total=stream.filesize)
                    elapsed_time = time.time() - start_time
                    speed = downloaded / elapsed_time / 1024 / 1024  # MB/s
                    progress.update(task_id, description=f"[cyan]Video {index}/{total}[/cyan] - [yellow]{speed:.2f} MB/s[/yellow]")

            yt.register_on_progress_callback(progress_callback)
            stream.download(output_path=output_path, filename=filename)

            if download_subtitles:
                caption = yt.captions.get_by_language_code('en')
                if caption:
                    subtitle_filename = f"{filename}.srt"
                    with open(os.path.join(output_path, subtitle_filename), 'w', encoding='utf-8') as f:
                        f.write(caption.generate_srt_captions())
                    console.print(f"[bold green]✓ Subtitles downloaded:[/bold green] {subtitle_filename}")

            console.print(f"[bold green]✓ Download complete:[/bold green] {filename}")
            logging.info(f"Successfully downloaded: {filename}")
            return True
        except Exception as e:
            console.print(f"[bold red]✗ Error downloading video {index} (Attempt {attempt + 1}/{max_retries}): {str(e)}[/bold red]")
            logging.error(f"Error downloading video {index} (Attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                return False
            time.sleep(5)  # Wait before retrying

def download_playlist(playlist_url, output_path, quality='highest', format='mp4', download_subtitles=False, max_workers=3):
    if not check_internet_connection():
        return

    try:
        playlist = Playlist(playlist_url)
        console.print(Panel.fit(f"[bold cyan]Playlist Title:[/bold cyan] {playlist.title}\n[bold cyan]Number of videos:[/bold cyan] {len(playlist.video_urls)}", title="Playlist Info", border_style="yellow"))

        total_duration = sum(YouTube(url).length for url in playlist.video_urls)
        console.print(f"[cyan]Total playlist duration:[/cyan] [bold]{str(timedelta(seconds=total_duration))}[/bold]")

        progress = Progress(
            "[progress.description]{task.description}",
            SpinnerColumn(),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
        )

        with Live(Columns([progress, Panel("", title="Download Status", border_style="green")]), refresh_per_second=10) as live:
            tasks = []
            for i, video_url in enumerate(playlist.video_urls, start=1):
                task_id = progress.add_task(description=f"Video {i}/{len(playlist.video_urls)}", total=100)
                tasks.append((task_id, video_url))

            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(download_video, video_url, output_path, i, len(playlist.video_urls), progress, task_id, quality, format, download_subtitles) 
                           for i, (task_id, video_url) in enumerate(tasks, start=1)]
                for future in concurrent.futures.as_completed(futures):
                    completed = sum(1 for f in futures if f.done())
                    live.update(Columns([progress, Panel(f"[green]Completed:[/green] {completed}/{len(playlist.video_urls)}\n[yellow]In Progress:[/yellow] {len(playlist.video_urls) - completed}", title="Download Status", border_style="green")]))
                    time.sleep(0.1)

        display_summary(playlist.title, len(playlist.video_urls), output_path, format)

    except Exception as e:
        console.print(f"[bold red]Error: Unable to access the playlist. Details: {str(e)}[/bold red]")
        console.print("[yellow]Please check the URL and your internet connection, then try again.[/yellow]")
        logging.error(f"Error accessing playlist: {str(e)}")



def get_output_path():
    while True:
        output_path = Prompt.ask("[cyan]Enter the output directory", default=os.getcwd())
        
        if not os.path.exists(output_path):
            if Confirm.ask(f"[yellow]Directory doesn't exist. Create it?"):
                try:
                    os.makedirs(output_path)
                    console.print(f"[bold green]✓ Created output directory:[/bold green] {output_path}")
                    return output_path
                except Exception as e:
                    console.print(f"[bold red]✗ Error creating output directory: {str(e)}[/bold red]")
            else:
                console.print("[yellow]Please enter a valid directory path.[/yellow]")
        else:
            return output_path


def display_summary(playlist_title, num_videos, output_path, audio_only):
    table = Table(title="Download Summary", show_header=True, header_style="bold magenta", border_style="cyan")
    table.add_column("Item", style="cyan", width=20)
    table.add_column("Value", style="yellow")
    
    table.add_row("Playlist Title", playlist_title)
    table.add_row("Number of Videos", str(num_videos))
    table.add_row("Output Directory", output_path)
    table.add_row("Download Type", "Audio Only 🎵" if audio_only else "Video 🎥")
    
    console.print(table)



def main():
    print_banner()

    while True:
        playlist_url = Prompt.ask("[cyan]Enter the YouTube playlist URL (or 'q' to quit)")
        
        if playlist_url.lower() == 'q':
            console.print("\n[yellow]Thank you for using YouTube Playlist Downloader! 👋[/yellow]")
            sys.exit(0)

        if not is_valid_youtube_playlist_url(playlist_url):
            console.print("[bold red]✗ Error: Invalid YouTube playlist URL. Please enter a valid URL.[/bold red]")
            continue

        output_path = get_output_path()
        format = Prompt.ask("[cyan]Choose output format", choices=['mp4', 'mp3'], default='mp4')
        
        if format == 'mp4':
            quality = Prompt.ask("[cyan]Choose video quality", choices=['highest', '360p', '720p', '1080p'], default='highest')
        else:
            quality = 'highest'  # For mp3, always use highest quality audio

        download_subtitles = Confirm.ask("[cyan]Download subtitles (if available)?")
        max_workers = Prompt.ask("[cyan]Enter the number of concurrent downloads", default="3")

        console.print(f"[yellow]Downloading playlist to:[/yellow] [bold]{output_path}[/bold]")
        download_playlist(playlist_url, output_path, quality, format, download_subtitles, int(max_workers))

        console.print("\n[bold green]✓ Playlist download complete! 🎉[/bold green]")
        console.print("[yellow]" + "=" * 60 + "[/yellow]")

        if not Confirm.ask("[cyan]Do you want to download another playlist?"):
            console.print("\n[yellow bold]Thank you for using YouTube Playlist Downloader! 👋[/yellow bold]")
            break
        console.print("[yellow]" + "=" * 60 + "[/yellow]")

if __name__ == "__main__":
    main()
