import os
import webbrowser
import subprocess
import sys
import json
import platform
from colorama import Fore, Style, init
from pystyle import Colorate, Colors

os.system("title ShunStrap")

# Init colorama
init(autoreset=False)

FASTFLAGS_FILE = "fastFlags.json"  # fflags

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

def get_system_info():
    """Get system information for cross-platform compatibility"""
    system = platform.system().lower()
    return {
        'is_windows': system == 'windows',
        'is_linux': system == 'linux',
        'is_macos': system == 'darwin',
        'system_name': system
    }

def get_installation_paths():
    """Get platform-specific installation paths"""
    sys_info = get_system_info()
    
    if sys_info['is_windows']:
        return [
            os.path.expandvars(r"%localappdata%\ProjectX\Versions\version-2"),
            os.path.expandvars(r"%localappdata%\Pekora2\Versions\version-2")
        ]
    elif sys_info['is_linux']:
        # Linux with Wine
        user = os.getenv('USER', 'user')
        return [
            os.path.expanduser(f"~/.wine/drive_c/users/{user}/AppData/Local/ProjectX/Versions/version-1"),
            os.path.expanduser(f"~/.wine/drive_c/users/{user}/AppData/Local/Pekora/Versions/version-1"),
            # Alternative Wine prefix locations
            os.path.expanduser(f"~/.local/share/wineprefixes/pekora/drive_c/users/{user}/AppData/Local/Pekora/Versions/version-1"),
            os.path.expanduser(f"~/.local/share/wineprefixes/projectx/drive_c/users/{user}/AppData/Local/ProjectX/Versions/version-1")
        ]
    elif sys_info['is_macos']:
        # macOS with Wine/CrossOver/Parallels
        user = os.getenv('USER', 'user')
        return [
            # Wine on macOS
            os.path.expanduser(f"~/.wine/drive_c/users/{user}/AppData/Local/ProjectX/Versions/version-1"),
            os.path.expanduser(f"~/.wine/drive_c/users/{user}/AppData/Local/Pekora/Versions/version-1"),
            # CrossOver
            os.path.expanduser(f"~/Library/Application Support/CrossOver/Bottles/*/drive_c/users/{user}/AppData/Local/ProjectX/Versions/version-1"),
            os.path.expanduser(f"~/Library/Application Support/CrossOver/Bottles/*/drive_c/users/{user}/AppData/Local/Pekora/Versions/version-1"),
            # Parallels (if running Windows VM)
            os.path.expanduser(f"~/Parallels/*.pvm/Windows*/Users/{user}/AppData/Local/ProjectX/Versions/version-1"),
            os.path.expanduser(f"~/Parallels/*.pvm/Windows*/Users/{user}/AppData/Local/Pekora/Versions/version-1")
        ]
    else:
        print(Fore.YELLOW + f"[!] Unsupported system: {sys_info['system_name']}")
        return []

def get_executable_paths(folder):
    """Get platform-specific executable paths"""
    sys_info = get_system_info()
    base_paths = get_installation_paths()
    exe_paths = []
    
    for base_path in base_paths:
        if sys_info['is_windows']:
            exe_paths.append(os.path.join(base_path, folder, "ProjectXPlayerBeta.exe"))
        else:
            # Linux/macOS with Wine - same executable name but different execution method
            exe_paths.append(os.path.join(base_path, folder, "ProjectXPlayerBeta.exe"))
    
    return exe_paths

def get_fps_unlocker_paths():
    """Get platform-specific FPS unlocker paths"""
    sys_info = get_system_info()
    
    if sys_info['is_windows']:
        return [
            "pekorafpsunlocker.exe",
            os.path.join(os.path.dirname(sys.executable), "pekorafpsunlocker.exe"),
            os.path.join(os.getcwd(), "pekorafpsunlocker.exe")
        ]
    else:
        # For Linux/macOS, also check for the exe to run with Wine
        return [
            "pekorafpsunlocker.exe",
            os.path.join(os.path.dirname(sys.executable), "pekorafpsunlocker.exe"),
            os.path.join(os.getcwd(), "pekorafpsunlocker.exe"),
            # Also check for potential native versions
            "pekorafpsunlocker",
            "./pekorafpsunlocker"
        ]

def load_fastflags():
    if not os.path.exists(FASTFLAGS_FILE):
        with open(FASTFLAGS_FILE, "w") as f:
            json.dump({}, f)
        return {}
    try:
        with open(FASTFLAGS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(Fore.RED + "[!] Error reading fastFlags.json - invalid JSON format")
        return {}

def save_fastflags(fastflags):
    try:
        with open(FASTFLAGS_FILE, "w") as f:
            json.dump(fastflags, f, indent=2)
        print(Fore.GREEN + "[*] FastFlags saved successfully!")
    except Exception as e:
        print(Fore.RED + f"[!] Failed to save FastFlags: {e}")

def apply_fastflags(fastflags):
    success = False
    exe_paths = get_installation_paths()
    
    for base_path in exe_paths:
        if os.path.exists(base_path):
            # version folderz
            for folder in ["2020L", "2021M"]:
                folder_path = os.path.join(base_path, folder)
                if os.path.exists(folder_path):
                    # ty zyth for helpinggg <3
                    client_settings_dir = os.path.join(folder_path, "ClientSettings")
                    try:
                        os.makedirs(client_settings_dir, exist_ok=True)
                        
                        settings_path = os.path.join(client_settings_dir, "ClientAppSettings.json")
                        
                        if os.path.exists(settings_path):
                            os.remove(settings_path)
                        
                        with open(settings_path, "w") as f:
                            json.dump(fastflags, f, indent=2)
                        print(Fore.GREEN + f"[*] Applied FastFlags to {folder}/ClientSettings")
                        print(Fore.CYAN + f"[*] Location: {settings_path}")
                        success = True
                    except Exception as e:
                        print(Fore.RED + f"[!] Failed to write to {folder}: {e}")
    
    return success

def auto_detect_value_type(value_str):
    value_str = value_str.strip()
    
    # boooooooolean
    if value_str.lower() in ['true', 'false']:
        return value_str.lower() == 'true'
    
    # int 
    try:
        if '.' not in value_str and 'e' not in value_str.lower():
            return int(value_str)
    except ValueError:
        pass
    
    # fLOATIES
    try:
        return float(value_str)
    except ValueError:
        pass
    
    # string
    return value_str

def ask_fastflags():
    while True:
        clear()
        print(Fore.YELLOW + "FastFlags Configuration")
        fastflags = load_fastflags()
        
        if fastflags:
            print(Fore.CYAN + "Current FFlags:")
            for i, (k, v) in enumerate(fastflags.items(), 1):
                value_type = type(v).__name__
                print(Fore.YELLOW + f" {i}. {k} = {v} ({value_type})")
        else:
            print(Fore.MAGENTA + "No fflags set yet")
        
        print(Fore.GREEN + "\nOptions:")
        print("1. Add a FastFlag")
        print("2. Remove a FastFlag") 
        print("3. Clear all FastFlags")
        print("4. Apply FastFlags")
        print("5. Import FastFlags from JSON")
        print("0. Back to main menu")
        
        choice = input(Fore.WHITE + "\nEnter choice: ").strip()
        
        if choice == "1":
            add_fastflag(fastflags)
        elif choice == "2":
            remove_fastflag(fastflags)
        elif choice == "3":
            clear_fastflags()
        elif choice == "4":
            if fastflags:
                if apply_fastflags(fastflags):
                    print(Fore.GREEN + "[*] FastFlags applied successfully.")
                else:
                    print(Fore.RED + "[!] Failed to apply FastFlags")
            else:
                print(Fore.YELLOW + "[*] No FastFlags to apply")
            press_any_key()
        elif choice == "5":
            import_fastflags()
        elif choice == "0":
            break
        else:
            print(Fore.RED + "Invalid choice!")
            press_any_key()

def add_fastflag(fastflags):
    print(Fore.GREEN + "\nAdd New FastFlag:")
    print(Fore.CYAN + "Tip: Values are auto-converted.")
    print(Fore.CYAN + "Common example:")
    print(Fore.YELLOW + "  FFlagDebugGraphicsDisableMetal = true")
    
    key = input(Fore.WHITE + "\nKey: ").strip()
    if not key:
        print(Fore.RED + "[*] Cancelled - no key provided")
        press_any_key()
        return
    
    value_input = input(Fore.WHITE + "Value: ").strip()
    if value_input == "":
        print(Fore.RED + "[*] Cancelled - no value provided")
        press_any_key()
        return
    
    value = auto_detect_value_type(value_input)
    fastflags[key] = value
    save_fastflags(fastflags)
    
    value_type = type(value).__name__
    print(Fore.GREEN + f"[*] Added FastFlag: {key} = {value} ({value_type})")
    press_any_key()

def remove_fastflag(fastflags):
    if not fastflags:
        print(Fore.YELLOW + "[*] No FastFlags to remove")
        press_any_key()
        return
    
    print(Fore.YELLOW + "\nRemove FastFlag:")
    key = input(Fore.WHITE + "Enter key to remove: ").strip()
    
    if key in fastflags:
        del fastflags[key]
        save_fastflags(fastflags)
        print(Fore.GREEN + f"[*] Removed FastFlag: {key}")
    else:
        print(Fore.RED + f"[!] FastFlag '{key}' not found")
    
    press_any_key()

def clear_fastflags():
    confirm = input(Fore.RED + "Are you sure you want to clear ALL FastFlags? (y/N): ").strip().lower()
    if confirm == 'y':
        save_fastflags({})
        print(Fore.GREEN + "[*] All FastFlags cleared")
    else:
        print(Fore.YELLOW + "[*] Cancelled")
    press_any_key()

def import_fastflags():
    print(Fore.CYAN + "\nImport FastFlags from JSON:")
    print(Fore.YELLOW + "Example format: {\"FFlagDebugGraphicsDisableMetal\": true, \"DFIntTaskSchedulerTargetFps\": 144}")
    print(Fore.YELLOW + "Paste JSON content and press Enter twice when done:")
    
    lines = []
    empty_count = 0
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 2 or (len(lines) > 0 and lines[-1] == ""):
                break
        else:
            empty_count = 0
        lines.append(line)
    
    # idk waht this does smb told me to addd
    while lines and lines[-1] == "":
        lines.pop()
    
    json_text = "\n".join(lines)
    
    if not json_text.strip():
        print(Fore.YELLOW + "[*] No content provided")
        press_any_key()
        return
    
    try:
        imported_flags = json.loads(json_text)
        if not isinstance(imported_flags, dict):
            print(Fore.RED + "[!] JSON must be an object/dictionary")
            press_any_key()
            return
        
        current_flags = load_fastflags()
        current_flags.update(imported_flags)
        save_fastflags(current_flags)
        
        print(Fore.GREEN + f"[*] Imported {len(imported_flags)} FastFlag(s)")
        for k, v in imported_flags.items():
            print(Fore.CYAN + f"  + {k} = {v}")
            
    except json.JSONDecodeError as e:
        print(Fore.RED + f"[!] Invalid JSON format: {e}")
    
    press_any_key()

def launch_fps_unlocker():
    clear()
    sys_info = get_system_info()
    print(Fore.CYAN + "Enable FPS Unlock")
    
    # check for unlockerrrr
    fps_unlocker_paths = get_fps_unlocker_paths()
    
    exe_path = None
    for path in fps_unlocker_paths:
        if os.path.isfile(path):
            exe_path = path
            break
    
    if exe_path:
        try:
            print(Fore.YELLOW + "[*] Launching FPS Unlocker...")
            
            if sys_info['is_windows']:
                subprocess.Popen([exe_path])
            elif sys_info['is_linux']:
                # Try Wine first, then native if available
                if exe_path.endswith('.exe'):
                    subprocess.Popen(["wine64", exe_path])
                else:
                    subprocess.Popen([exe_path])
            elif sys_info['is_macos']:
                # macOS with wine or native
                if exe_path.endswith('.exe'):
                    # try Wine on macOS
                    subprocess.Popen(["wine64", exe_path])
                else:
                    subprocess.Popen([exe_path])
            
            print(Fore.GREEN + "[*] FPS Unlocker launched successfully!")
        except Exception as e:
            print(Fore.RED + f"Error while launching FPS Unlocker:\n{e}")
            if not sys_info['is_windows']:
                print(Fore.YELLOW + "Make sure Wine is installed and configured properly.")
    else:
        print(Fore.RED + "Could not find pekorafpsunlocker.exe")
        print(Fore.YELLOW + "Searched paths:")
        for path in fps_unlocker_paths:
            print(Fore.YELLOW + f"  - {path}")
    
    press_any_key()

def debug():
    clear()
    sys_info = get_system_info()
    print(Fore.MAGENTA + "Debug info")

    # check paths
    base_paths = get_installation_paths()
    
    print(Fore.CYAN + "Checking installation paths:")
    for base_path in base_paths:
        if os.path.exists(base_path):
            print(Fore.GREEN + f"  ✓ Found: {base_path}")
            versions_path = os.path.join(base_path, "Versions")
            if os.path.exists(versions_path):
                versions = [d for d in os.listdir(versions_path) if os.path.isdir(os.path.join(versions_path, d))]
                for version in versions:
                    print(Fore.YELLOW + f"    - Version: {version}")
        else:
            print(Fore.RED + f"  ✗ Not found: {base_path}")
    
    # check ClientSettings
    exe_paths = get_installation_paths()
    
    print(Fore.CYAN + f"\nClientSettings status:")
    for base_path in exe_paths:
        if os.path.exists(base_path):
            for folder in ["2020L", "2021M"]:
                folder_path = os.path.join(base_path, folder)
                if os.path.exists(folder_path):
                    client_settings_dir = os.path.join(folder_path, "ClientSettings")
                    settings_file = os.path.join(client_settings_dir, "ClientAppSettings.json")
                    print(Fore.YELLOW + f"{folder} ClientSettings: {settings_file}")
                    if os.path.exists(settings_file):
                        print(Fore.GREEN + "  ✓ Exists")
                        try:
                            with open(settings_file, 'r') as f:
                                settings = json.load(f)
                            print(Fore.CYAN + f"  Active FastFlags: {len(settings)}")
                            if settings:
                                print(Fore.YELLOW + "  Current flags:")
                                for k, v in list(settings.items())[:3]:  # Show first 3
                                    print(Fore.CYAN + f"    {k} = {v}")
                                if len(settings) > 3:
                                    print(Fore.CYAN + f"    ... and {len(settings) - 3} more")
                        except Exception as e:
                            print(Fore.RED + f"  ✗ Error reading: {e}")
                    else:
                        print(Fore.RED + "  ✗ Not found")

    # fastflags file
    print(Fore.CYAN + f"\nLocal FastFlags file: {FASTFLAGS_FILE}")
    if os.path.exists(FASTFLAGS_FILE):
        print(Fore.GREEN + "  ✓ Exists")
        try:
            local_flags = load_fastflags()
            print(Fore.CYAN + f"  Stored FastFlags: {len(local_flags)}")
        except:
            print(Fore.RED + "  ✗ Error reading local file")
    else:
        print(Fore.RED + "  ✗ Not found")

    # Wine check for non-Windows systems
    if not sys_info['is_windows']:
        print(Fore.CYAN + f"\nWine Configuration:")
        try:
            wine_version = subprocess.check_output(["wine64", "--version"], stderr=subprocess.DEVNULL).decode().strip()
            print(Fore.GREEN + f"  ✓ Wine installed: {wine_version}")
        except:
            try:
                wine_version = subprocess.check_output(["wine", "--version"], stderr=subprocess.DEVNULL).decode().strip()
                print(Fore.GREEN + f"  ✓ Wine installed: {wine_version}")
            except:
                print(Fore.RED + "  ✗ Wine not found - required for running Windows executables") # BRO I KEEP SPENDING 5 MINUTES TRYING TO FIND THESE SYMBOLS

    print(Fore.CYAN + f"\nSystem Information:")
    print(Fore.YELLOW + f"OS: {platform.system()} {platform.release()}")
    print(Fore.YELLOW + f"Architecture: {platform.machine()}")
    print(Fore.YELLOW + f"CPU: {platform.processor() or 'Unknown'}")
    print(Fore.YELLOW + f"Python: {sys.version.split()[0]}")
    
    if sys_info['is_linux']:
        # distro info for the linux people
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read()
                for line in os_info.split('\n'):
                    if line.startswith('PRETTY_NAME='):
                        distro = line.split('=')[1].strip('"')
                        print(Fore.YELLOW + f"Distribution: {distro}")
                        break
        except:
            pass

    print(Fore.MAGENTA + "=" * 50)
    press_any_key()

def main_menu():
    while True:
        clear()
        sys_info = get_system_info()

        ascii_logo = """   
  ______             ______               
 / __/ /  __ _____  / __/ /________ ____  
 _\ \/ _ \/ // / _ \_\ \/ __/ __/ _ `/ _ \ 
/___/_//_/\_,_/_//_/___/\__/_/  \_,_/ .__/ 
                                /_/     
        """


        print(Colorate.Horizontal(Colors.blue_to_cyan, ascii_logo))

        print(Fore.BLUE + "Made with <3 by shun on pekora.org")
        print(Fore.LIGHTBLACK_EX + "UI was tweaked by @cinnamon on pekora.org and dc ;)")
        
        # platform info
        platform_name = "Windows" if sys_info['is_windows'] else ("Linux" if sys_info['is_linux'] else ("macOS" if sys_info['is_macos'] else "Unknown"))
        print(Fore.CYAN + f"OS: {platform_name}")
        if not sys_info['is_windows']:
            print(Fore.YELLOW + "Note: Wine is required for Windows executables")
        
        menu_text = """
╔══════════════════════════════════╗
║  1 | LAUNCH 2017 [NOT WORKING]   ║
║  2 | LAUNCH 2018 [NOT WORKING]   ║
║  3 | LAUNCH 2020                 ║
║  4 | LAUNCH 2021                 ║
║  5 | Set FastFlags For Pekora    ║
║  6 | Enable FPS Unlock           ║
║  7 | Join Discord                ║
║  0 | Exit Bootstrapper           ║
╚══════════════════════════════════╝

"""
        print(Colorate.Vertical(Colors.blue_to_cyan, menu_text))
        
        choice = input(Fore.LIGHTBLUE_EX + "\n>> ")
        
        if choice == "1":
            wip_message("2017")
        elif choice == "2":
            wip_message("2018")
        elif choice == "3":
            launch_version("2020L")
        elif choice == "4":
            launch_version("2021M")
        elif choice == "5":
            ask_fastflags()
        elif choice == "6":
            launch_fps_unlocker()
        elif choice == "debug":
            debug()
        elif choice == "7":
         webbrowser.open("https://discord.gg/pvvKxJ78yU")      
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
    sys_info = get_system_info()
    
    # check paths
    paths = get_executable_paths(folder)

    # Apply FastFlags
    fastflags = load_fastflags()
    if fastflags:
        print(Fore.CYAN + f"[*] Applying {len(fastflags)} FastFlag(s)...")
        if apply_fastflags(fastflags):
            print(Fore.GREEN + "[*] FastFlags applied successfully!")
        else:
            print(Fore.RED + "[!] Failed to apply FastFlags")
    else:
        print(Fore.YELLOW + "[*] No FastFlags configured")

    print(Fore.CYAN + f"Launching {folder}...")

    exe_path = None
    for path in paths:
        if os.path.isfile(path):
            exe_path = path
            break
    # idk i just copied some stuff of stack overflow
    if exe_path:
        try:
            if sys_info['is_windows']:
                subprocess.Popen([exe_path, "--app"])
            elif sys_info['is_linux']:
                subprocess.Popen([
                    "env",
                    "__NV_PRIME_RENDER_OFFLOAD=1",
                    "__GLX_VENDOR_LIBRARY_NAME=nvidia",
                    "wine64", exe_path, "--app"
                ])
            elif sys_info['is_macos']:
                # macOS with Wine
                subprocess.Popen(["wine64", exe_path, "--app"])
            
            print(Fore.GREEN + "[*] Launch successful!")
        except Exception as e:
            print(Fore.RED + f"Error while launching:\n{e}")
            if not sys_info['is_windows']:
                print(Fore.YELLOW + "Make sure Wine is installed and configured properly.")
    else:
        print(Fore.RED + "Could not find executable. Error code: EXECNFOUND")
        print(Fore.YELLOW + "Searched paths:")
        for path in paths:
            print(Fore.YELLOW + f"  - {path}")
        
        if not sys_info['is_windows']:
            print(Fore.CYAN + "\nTroubleshooting tips:")
            print(Fore.YELLOW + "- Make sure Wine is installed")
            print(Fore.YELLOW + "- Verify your Wine prefix is configured")
            print(Fore.YELLOW + "- Check that the game is installed in the Wine prefix")

    press_any_key()

if __name__ == "__main__":
    main_menu()
