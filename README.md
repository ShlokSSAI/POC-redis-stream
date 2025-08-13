# POC-redis-stream
Comparison between redis stream and pub/sub
POC: Redis Streams vs Pub/Sub

Goal: Show why Redis Streams are more reliable than Pub/Sub for your producer→consumer pipeline.

Structure
- producer_pubsub.py / consumer_pubsub.py: classic Pub/Sub (ephemeral)
- producer_stream.py / consumer_stream.py: Redis Streams with consumer groups (durable + ack)

Prereqs
- Python 3.9+
- `pip install redis`
- REDIS_URL set (or it will default to your cloud Redis)

Environment
```bash
.env

Run: Pub/Sub (shows message loss if consumer starts late)
```bash
# 1) Publish 3 messages BEFORE starting consumer
python producer_pubsub.py 3

# 2) Now start consumer; it will not receive the 3 old messages
python consumer_pubsub.py
# In a new shell, publish more and see they arrive only if consumer is running
python producer_pubsub.py 2
```

Run: Streams (reliable, with replay + ack)
```bash
# 1) Produce 3 messages to the stream first
python producer_stream.py 3

# 2) Start consumer; it will read the 3 past messages (replay) and ACK them
python consumer_stream.py

# 3) Produce more; consumer will continue from last ID
python producer_stream.py 2
```

Notes
- Streams consumer uses a group (poc-group) and acknowledges processed entries.
- If consumer crashes mid-way, unacked entries remain PENDING and can be claimed/retried.
- This is the key advantage over Pub/Sub in your pipeline.



