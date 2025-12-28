#!/usr/bin/env python3
import os
import json
import datetime
from pathlib import Path

DATA_DIR = Path("data/records")
PREFIX = "NTR"
PAD = 4  # number of digits for sequence

DATA_DIR.mkdir(parents=True, exist_ok=True)

def next_code(year=None):
    if year is None:
        year = datetime.date.today().year
    prefix = f"{PREFIX}-{year}"
    max_seq = 0
    for p in DATA_DIR.glob(f"{prefix}-*.json"):
        name = p.stem  # filename without .json
        try:
            seq = int(name.split("-")[-1])
            if seq > max_seq:
                max_seq = seq
        except ValueError:
            continue
    return f"{prefix}-{str(max_seq + 1).zfill(PAD)}"

def create_record(title, artist, release_date=None, tier="subscription: standard", files=None, created_by="NetherXXVI"):
    code = next_code()
    obj = {
        "code": code,
        "title": title,
        "artist": artist,
        "release_date": release_date or str(datetime.date.today()),
        "format": "digital",
        "files": files or [],
        "tier": tier,
        "notes": "",
        "created_by": created_by,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    out_path = DATA_DIR / f"{code}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("Created", out_path)
    return out_path

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("title")
    p.add_argument("artist")
    p.add_argument("--release_date")
    p.add_argument("--tier", default="subscription: standard")
    args = p.parse_args()
    create_record(args.title, args.artist, args.release_date, args.tier)
