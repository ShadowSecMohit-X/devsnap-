# DevSnap-
time saving project for developers 

INTRODUCTION OF PROJECT --

DevSnap --- a developer tool that saves a snapshot of your active workspace (open folders, links/tabs and terminal commands) and allow you to restore it with a single command or click 

WHY I'M BUILDING IT ----

When you shut down your development setup after finishing your work , you might not remember exactly which files or tabs you had open when you return and start it up again. This is where DevSnap comes in by clicking on "snapshot" it captures the state of your workspace. When you return later, a single click restores all those same files, tabs and links. This save developers time and eliminates the need to manually keep track of which files and tabs were previously open. 

PLANNED FEATURES ---

1 Saving a workspace snapshot (with a custom profile name)
2 viewing alist of saved snapshots 
3 instantly restoring any snapshot 
4 deleting or updating old snapshot

## PROJECT STRUCTURE

- `storage.py` - Local JSON storage helper for saving and loading snapshots.
- `snapshot_ops.py` - Core logic for saving, listing, restoring, and deleting snapshots.
  - `devsnap.py` - CLI entry point for handling user commands.

 ## USAGE 

 ```bash
python3 devsnap.ppy save <name>
python3 devsnap.py list 
python3 devsnap.py restore <name>
python3 devsnap.py delete <name>
