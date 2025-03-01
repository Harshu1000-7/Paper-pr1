import os
import sys
import subprocess
import shutil
import requests
import socket
import numpy as np
import colorama
from colorama import Fore, Style
import random
from bs4 import BeautifulSoup
import threading
import time
import requests



previous_dir = os.getcwd()

THEMES = {
    "default": {"text": Fore.WHITE, "ascii": Fore.CYAN, "prompt": Fore.LIGHTCYAN_EX},
    "cyberpunk": {"text": Fore.MAGENTA, "ascii": Fore.BLUE, "prompt": Fore.LIGHTBLUE_EX},
    "retro": {"text": Fore.GREEN, "ascii": Fore.LIGHTGREEN_EX, "prompt": Fore.YELLOW},
}
current_theme = "default"

ASCII_BOOT = r"""
 
  _____                      
 |  __ \                     
 | |__) |_ _ _ __   ___ _ __ 
 |  ___/ _` | '_ \ / _ \ '__|
 | |  | (_| | |_) |  __/ |   
 |_|   \__,_| .__/ \___|_|   
            | |              
            |_|              

  Welcome to Paper, a Python CLI OS 
  Type 'help' for commands.
"""
def change_theme(theme):
    global current_theme
    if theme in THEMES:
        current_theme = theme
        print(f"{THEMES[current_theme]['text']}Theme changed to {theme}!")
    else:
        print(f"{Fore.RED}Invalid theme. Available themes: {', '.join(THEMES.keys())}")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def list_files():
    for file in os.listdir():
        print(file)

def change_directory(path):
    global previous_dir
    try:
        previous_dir, os.getcwd()
        os.chdir(path)
        print(f"Changed directory to: {os.getcwd()}")
    except FileNotFoundError:
        print("Directory not found")
    except PermissionError:
        print("Permission denied")

def go_back():
    change_directory(previous_dir)

def run_command(command):
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        print(f"Error executing command: {e}")

def install_package(package):
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Error installing package: {e}")

def create_folder(folder_name):
    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"Folder '{folder_name}' created.")
    except Exception as e:
        print(f"Error creating folder: {e}")

def delete_folder(folder_name):
    def on_error(func, path, exc_info):
        """ Change file permission and retry """
        os.chmod(path, 0o777)  # Change permission
        func(path)  # Retry deletion

    try:
        shutil.rmtree(folder_name, onerror=on_error)
        print(f"Folder '{folder_name}' deleted.")
    except FileNotFoundError:
        print("Folder not found")
    except PermissionError:
        print("Permission denied. Try running as administrator.")
    except Exception as e:
        print(f"Error deleting folder: {e}")

def create_file(filename):
    try:
        with open(filename, 'w') as file:
            file.write("")  # Empty file creation
        print(f"File '{filename}' created.")
    except Exception as e:
        print(f"Error creating file: {e}")

def view_file(filename):
    try:
        with open(filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"Error reading file: {e}")

def delete_file(filename):
    try:
        if os.path.isfile(filename):
            os.remove(filename)
            print(f"Deleted file: {filename}")
        else:
            print("File not found")
    except Exception as e:
        print(f"Error: {e}")


def get_local_ip():
    ip = socket.gethostbyname(socket.gethostname())
    print(f"Local IP Address: {ip}")

def get_public_ip():
    try:
        ip = requests.get("https://api64.ipify.org").text
        print(f"Public IP Address: {ip}")
    except:
        print("Unable to fetch public IP")

def ping_host(host):
    os.system(f"ping -c 4 {host}" if os.name != "nt" else f"ping {host}")

def traceroute(host):
    os.system(f"traceroute {host}" if os.name != "nt" else f"tracert {host}")

def check_open_ports(host):
    print(f"Scanning open ports on {host}...")
    for port in range(1, 1025):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((host, port)) == 0:
                print(f"Port {port} is open")

    

def web_scraper(url, save=False, filename=None):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful

        if save and filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Web scraped content saved to {filename}")
        else:
            print(response.text)  # Print raw HTML content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")

def binary_to_text(binary):
    binary_values = binary.split()
    return ''.join(chr(int(b, 2)) for b in binary_values)


def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)

def edit_file(filename):
    """Edit a file directly in the CLI OS."""
    try:
        if not os.path.exists(filename):
            print(f"File '{filename}' does not exist. Creating a new file.")
            create_file(filename)

        print(f"Editing '{filename}'... Type your content below.")
        print("Press Ctrl+D (Linux/Mac) or Ctrl+Z (Windows) + Enter to save.")

        content = []
        while True:
            try:
                line = input()
                content.append(line)
            except EOFError:
                break

        with open(filename, 'w') as file:
            file.write("\n".join(content) + "\n")

        print(f"File '{filename}' saved successfully.")

    except Exception as e:
        print(f"Error editing file: {e}")

def matrix_rain():
    print('Ctrl + C to stop')
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()"
    width = os.get_terminal_size().columns
    drops = [0] * width
    
    try:
        while True:
            print("".join(random.choice(chars) if random.random() > 0.95 else " " for _ in range(width)))
            drops = [(drop + 1 if drop < random.randint(1, 10) else 0) for drop in drops]
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nMatrix rain stopped.")

def copy(src, dest):
    """ Copy a file or folder """
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        print(f"Copied '{src}' to '{dest}'")
    except Exception as e:
        print(f"Error copying: {e}")
        
def cpu_ram_usage():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    print(f"CPU Usage: {cpu}% | RAM Usage: {ram}%")

def system_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_string = time.strftime('%H:%M:%S', time.gmtime(uptime_seconds))
    print(f"System Uptime: {uptime_string}")


def move(src, dest):
    """ Move a file or folder """
    try:
        shutil.move(src, dest)
        print(f"Moved '{src}' to '{dest}'")
    except Exception as e:
        print(f"Error moving: {e}")

def list_processes():
    """ List running processes """
    for proc in psutil.process_iter(['pid', 'name']):
        print(f"{proc.info['pid']:>6} - {proc.info['name']}")

def kill_process(pid):
    """ Kill a process by PID """
    try:
        psutil.Process(int(pid)).terminate()
        print(f"Process {pid} terminated.")
    except Exception as e:
        print(f"Error killing process: {e}")

def download_file(url, filename):
    """ Download a file from the web """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"File downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Download error: {e}")

def about():
    print('Made By HarshuJiwane')
    print('Github: https://github.com/Harshu1000-7')
    print('Discord: solaris3551')
    print("version: pr.2")



def show_help():
    print("""
CLI OS Commands:
  clear            - Clear screen
  ls               - List files
  cd <dir>         - Change directory
  cd -             - Go back
  run <cmd>        - Run system command
  install <p>      - Install a Python package
  mkdir <dir>      - Create folder
  rmdir <dir>      - Delete folder
  cp <src> <dest>  - Copy a file or folder
  mv <src> <dest>  - Move a file or folder
  ps               - List running processes
  kill <pid>       - Kill a process by PID
  download <url> <file> - Download a file from the web
  touch <file>     - Create file
  edit <file>      - Edit a file
  cat <file>       - View file content
  rm <file>        - Delete file
  local-ip         - Show local IP address
  public-ip        - Show public IP address
  ping <host>      - Ping a host
  traceroute <h>   - Trace route to a host
  uptime           - Show system uptime
  usage            - Show CPU and RAM usage
  theme <name>     - Change color theme (default, cyberpunk, retro)
  scan-ports <h>   - Scan open ports on a host
  text-bin <txt>   - Convert text to binary
  bin-text <bin>   - Convert binary to text
  scrape <url>     - Web scraper to fetch page content
  matrix           - Start Matrix rain effect
  exit             - Exit CLI
  help             - Show commands
  about            - About...
""")

def main():
    clear_screen()
    print(ASCII_BOOT)
    
    while True:
        try:
            command = input(THEMES[current_theme]["text"] + "Paper> ").strip()
            parts = command.split()
            if not parts:
                continue

            cmd, *args = parts

            commands = {
                "clear": clear_screen,
                "ls": list_files,
                "cd": lambda: change_directory(args[0]) if args else print("Usage: cd <dir>"),
                "cd-": go_back,
                "mkdir": lambda: create_folder(args[0]) if args else print("Usage: mkdir <folder>"),
                "rmdir": lambda: delete_folder(args[0]) if args else print("Usage: rmdir <folder>"),
                "touch": lambda: create_file(args[0]) if args else print("Usage: touch <file>"),
                "cat": lambda: view_file(args[0]) if args else print("Usage: cat <file>"),
                "rm": lambda: delete_file(args[0]) if args else print("Usage: rm <file>"),
                "run": lambda: run_command(" ".join(args)) if args else print("Usage: run <command>"),
                "install": lambda: install_package(args[0]) if args else print("Usage: install <package>"),
                "local-ip": get_local_ip,
                "public-ip": get_public_ip,
                "ping": lambda: ping_host(args[0]) if args else print("Usage: ping <host>"),
                "traceroute": lambda: traceroute(args[0]) if args else print("Usage: traceroute <host>"),
                "scan-ports": lambda: check_open_ports(args[0]) if args else print("Usage: scan-ports <host>"),
                "theme": lambda: change_theme(args[0]) if args else print("Usage: theme <name>"),
                "edit": lambda: edit_file(args[0]) if args else print("Usage: edit <filename>"),
                "text-bin": lambda: print(text_to_binary(args[0])) if args else print("Usage: text-bin <text>"),
                "bin-text": lambda: print(binary_to_text(args[0])) if args else print("Usage: bin-text <binary>"),
                "scrape": lambda: (
                    web_scraper(args[0], save=("-s" in args), filename=(args[args.index("-s")+1] if "-s" in args else None))
                ) if args else print("Usage: scrape <url> [-s filename]"),
                "cp": lambda: copy(args[0], args[1]) if len(args) >= 2 else print("Usage: cp <src> <dest>"),
                "mv": lambda: move(args[0], args[1]) if len(args) >= 2 else print("Usage: mv <src> <dest>"),
                "uptime": system_uptime,
                "usage": cpu_ram_usage,
                "ps": list_processes,
                "kill": lambda: kill_process(args[0]) if args else print("Usage: kill <pid>"),
                "download": lambda: download_file(args[0], args[1]) if len(args) >= 2 else print("Usage: download <url> <file>"),
                "matrix": matrix_rain,
                "help": show_help,
                "exit": sys.exit,
                "about": about,
            }

            commands.get(cmd, lambda: print("Unknown command. Type 'help'."))()

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")

if __name__ == "__main__":
    main()
