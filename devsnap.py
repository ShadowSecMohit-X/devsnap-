import sys
from snapshot_ops import (
    list_snapshots,
    save_snapshot,
    restore_snapshot,
    delete_snapshot,
)

def show_help():
    print("\nDevSnap - Auto Workspace Snapshot & Restore")
    print("  python3 devsnap.py snap [name]     Auto-capture active folders, tabs & commands")
    print("  python3 devsnap.py restore [name]  Instantly restore snapshot")
    print("  python3 devsnap.py list            Show saved snapshots")
    print("  python3 devsnap.py delete <name>   Delete a snapshot\n") 

def main():
    if len(sys.argv) <2: 
        show_help()
        
        return
    cmd = sys.argv[1].lower()
    arg = sys.argv[2] if len(sys.argv) >2 else "latest"

    if cmd in ("snap", "save"):
        save_snapshot(arg)
    elif cmd == "restore":
        restore_snapshot(arg)
    elif cmd == "list":
        list_snapshots()
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("Error: Specify snapshot name to dlete.")
            return 
        delete_snapshot(sys.argv[2])
    else:
        show_help()


if __name__=="__main__":
    main() 