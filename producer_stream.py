import os
import sys
import json
import time
from datetime import datetime
from redis import Redis


REDIS_URL = os.getenv("REDIS_URL")
STREAM_KEY = os.getenv("POC_STREAM")

if not REDIS_URL:
    print("ERROR: REDIS_URL is not set. Please define it in your environment (e.g., via .env).", flush=True)
    sys.exit(1)
if not STREAM_KEY:
    print("ERROR: POC_STREAM is not set. Please define it in your environment (e.g., via .env).", flush=True)
    sys.exit(1)


def main(num: int) -> None:
    client = Redis.from_url(REDIS_URL, decode_responses=True)
    for i in range(num):
        event = {
            "type": "demo",
            "payload": json.dumps({"message": f"stream-event-{i}"}),
            "ts": datetime.now().isoformat(),
        }
        msg_id = client.xadd(STREAM_KEY, event, maxlen=10000, approximate=True)
        print(f"[STREAM] XADD id={msg_id}, fields={event}")
        time.sleep(0.2)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(n)



