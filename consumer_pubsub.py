import os
import json
from redis import Redis


REDIS_URL = os.getenv("REDIS_URL", "redis://default:PECFNp0jYt42UbXHjVTSbKH0uj6Te2UG@redis-17839.c56.east-us.azure.redns.redis-cloud.com:17839/0")
CHANNEL = os.getenv("POC_CHANNEL", "poc_channel")


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



