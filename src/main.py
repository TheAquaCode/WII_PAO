from __future__ import annotations

import argparse
from pathlib import Path
from datetime import datetime

from sync_copy import copy_no_delete

LOG_FILE = Path("logs/copy.log")


def log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Copy files from a USB source to a USB-C destination without deleting data."
    )
    p.add_argument(
        "--src",
        default="test_data/usb_source",
        help="Source folder (default: test_data/usb_source)",
    )
    p.add_argument(
        "--dst",
        default="test_data/usbc_destination",
        help="Destination folder (default: test_data/usbc_destination)",
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite destination files if they already exist (default: skip existing)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    src = Path(args.src)
    dst = Path(args.dst)

    log(f"START copy src={src} dst={dst} overwrite={args.overwrite}")
    copied, skipped, errors = copy_no_delete(src, dst, overwrite=args.overwrite)
    log(f"RESULT copied={copied} skipped={skipped} errors={errors}")
    log("END copy")

    print(f"Copied: {copied}, Skipped: {skipped}, Errors: {errors}")


if __name__ == "__main__":
    main()
