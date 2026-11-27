import os
import subprocess
import sys
import webbrowser
from datetime import datetime 
from storage import load_snapshots, save_snapshots


def save_snapshot(name, folder_path, urls=None, commands=None):
    snapshots = load_snapshots()
    snapshots[name] = {
        "folder": folder_path,
        "urls": urls or [], 
        "commands": commands or [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_snapshots(snapshots)
    print(f"snapshot \"{name}\" saved.")


def list_snapshots():
    snapshots = load_snapshots()
    if not snapshots:
        print("No snapshots found.")
        return

    print("\nSaved Snapshots:")
    for name, info in snapshots.items():
        created = info.get("created_at", "N/A")
        folder = info.get("folder") or "None"
        urls_count = len(info.get("urls", []))
        cmds_count = len(info.get("commands", []))
        print(f"    {name} | Folder: {folder} | URLs: {urls_count} | commands: {cmds_count} | created: {created}")
    print()     


def _open_folder(folder_path):
    expanded = os.path.expanduser(folder_path)
    if not os.path.exists(expanded):
        print(f"warning: Folder not found -> {expanded}")
        return

    try:
        if sys.platform == "darwin":
            subprocess.run(["open", expanded], check=False)
        elif os.name =="nt":
            os.startfile(expanded)
        else:
            subprocess.run(["xdg-open", expanded], check=False)
        print(f"Opened folder: {expanded}")
    except OSError as exc:
        print(f"Could not open folder '{expanded}': {exc}")


def restore_snapshot(name):
    snapshots = load_snapshots()
    if name not in snapshots:
        print(f"Error: snapshot '{name}' not found.")
        return 
    info = snapshots[name]
    print(f"\nRestoring snapshot '{name}'....")


    folder = info.get("folder", "").strip()
    if folder:
        _open_folder(folder)


    for url in info.get("urls", []):
        print(f"Openning URL: {url}")
        webbrowser.open(url)

    commands = info.get("commands", [])
    if commands:
        print("\nSaved terminal commands:")
        for cmd in commands:
            print(f"  $ {cmd}")
        run_choice = input("Run these commands now? (y/N): ").strip().lower()
        if run_choice == "y":
            cwd = os.path.expanduser(folder) if folder and os.path.exists(os.path.expanduser(folder)) else None
            for cmd in commands:
                print(f"Running: {cmd}")
                subprocess.run(cmd, shell=True, cwd=cwd, check=False)

        print(f"Done restoring snapshot '{name}'.\n")


def delete_snapshot(name):
    snapshots = load_snapshots()
    if name not in snapshots:
        print(f"Error: snapshot '{name}' not found.")
        return

    del snapshots[name]
    save_snapshots(snapshots)
    print(f"snapshot '{name}' deleted.")