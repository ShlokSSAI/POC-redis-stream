import os
import sys
import json
import time
from redis import Redis


REDIS_URL = os.getenv("REDIS_URL")
STREAM_KEY = os.getenv("POC_STREAM")
GROUP = os.getenv("POC_GROUP")
CONSUMER = os.getenv("POC_CONSUMER", os.getenv("HOSTNAME"))

missing = []
if not REDIS_URL: missing.append("REDIS_URL")
if not STREAM_KEY: missing.append("POC_STREAM")
if not GROUP: missing.append("POC_GROUP")
if not CONSUMER: missing.append("POC_CONSUMER")
if missing:
    print(f"ERROR: Missing required env vars: {', '.join(missing)}. Define them in your environment (e.g., via .env).", flush=True)
    sys.exit(1)


def ensure_group(client: Redis) -> None:
    try:
        client.xgroup_create(STREAM_KEY, GROUP, id="$", mkstream=True)
        print(f"[STREAM] Created group {GROUP} on {STREAM_KEY}")
    except Exception as e:
        # Group exists
        pass


def main() -> None:
    client = Redis.from_url(REDIS_URL, decode_responses=True)
    ensure_group(client)
    print(f"[STREAM] Starting consumer {CONSUMER} in group {GROUP}")
    while True:
        resp = client.xreadgroup(GROUP, CONSUMER, {STREAM_KEY: ">"}, count=10, block=5000)
        if not resp:
            continue
        for _, entries in resp:
            for message_id, fields in entries:
                try:
                    payload = json.loads(fields.get("payload", "{}"))
                    print(f"[STREAM] Got id={message_id} type={fields.get('type')} payload={payload}")
                    # Simulate processing
                    time.sleep(0.1)
                    client.xack(STREAM_KEY, GROUP, message_id)
                    print(f"[STREAM] XACK id={message_id}")
                except Exception as e:
                    print(f"[STREAM] Error on id={message_id}: {e}")
                    # no ACK: will remain pending for retry


if __name__ == "__main__":
    main()



