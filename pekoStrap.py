import os
import subprocess
import sys
import json
import platform
from colorama import Fore, Style, init

# Init colorama
init(autoreset=True)

FASTFLAGS_FILE = "fastFlags.json"  # New file for fastflags

# fixed press any key (i think??)
if os.name == "nt":
    import msvcrt
    def press_any_key(prompt="Press any key to continue..."):
        print(Fore.MAGENTA + prompt, end="", flush=True)
        msvcrt.getch()
        print()
else:
    def press_any_key(prompt="Press any key to continue..."):
        input(Fore.MAGENTA + prompt)

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def load_fastflags():
    """Load fastflags from fastFlags.json, auto-create file if missing"""
    if not os.path.exists(FASTFLAGS_FILE):
        with open(FASTFLAGS_FILE, "w") as f:
            json.dump({}, f)
        return {}
    try:
        with open(FASTFLAGS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_fastflags(fastflags):
    """Save fastflags dict to fastFlags.json"""
    with open(FASTFLAGS_FILE, "w") as f:
        json.dump(fastflags, f, indent=2)

def ask_fastflags():
    """Ask user for a new fastflag key/value and save it (WIP)"""
    clear()
    print(Fore.YELLOW + "=== FastFlags Configuration (WIP) ===")
    fastflags = load_fastflags()
    
    if fastflags:
        print(Fore.CYAN + "Current fastflags:")
        for k, v in fastflags.items():
            print(Fore.YELLOW + f" - {k} = {v}")
    else:
        print(Fore.MAGENTA + "No fastflags set yet.")
    
    print(Fore.GREEN + "\nEnter a new fastflag (leave key blank to cancel):")
    key = input(Fore.WHITE + "Key: ").strip()
    
    if not key:
        print(Fore.RED + "[*] Cancelled, no changes made.")
        press_any_key()
        return
    
    value = input(Fore.WHITE + "Value: ").strip()
    fastflags[key] = value
    save_fastflags(fastflags)
    print(Fore.GREEN + f"[*] Saved fastflag: {key} = {value}")
    print(Fore.YELLOW + "[*] Note: FastFlags are currently WIP and won't be applied when launching.")
    press_any_key()

def debug():
    clear()
    print(Fore.MAGENTA + "Debug info")

    # check pekora paths
    pekora_paths = [
        os.path.expandvars(
            r"%localappdata%\ProjectX\Versions\version-7e043f9d229d4b9a"
        ),
        os.path.expandvars(
            r"%localappdata%\Pekora\Versions\version-7e043f9d229d4b9a"
        )
    ]
    found_paths = [p for p in pekora_paths if os.path.exists(p)]

    if found_paths:
        print(Fore.GREEN + "Pekora found at:")
        for p in found_paths:
            print(" - " + p)
    else:
        print(Fore.RED + "Pekora not found in known paths.")

    # system info
    os_name = platform.system()
    os_version = platform.version()
    cpu = platform.processor() or "Unknown CPU"

    print(Fore.CYAN + f"Operating System: {os_name} {os_version}")
    print(Fore.CYAN + f"CPU: {cpu}")

    print(Fore.MAGENTA + "==========================")
    press_any_key()


def main_menu():
    while True:
        clear()

        # Gradient colors from #07C8F9 to #0D41E1 (hex)
        gradient = [
            (7, 200, 249),
            (5, 157, 230),
            (4, 123, 220),
            (3, 98, 210),
            (2, 74, 200),
            (1, 58, 195),
            (0, 50, 185),
            (13, 65, 225),
        ]

        ascii_logo = [
            "              __          _______ __                    ",
            " .-----.-----|  |--.-----|   _   |  |_.----.---.-.-----. ",
            " |  _  |  -__|    <|  _  |   1___|   _|   _|  _  |  _  | ",
            " |   __|_____|__|__|_____|____   |____|__| |___._|   __| ",
            " |__|                    |:  1   |               |__|    ",
            "                         |::.. . |                       ",
            "                         `-------'                       "
        ]

        for (r, g, b), line in zip(gradient, ascii_logo):
            print(f"\033[38;2;{r};{g};{b}m{line}\033[0m")

        print()
        print(Fore.YELLOW + "Select your option:")
        print(Fore.GREEN + "1 - 2017 (WIP)")
        print(Fore.GREEN + "2 - 2018 (WIP)")
        print(Fore.GREEN + "3 - 2020")
        print(Fore.GREEN + "4 - 2021")
        print(Fore.YELLOW + "5 - Set FastFlags (WIP)")  
        print(Fore.RED + "0 - Exit")
        
        choice = input(Fore.WHITE + "\nEnter your choice: ")
        
        if choice == "1":
            wip_message("2017")
        elif choice == "2":
            wip_message("2018")
        elif choice == "3":
            launch_version("2020L")
        elif choice == "4":
            launch_version("2021M")
        elif choice == "5":
            ask_fastflags()  # wip fflags
        elif choice == "debug":
            debug()
        elif choice == "0":
            print(Fore.CYAN + "Goodbye!")
            sys.exit()
        else:
            print(Fore.RED + "Invalid choice! Try again.")
            press_any_key()


def wip_message(version):
    clear()
    print(Fore.RED + f"{version} is Work in Progress, this option is currently unavailable.")
    press_any_key()

def launch_version(folder):
    clear()
    
    # fallback idk wwhat im diignngnggnng
    paths = [
        os.path.expandvars(
            fr"%localappdata%\ProjectX\Versions\version-7e043f9d229d4b9a\{folder}\ProjectXPlayerBeta.exe"
        ),
        os.path.expandvars(
            fr"%localappdata%\Pekora\Versions\version-7e043f9d229d4b9a\{folder}\ProjectXPlayerBeta.exe"
        )
    ]

    # huh
    fastflags = load_fastflags()
    flags_list = [f"{k}={v}" for k, v in fastflags.items()]
    
    if fastflags:
        print(Fore.YELLOW + f"[*] Note: {len(fastflags)} fastflag(s) loaded but not applied (WIP feature)")
    
    print(Fore.CYAN + f"Launching {folder}...")

    # tries paths
    exe_path = None
    for path in paths:
        if os.path.isfile(path):
            exe_path = path
            break

    if exe_path:
        try:
            args = [exe_path, "--app"]
            if flags_list:
                args.extend(flags_list)
            subprocess.Popen(args)
        except Exception as e:
            print(Fore.RED + f"Error while launching:\n{e}")
    else:
        print(Fore.RED + "Could not find executable. Error code: EXECNFOUND")
    
    press_any_key()


if __name__ == "__main__":
    main_menu()
