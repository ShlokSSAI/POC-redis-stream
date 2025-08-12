import os
import json
import time
from redis import Redis


REDIS_URL = os.getenv("REDIS_URL", "redis://default:PECFNp0jYt42UbXHjVTSbKH0uj6Te2UG@redis-17839.c56.east-us.azure.redns.redis-cloud.com:17839/0")
STREAM_KEY = os.getenv("POC_STREAM", "poc:events")
GROUP = os.getenv("POC_GROUP", "poc-group")
CONSUMER = os.getenv("POC_CONSUMER", os.getenv("HOSTNAME", "consumer-1"))


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



