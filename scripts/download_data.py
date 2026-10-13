"""Automated Data Ingestion Script for InsightLab.

Downloads the authentic Olist Relational E-Commerce dataset directly into
data/raw/ with progress logging and validation.
"""

import sys
from pathlib import Path
import urllib.request
import time

# Ensure project root is in sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import DATA_RAW_DIR, RAW_DOWNLOAD_URLS


def download_file(url: str, dest_path: Path) -> bool:
    """Download a file with progress reporting and error handling."""
    if dest_path.exists() and dest_path.stat().st_size > 0:
        print(f"  [SKIPPED] {dest_path.name} already exists ({dest_path.stat().st_size / (1024*1024):.2f} MB).")
        return True

    print(f"  [DOWNLOADING] {dest_path.name} from {url}...")
    start_time = time.time()
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) InsightLab/1.0"}
        )
        with urllib.request.urlopen(req, timeout=60) as response, open(dest_path, "wb") as out_file:
            chunk_size = 64 * 1024  # 64 KB
            bytes_downloaded = 0
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                out_file.write(chunk)
                bytes_downloaded += len(chunk)

        elapsed = time.time() - start_time
        mb = bytes_downloaded / (1024 * 1024)
        print(f"  [SUCCESS] {dest_path.name} ({mb:.2f} MB) in {elapsed:.1f}s.")
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to download {dest_path.name}: {e}")
        if dest_path.exists():
            dest_path.unlink()
        return False


def main():
    print("=" * 60)
    print("INSIGHTLAB: Raw Dataset Ingestion Pipeline")
    print(f"Target Directory: {DATA_RAW_DIR}")
    print("=" * 60)

    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    success_count = 0
    total = len(RAW_DOWNLOAD_URLS)

    for filename, url in RAW_DOWNLOAD_URLS.items():
        dest = DATA_RAW_DIR / filename
        if download_file(url, dest):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"Ingestion Finished: {success_count}/{total} files present in data/raw/.")
    print("=" * 60)


if __name__ == "__main__":
    main()
