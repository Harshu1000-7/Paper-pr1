import os
import sys
import subprocess
import shutil
import psutil
import requests


previous_dir = os.getcwd()

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
    try:
        shutil.rmtree(folder_name)
        print(f"Folder '{folder_name}' deleted.")
    except FileNotFoundError:
        print("Folder not found")
    except Exception as e:
        print(f"Error deleting folder: {e}")

def create_file(filename):
    try:
        with open(filename, 'w') as file:
            file.write("")  # Empty file creation
        print(f"File '{filename}' created.")
    except Exception as e:
        print(f"Error creating file: {e}")

def edit_file(filename):
    try:
        if not os.path.exists(filename):
            print(f"File '{filename}' does not exist. Creating it.")
            create_file(filename)

        print(f"Editing '{filename}'... Type content below.")
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

        print(f"File '{filename}' saved.")

    except Exception as e:
        print(f"Error editing file: {e}")

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

def copy_file(src, dest):
    try:
        if os.path.isfile(src):
            shutil.copy(src, dest)
            print(f"Copied {src} to {dest}")
        elif os.path.isdir(src):
            shutil.copytree(src, dest)
            print(f"Copied folder {src} to {dest}")
    except Exception as e:
        print(f"Error: {e}")

def move_file(src, dest):
    try:
        shutil.move(src, dest)
        print(f"Moved {src} to {dest}")
    except Exception as e:
        print(f"Error: {e}")

def list_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        print(f"PID: {proc.info['pid']} - {proc.info['name']}")

def kill_process(pid):
    try:
        p = psutil.Process(int(pid))
        p.terminate()
        print(f"Terminated process {pid}")
    except Exception as e:
        print(f"Error: {e}")

def about():
    print('Made By HarshuJiwane')
    print('Github: https://github.com/Harshu1000-7')
    print('Discord: solaris3551')
    print("version: pr.1")

def download_file(url, filename):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Download error: {e}")

def show_help():
    print("""
CLI OS Commands:
  clear       - Clear screen
  ls          - List files
  cd <dir>    - Change directory
  cd -        - Go back
  run <cmd>   - Run system command
  install <p> - Install a Python package
  mkdir <dir> - Create folder
  rmdir <dir> - Delete folder
  touch <file> - Create file
  edit <file> - Edit file
  cat <file>  - View file content
  rm <file>   - Delete file
  cp <src> <dest> - Copy file/folder
  mv <src> <dest> - Move file/folder
  ps          - List processes
  kill <pid>  - Kill process
  download <url> <file> - Download file
  exit        - Exit CLI
  help        - Show commands
  about       - Info
""")

def main():
    clear_screen()
    print(ASCII_BOOT)
    
    while True:
        try:
            command = input("cli-os> ").strip()
            parts = command.split()
            if not parts:
                continue

            cmd, *args = parts

            commands = {
                "about": about,
                "clear": clear_screen,
                "ls": list_files,
                "cd": lambda: change_directory(args[0]) if args else print("Usage: cd <dir>"),
                "cd-": go_back,
                "mkdir": lambda: create_folder(args[0]) if args else print("Usage: mkdir <folder>"),
                "rmdir": lambda: delete_folder(args[0]) if args else print("Usage: rmdir <folder>"),
                "touch": lambda: create_file(args[0]) if args else print("Usage: touch <file>"),
                "edit": lambda: edit_file(args[0]) if args else print("Usage: edit <file>"),
                "cat": lambda: view_file(args[0]) if args else print("Usage: cat <file>"),
                "rm": lambda: delete_file(args[0]) if args else print("Usage: rm <file>"),
                "run": lambda: run_command(" ".join(args)) if args else print("Usage: run <command>"),
                "install": lambda: install_package(args[0]) if args else print("Usage: install <package>"),
                "cp": lambda: copy_file(args[0], args[1]) if len(args) == 2 else print("Usage: cp <src> <dest>"),
                "mv": lambda: move_file(args[0], args[1]) if len(args) == 2 else print("Usage: mv <src> <dest>"),
                "ps": list_processes,
                "kill": lambda: kill_process(args[0]) if args else print("Usage: kill <pid>"),
                "download": lambda: download_file(args[0], args[1]) if len(args) == 2 else print("Usage: download <url> <file>"),
                "help": show_help,
                "exit": sys.exit,
            }

            commands.get(cmd, lambda: print("Unknown command. Type 'help'."))()

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")

if __name__ == "__main__":
    main()
