from __future__ import annotations
import os
import shutil
from pathlib import Path

def copy_no_delete(src: Path, dst: Path, overwrite: bool = False) -> tuple[int, int, int]:
    """
    Copy files from src -> dst recursively.
    - Never deletes anything in dst.
    - If overwrite=False, skips files that already exist in dst.
    Returns: (copied_files, skipped_files, error_files)
    """
    copied = skipped = errors = 0

    src = src.resolve()
    dst = dst.resolve()

    if not src.exists() or not src.is_dir():
        raise ValueError(f"Source folder not found: {src}")

    dst.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(src):
        root_path = Path(root)
        rel = root_path.relative_to(src)
        target_dir = dst / rel
        target_dir.mkdir(parents=True, exist_ok=True)

        for name in files:
            s = root_path / name
            d = target_dir / name
            try:
                if d.exists() and not overwrite:
                    skipped += 1
                    continue
                shutil.copy2(s, d)
                copied += 1
            except Exception:
                errors += 1

    return copied, skipped, errors
