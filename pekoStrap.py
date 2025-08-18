import os
import subprocess
import sys
from colorama import Fore, Style, init

# Init colorama
init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main_menu():
    while True:
        clear()
        print(Fore.CYAN + "=== Welcome to pekoStrap ===")
        print(Fore.YELLOW + "Select your version:")
        print(Fore.GREEN + "1 - 2017 (WIP)")
        print(Fore.GREEN + "2 - 2018 (WIP)")
        print(Fore.GREEN + "3 - 2020")
        print(Fore.GREEN + "4 - 2021")
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
        elif choice == "0":
            print(Fore.CYAN + "Goodbye!")
            sys.exit()
        else:
            print(Fore.RED + "Invalid choice! Try again.")
            input("Press any key to continue...")

def wip_message(version):
    clear()
    print(Fore.RED + f"{version} is Work in Progress, this option is currently unavailable.")
    input(Fore.MAGENTA + "Press any key to go back to main menu...")

def launch_version(folder):
    clear()
    path = os.path.expandvars(
        fr"%localappdata%\ProjectX\Versions\version-29f22ac5f5de4484\{folder}\ProjectXPlayerBeta.exe"
    )
    print(Fore.CYAN + f"Launching {folder}...")
    try:
        subprocess.Popen([path, "--app"])
    except FileNotFoundError:
        print(Fore.RED + f"Could not find executable at:\n{path}")
    input(Fore.MAGENTA + "Press any key to go back to main menu...")

if __name__ == "__main__":
    main_menu()
