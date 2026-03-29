# Filesystem Bridge

## Why

Agents running in sandboxed environments (like Claude Desktop's Cowork mode) cannot make outbound HTTP requests. MCP tool calls work (the MCP client bridges the connection), but raw HTTP does not. The bridge works around this by turning a shared filesystem folder into a message bus for HTTP requests.

## How It Works

A lightweight Python script runs on the host machine and watches a shared folder. The agent writes a JSON request file, the script executes the HTTP call on the host side, and writes the response back to the same folder.

## Setup

The bridge script lives in `/scripts/fs_bridge.py` and watches the `/bridge` folder.

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (the script handles its own dependencies via inline metadata)

### Running

```bash
cd scripts
chmod +x fs_bridge.py
./fs_bridge.py
```

By default it watches `../bridge/` and sends HTTP calls to `http://localhost:8000`. Override with flags:

```bash
./fs_bridge.py --watch-dir /path/to/bridge --base-url http://plotter-pi.local:8000
```

## Protocol

The agent places files and requests in the watch directory. Request files are named `{id}.request.json`. The watchdog processes them and writes `{id}.response.json`.

### POST (file upload)

```json
{"id": "my-upload", "method": "POST", "url": "/files", "file": "my-drawing.svg"}
```

The `file` field is relative to the watch directory. The file must be placed there before the request is written. The response body contains whatever the server returns.

### GET (file download)

```json
{"id": "my-download", "method": "GET", "url": "/files/abc123", "save_as": "capture.jpg"}
```

When `save_as` is present, the response body is saved as a file in the watch directory instead of being returned as JSON.

## Limitations

- This is a workaround for sandboxed environments. Agents with direct HTTP access should skip the bridge entirely.
- The watchdog polls every 0.5 seconds so there is a small delay between writing a request and getting a response.
- Request files are deleted after processing. Response files accumulate and should be cleaned up periodically.
