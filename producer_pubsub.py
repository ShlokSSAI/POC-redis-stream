import os
import sys
import json
import time
from datetime import datetime
from redis import Redis


REDIS_URL = os.getenv("REDIS_URL", "redis://default:PECFNp0jYt42UbXHjVTSbKH0uj6Te2UG@redis-17839.c56.east-us.azure.redns.redis-cloud.com:17839/0")
CHANNEL = os.getenv("POC_CHANNEL", "poc_channel")


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



