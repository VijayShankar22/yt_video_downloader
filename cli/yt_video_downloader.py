import yt_dlp
import os
from tqdm import tqdm
from colorama import init, Fore

init()

def print_banner(banner, color=None):
    if color is not None:
        print("\033[{}m{}\033[0m".format(color, banner))
    else:
        print(banner)

banner = r'''
 _________________________________________________________________________________________________________
|  __   _______  __     ___     _              ____                      _                 _              |
|  \ \ / /_   _| \ \   / (_) __| | ___  ___   |  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __    |
|   \ V /  | |    \ \ / /| |/ _` |/ _ \/ _ \  | | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|   | 
|    | |   | |     \ V / | | (_| |  __/ (_) | | |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |      |
|    |_|   |_|      \_/  |_|\__,_|\___|\___/  |____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|      |
|                                                                                                         |
|                                                                         -github.com/vijayshankar22      |
|_________________________________________________________________________________________________________|
  
  '''
print_banner(banner, 92)


class DownloadProgress:
    def __init__(self):
        self.pbar = None

    def hook(self, d):
        if d['status'] == 'downloading':
            if self.pbar is None:
                total_size = d.get('total_bytes', 0)

                print(Fore.YELLOW + f"\nDownloading: {d.get('filename', 'Video')}" + Fore.RESET)

                self.pbar = tqdm(total=total_size, unit='B', unit_scale=True, leave=True, ncols=150)
            
            self.pbar.update(d.get('downloaded_bytes', 0) - self.pbar.n)
            self.pbar.set_postfix({"Speed": d.get('_speed_str', '')})

        elif d['status'] == 'finished':
            if self.pbar:
                self.pbar.close()
                self.pbar = None
            print(Fore.GREEN + f"Download complete: {d.get('filename', '')}" + Fore.RESET)

def list_formats(url):

    try:
        ydl_opts = {'listformats': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
    except Exception as e:
        print(Fore.RED + f"Error fetching formats: {e}" + Fore.RESET)

def download_video(url, format_id, output_dir):

    ydl_opts = {
        'format': format_id + '+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'progress_hooks': [DownloadProgress().hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print()
        print(Fore.CYAN + "Downloaded successfully." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Download failed: {e}" + Fore.RESET)

def select_download_location():
    
    print(Fore.YELLOW + "\nChoose download location:" + Fore.RESET)
    print()
    print(Fore.LIGHTGREEN_EX + "1. Default folder (C:\\youtube_downloads)" + Fore.RESET)
    print(Fore.LIGHTGREEN_EX + "2. Custom folder" + Fore.RESET)

    while True:
        print()
        choice = input(Fore.CYAN + "Enter your choice (1 or 2): " + Fore.RESET).strip()

        if choice == '1':
            output_dir = r"C:\youtube_downloads"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            return output_dir

        elif choice == '2':
            output_dir = input(Fore.CYAN + "Enter the full folder path: " + Fore.RESET).strip()
            if os.path.exists(output_dir):
                return output_dir
            else:
                print(Fore.RED + "Invalid path. Please enter a valid folder path." + Fore.RESET)
        else:
            print(Fore.RED + "Invalid choice. Please enter 1 or 2." + Fore.RESET)

if __name__ == "__main__":
    while True:
        try:
            url = input(Fore.LIGHTMAGENTA_EX + "Enter the YouTube video URL: " + Fore.RESET).strip()
            if not url:
                raise ValueError("YouTube URL cannot be empty")

            print("Fetching available formats...")
            list_formats(url)

            print()
            format_id = input(Fore.LIGHTMAGENTA_EX + "Enter the format ID to download: " + Fore.RESET).strip()
            if not format_id:
                raise ValueError("Format ID cannot be empty")

            output_dir = select_download_location()
            
            download_video(url, format_id, output_dir)

            print()
            another = input(Fore.GREEN + "\nDo you want to download another video? (y/n): " + Fore.RESET).strip().lower()
            if another != 'y':
                break

        except ValueError as ve:
            print(Fore.RED + f"Input Error: {ve}" + Fore.RESET)
        except Exception as e:
            print(Fore.RED + f"Unexpected Error: {e}" + Fore.RESET)
