import sys
from snapshot_ops import (
    list_snapshots,
    save_snapshot,
    restore_snapshot,
    delete_snapshot,
)

def show_help():
    print("\nDevSnap - workspace & Quick Restore Tool")
    print("commands:")
    print("  save <name>    Save workspace folders, links, and commands")
    print ("   list        show all saved snapshots")
    print ("resotore <name>    restore a saved snapshot")
    print ("    delete <name>    delete a saved snapshot\n")


def prompt_items(label):
    raw = input(f"{label} (comma-separated, optional): ").strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def handle_save(args):
    if not args:
        print("Error: Please enter a snapshot name. example: save work")
        return

    name = args[0]
    folder_path = input("workspace folder path: (optional): ").strip()
    urls = prompt_items("URLs/tabs to open")
    commands = prompt_items("terminal commands to run")

    save_snapshot(name, folder_path, urls, commands)


def handle_restore(args):
    if not args:
        print("Error: Please provide a snapshot. Exmaple: restore work")
        return 
    restore_snapshot(args[0])


def handle_delete(args):
    if not args:
        print("Error: Please provide a snapshot. Exmaple: delete work")
        return 
    delete_snapshot(args[0])


def main():
    if len(sys.argv) <2:
        show_help()
        return

    command = sys.argv[1].lower()
    rest_args = sys.argv[2:]

    if command == "help":
        show_help()
    elif command == "save":
        handle_save(rest_args)
    elif command == "list":
        list_snapshots()
    elif command == "restore":
        handle_restore(rest_args)
    elif command == "delete":
        handle_delete(rest_args)
    else:
        print(f"Feature '{command}' is planned next.")


if __name__ == "__main__":
    main()
