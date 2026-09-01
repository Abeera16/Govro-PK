#!/usr/bin/env python3

import os
import sys
from datetime import datetime, timezone

from qdrant_client import QdrantClient


def main() -> int:
    qdrant_url = os.getenv("QDRANT_URL", "").strip()
    qdrant_api_key = os.getenv("QDRANT_API_KEY", "").strip()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    if not qdrant_url or not qdrant_api_key:
        print(f"[{timestamp}] ERROR: QDRANT_URL and QDRANT_API_KEY must be set.")
        return 1

    try:
        client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key, timeout=30)
        client.get_collections()
        print(f"[{timestamp}] SUCCESS: Qdrant keepalive heartbeat sent to {qdrant_url}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[{timestamp}] ERROR: Qdrant keepalive failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
