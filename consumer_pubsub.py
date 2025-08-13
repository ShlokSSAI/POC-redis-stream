import os
import sys
import json
from redis import Redis


REDIS_URL = os.getenv("REDIS_URL")
CHANNEL = os.getenv("POC_CHANNEL")

if not REDIS_URL:
    print("ERROR: REDIS_URL is not set. Please define it in your environment (e.g., via .env).", flush=True)
    sys.exit(1)
if not CHANNEL:
    print("ERROR: POC_CHANNEL is not set. Please define it in your environment (e.g., via .env).", flush=True)
    sys.exit(1)


def main() -> None:
    client = Redis.from_url(REDIS_URL, decode_responses=True)
    pubsub = client.pubsub()
    pubsub.subscribe(CHANNEL)
    print(f"[PUBSUB] Subscribed to {CHANNEL}")
    for message in pubsub.listen():
        if message["type"] != "message":
            continue
        event = json.loads(message["data"])  # ephemeral; only receives messages while running
        print(f"[PUBSUB] Received: {event}")


if __name__ == "__main__":
    main()



