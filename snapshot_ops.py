import os
import subprocess
import webbrowser
from datetime import datetime
from storage import load_snapshots, save_snapshots


def _run_applescript(script):
    try:
        res = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if res.returncode == 0:
            return [line.strip() for line in res.stdout.splitlines() if line.strip()]
    except Exception:
        pass
    return []


def capture_finder_folders():
    script = """
    tell application "Finder"
        set outList to {}
        repeat with w in Finder windows
            try
                set p to POSIX path of (target of w as alias)
                set end of outList to p
            end try
        end repeat
        return outList
    end tell
    """
    return _run_applescript(script)


def capture_browser_urls():
    urls = []
    chrome_script = """
    if application "Google Chrome" is running then
        tell application "Google Chrome"
            set tabUrls to {}
            repeat with w in windows
                repeat with t in tabs of w
                    set end of tabUrls to URL of t
                end repeat
            end repeat
            return tabUrls
        end tell
    end if
    """
    safari_script = """
    if application "Safari" is running then
        tell application "Safari"
            set tabUrls to {}
            repeat with w in windows
                repeat with t in tabs of w
                    try
                        set end of tabUrls to URL of t
                    end try
                end repeat
            end repeat
            return tabUrls
        end tell
    end if
    """
    for raw in _run_applescript(chrome_script) + _run_applescript(safari_script):
        for part in raw.split(", "):
            u = part.strip()
            if u.startswith(("http://", "https://")) and u not in urls:
                urls.append(u)
    return urls[:15]


def capture_recent_commands(limit=5):
    hist_path = os.path.expanduser("~/.zsh_history")
    if not os.path.exists(hist_path):
        hist_path = os.path.expanduser("~/.bash_history")
    if not os.path.exists(hist_path):
        return []

    cmds = []
    try:
        with open(hist_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f.readlines()[-40:]:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(":") and ";" in line:
                    line = line.split(";", 1)[1].strip()
                if not line.startswith("python3 devsnap.py") and line not in cmds:
                    cmds.append(line)
    except OSError:
        return []
    return cmds[-limit:]


def save_snapshot(name="latest"):
    folders = capture_finder_folders()
    urls = capture_browser_urls()
    commands = capture_recent_commands()

    snapshots = load_snapshots()
    snapshots[name] = {
        "folders": folders,
        "urls": urls,
        "commands": commands,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_snapshots(snapshots)

    print(f"\nSnapshot '{name}' auto-captured!")
    print(f"  Folders ({len(folders)}): {folders if folders else 'None detected'}")
    print(f"  URLs ({len(urls)}): {urls if urls else 'None detected'}")
    print(f"  Recent commands ({len(commands)}): {commands if commands else 'None detected'}\n")


def list_snapshots():
    snapshots = load_snapshots()
    if not snapshots:
        print("No snapshots saved yet.")
        return

    print("\nSaved Snapshots:")
    for name, info in snapshots.items():
        created = info.get("created_at", "N/A")
        f_count = len(info.get("folders", []))
        u_count = len(info.get("urls", []))
        c_count = len(info.get("commands", []))
        print(f"  - {name} | Folders: {f_count} | URLs: {u_count} | Commands: {c_count} | {created}")
    print()


def restore_snapshot(name="latest"):
    snapshots = load_snapshots()
    if name == "latest" and name not in snapshots and snapshots:
        name = list(snapshots.keys())[-1]

    if name not in snapshots:
        print(f"Error: Snapshot '{name}' not found.")
        return

    info = snapshots[name]
    print(f"\nRestoring '{name}'...")

    for folder in info.get("folders", []):
        if os.path.exists(folder):
            subprocess.run(["open", folder], check=False)
            print(f"  Opened folder: {folder}")

    for url in info.get("urls", []):
        webbrowser.open(url)
        print(f"  Opened URL: {url}")

    commands = info.get("commands", [])
    if commands:
        print("  Saved commands:")
        for cmd in commands:
            print(f"    $ {cmd}")
    print("Done!\n")


def delete_snapshot(name):
    snapshots = load_snapshots()
    if name not in snapshots:
        print(f"Error: Snapshot '{name}' not found.")
        return
    del snapshots[name]
    save_snapshots(snapshots)
    print(f"Deleted snapshot '{name}'.")