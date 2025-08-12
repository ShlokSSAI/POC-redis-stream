import os
import sys
import json
import time
from datetime import datetime
from redis import Redis


REDIS_URL = os.getenv("REDIS_URL", "redis://default:PECFNp0jYt42UbXHjVTSbKH0uj6Te2UG@redis-17839.c56.east-us.azure.redns.redis-cloud.com:17839/0")
STREAM_KEY = os.getenv("POC_STREAM", "poc:events")


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



