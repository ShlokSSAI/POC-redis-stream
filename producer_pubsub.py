import os
import sys
import json
import time
from datetime import datetime
from redis import Redis


REDIS_URL = os.getenv("REDIS_URL")
CHANNEL = os.getenv("POC_CHANNEL")

if not REDIS_URL:
    print("ERROR: REDIS_URL is not set. Please define it in your environment (e.g., via .env).", flush=True)
    sys.exit(1)
if not CHANNEL:
    print("ERROR: POC_CHANNEL is not set. Please define it in your environment (e.g., via .env).", flush=True)
    sys.exit(1)


def main(num: int) -> None:
    client = Redis.from_url(REDIS_URL, decode_responses=True)
    for i in range(num):
        event = {
            "id": i,
            "ts": datetime.now().isoformat(),
            "type": "demo",
            "payload": {"message": f"pubsub-event-{i}"},
        }
        client.publish(CHANNEL, json.dumps(event))
        print(f"[PUBSUB] Published: {event}")
        time.sleep(0.2)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(n)



