#!/usr/bin/env -S uv run --with requests
"""
Plotter Studio Filesystem Bridge
=================================
A watchdog that monitors a folder for HTTP request files from a sandboxed
agent, executes them on the host, and writes responses back.

Usage:
    python fs_bridge.py [--watch-dir ../bridge] [--base-url http://localhost:8888]

The agent writes request files like `abc123.request.json`:
    {"id": "abc123", "method": "POST", "url": "/files", "file": "drawing.svg"}

The watchdog executes the request, then writes `abc123.response.json`:
    {"id": "abc123", "status": 200, "body": {"id": "xyz", "url": "/files/xyz"}}

Supported request types:
    - File upload:  {"method": "POST", "url": "/files", "file": "name.svg"}
                    The "file" field is relative to the watch directory.
    - Download:     {"method": "GET", "url": "/files/{id}", "save_as": "capture.jpg"}
                    Downloads the file and saves it in the watch directory.
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="[bridge] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
log = logging.getLogger("bridge")

DEFAULT_WATCH_DIR = Path(__file__).resolve().parent.parent / "bridge"
DEFAULT_BASE_URL = "http://localhost:8888"
POLL_INTERVAL = 0.5


def handle_request(req_path: Path, base_url: str, watch_dir: Path):
    req_id = req_path.stem.replace(".request", "")
    resp_path = req_path.parent / f"{req_id}.response.json"

    try:
        req = json.loads(req_path.read_text())
    except Exception as e:
        log.error(f"Failed to parse {req_path.name}: {e}")
        resp_path.write_text(json.dumps({"id": req_id, "status": 400, "error": str(e)}))
        req_path.unlink(missing_ok=True)
        return

    method = req.get("method", "GET").upper()
    url = base_url.rstrip("/") + "/" + req.get("url", "").lstrip("/")
    log.info(f"{method} {url}")

    try:
        if method == "POST" and "file" in req:
            file_path = watch_dir / req["file"]
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            with open(file_path, "rb") as f:
                r = requests.post(url, files={"file": (file_path.name, f)})
            body = r.json()
            resp_path.write_text(json.dumps({"id": req_id, "status": r.status_code, "body": body}))

        elif method == "GET":
            r = requests.get(url)
            save_as = req.get("save_as")
            if save_as and r.ok:
                out = watch_dir / save_as
                out.write_bytes(r.content)
                resp_path.write_text(json.dumps({
                    "id": req_id,
                    "status": r.status_code,
                    "saved": save_as,
                    "size": len(r.content),
                }))
            else:
                try:
                    body = r.json()
                except Exception:
                    body = r.text[:500]
                resp_path.write_text(json.dumps({"id": req_id, "status": r.status_code, "body": body}))

        else:
            resp_path.write_text(json.dumps({"id": req_id, "status": 400, "error": f"Unsupported method: {method}"}))

    except Exception as e:
        log.error(f"Request failed: {e}")
        resp_path.write_text(json.dumps({"id": req_id, "status": 500, "error": str(e)}))

    req_path.unlink(missing_ok=True)
    log.info(f"Done: {resp_path.name}")


def watch(watch_dir: Path, base_url: str):
    watch_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Watching {watch_dir}")
    log.info(f"Base URL: {base_url}")

    while True:
        for req_file in sorted(watch_dir.glob("*.request.json")):
            handle_request(req_file, base_url, watch_dir)
        time.sleep(POLL_INTERVAL)


def main():
    parser = argparse.ArgumentParser(description="Plotter Studio Filesystem Bridge")
    parser.add_argument("--watch-dir", type=Path, default=DEFAULT_WATCH_DIR)
    parser.add_argument("--base-url", type=str, default=DEFAULT_BASE_URL)
    args = parser.parse_args()
    watch(args.watch_dir, args.base_url)


if __name__ == "__main__":
    main()
