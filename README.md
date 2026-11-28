# DevSnap

**DevSnap** is a lightweight pytho CLI tool to save and quickly restore developer workspaces-including workspace folder, refrence URLs, and terminal commmands-using a local JSON store.

## Project Sturcture

- `devsnap.py`- CLI entry poitn and argument/command routing (`save`, `list`, `resotre`, `delete`, `help`).
- `snapshot_ops.py` - core logic for saving listing, restoring, and deleting snapshots.
- `storage.py` - JSON file read/write helper for presisting snapshot locally.


## usage

Run commands from the project folder:

``` bash 
python3 devsnap.py save work
python3 devsnap.py list 
python3 devsnap.py restore work 
python3 devsnap.py delete work


FEATURES-->

1 Save named workspace snapshots woth an optional folder path, URLs and setup commands

2 List all saved snapshot bu opening the target folder,launching and item. counts.

3 Resotre a workspace by opening the target folder,alaunching saved URls, and optionally running saved commands.

4 Delete snapshots that are no linger needed.


work in progresss ---- sorry for the dealy 
