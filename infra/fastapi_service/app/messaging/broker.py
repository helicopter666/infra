from faststream.kafka import KafkaBroker

from app.core.config import settings

broker = KafkaBroker(
    settings.REDPANDA_BOOTSTRAP_SERVERS,
    # producer defaults
    request_timeout_ms=30_000,
    # consumer defaults переопределяются в @broker.subscriber
)
