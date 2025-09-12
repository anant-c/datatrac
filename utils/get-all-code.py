import os

# Default ignores (common junk / non-code directories & files)
DEFAULT_IGNORES = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".DS_Store",
    "Thumbs.db",
    ".venv",
    "venv",
    "env",
    ".coverage",
    ".tox",
    "node_modules",
}


def load_list(filename, defaults=None):
    """Load a list from a txt file."""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)

    entries = set(defaults) if defaults else set()
    if os.path.isfile(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    entry = line.strip()
                    if entry and not entry.startswith("#"):
                        entries.add(entry)
        except Exception as e:
            print(f"⚠️ Could not read {filename}: {e}")
    return entries


def save_entry(filename, entry):
    """Append a new entry to a txt file."""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception as e:
        print(f"⚠️ Could not save to {filename}: {e}")


def main():
    # Ask for input folder
    root_dir = input("Enter the root folder path to scan: ").strip()
    if not os.path.isdir(root_dir):
        print("Invalid folder path. Exiting.")
        return

    output_file = os.path.join(os.path.dirname(__file__), "collected_code.txt")

    ignore_entries = load_list("ignore_list.txt", DEFAULT_IGNORES)
    allow_entries = load_list("allow_list.txt")

    with open(output_file, "w", encoding="utf-8") as out:
        walk_directory(root_dir, out, root_dir, ignore_entries, allow_entries)

    print(f"\n✅ Done! Code has been written to {output_file}")


def walk_directory(current_dir, out, root_dir, ignore_entries, allow_entries):
    """Recursively walk through a directory with user prompts and ignore/allow rules."""
    rel_dir = os.path.relpath(current_dir, root_dir)
    if rel_dir == ".":
        rel_dir = os.path.basename(root_dir)

    # Ignore folders
    if rel_dir in ignore_entries or os.path.basename(current_dir) in ignore_entries:
        print(f"🚫 Ignored folder '{rel_dir}' (ignore list)")
        return

    # Allow folders silently
    if rel_dir in allow_entries or os.path.basename(current_dir) in allow_entries:
        choice = "y"
    else:
        choice = input(f"\nExplore folder '{rel_dir}'? (y/n): ").strip().lower()
        if choice == "y":
            save_entry("allow_list.txt", rel_dir)

    if choice != "y":
        print(f"⏭ Skipping folder '{rel_dir}'")
        return

    try:
        entries = sorted(os.listdir(current_dir))
    except PermissionError:
        print(f"⚠️ Permission denied: {current_dir}")
        return

    for entry in entries:
        path = os.path.join(current_dir, entry)

        if os.path.isdir(path):
            walk_directory(path, out, root_dir, ignore_entries, allow_entries)

        elif entry.endswith(".py"):
            rel_path = os.path.relpath(path, root_dir)

            # Ignore files
            if rel_path in ignore_entries or entry in ignore_entries:
                print(f"🚫 Ignored file '{rel_path}' (ignore list)")
                continue

            # Allow files silently
            if rel_path in allow_entries or entry in allow_entries:
                file_choice = "y"
            else:
                file_choice = input(f"Include file '{rel_path}'? (y/n): ").strip().lower()
                if file_choice == "y":
                    save_entry("allow_list.txt", rel_path)

            if file_choice == "y":
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        code = f.read()
                    out.write(f"\n=== {rel_path} ===\n")
                    out.write(code + "\n")
                    print(f"✅ Recorded {rel_path}")
                except Exception as e:
                    print(f"⚠️ Could not read {rel_path}: {e}")
            else:
                print(f"⏭ Skipped file '{rel_path}'")


if __name__ == "__main__":
    main()
