#!/usr/bin/env python3
"""
move_to_wiistorage.py
Moves files from a USB drive named 'USBA' to one named 'WIISTORAGE'.
Files that already exist on WIISTORAGE are skipped (not overwritten or deleted).
Designed to run on a Raspberry Pi 3.
"""

import os
import shutil
import sys

# --- Configuration ---
SOURCE_LABEL = "USBA"
DEST_LABEL = "WIISTORAGE"
MEDIA_BASE = "/media/pi"  # Default mount point on Raspberry Pi OS
# ---------------------


def find_mount(label: str) -> str | None:
    """Return the mount path for a drive with the given label, or None."""
    path = os.path.join(MEDIA_BASE, label)
    if os.path.ismount(path):
        return path
    return None


def move_files(source_root: str, dest_root: str) -> None:
    """
    Walk source_root and move every file to the matching location in dest_root.
    Files that already exist at the destination are skipped.
    Empty directories left behind in source are removed.
    """
    moved = 0
    skipped = 0
    errors = 0

    for dirpath, dirnames, filenames in os.walk(source_root, topdown=True):
        # Build the equivalent destination directory path
        rel_dir = os.path.relpath(dirpath, source_root)
        dest_dir = os.path.join(dest_root, rel_dir)

        for filename in filenames:
            src_file = os.path.join(dirpath, filename)
            dest_file = os.path.join(dest_dir, filename)

            if os.path.exists(dest_file):
                print(f"  [SKIP]  Already exists: {os.path.join(rel_dir, filename)}")
                skipped += 1
                continue

            try:
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(src_file, dest_file)
                print(f"  [MOVED] {os.path.join(rel_dir, filename)}")
                moved += 1
            except Exception as exc:
                print(f"  [ERROR] Could not move {src_file}: {exc}")
                errors += 1

    # Clean up empty directories left on the source drive
    for dirpath, dirnames, filenames in os.walk(source_root, topdown=False):
        if dirpath == source_root:
            continue
        try:
            os.rmdir(dirpath)  # Only removes if empty
        except OSError:
            pass  # Not empty — leave it

    print(f"\nDone. Moved: {moved}  |  Skipped (already exist): {skipped}  |  Errors: {errors}")


def main() -> None:
    print(f"Looking for '{SOURCE_LABEL}' and '{DEST_LABEL}' under {MEDIA_BASE} ...\n")

    source = find_mount(SOURCE_LABEL)
    dest = find_mount(DEST_LABEL)

    if source is None:
        print(f"ERROR: Could not find USB drive mounted at '{os.path.join(MEDIA_BASE, SOURCE_LABEL)}'")
        print("Make sure the drive is plugged in and its label matches exactly.")
        sys.exit(1)

    if dest is None:
        print(f"ERROR: Could not find USB drive mounted at '{os.path.join(MEDIA_BASE, DEST_LABEL)}'")
        print("Make sure the drive is plugged in and its label matches exactly.")
        sys.exit(1)

    print(f"Source : {source}")
    print(f"Dest   : {dest}\n")

    move_files(source, dest)


if __name__ == "__main__":
    main()