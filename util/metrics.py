"""Prometheus metrics for kp-msx.

Scraped by the homelab Prometheus over Fly's public, token-guarded /metrics
endpoint (see api.py). Single uvicorn worker (Dockerfile) -> the default
process-global registry is correct; no multiprocess mode needed.
"""
from prometheus_client import Counter
from prometheus_client.core import GaugeMetricFamily
from prometheus_client.registry import REGISTRY

from util import db

# Custom application counters.
PLAY = Counter('kpmsx_play_total', 'Number of /msx/play requests served')
PROXY = Counter('kpmsx_proxy_total', 'Number of /msx/proxy playlist-launder requests served')
REGISTRATIONS = Counter('kpmsx_registrations_total', 'Number of successful new device pairings')


class _DeviceCollector:
    """Query-on-scrape gauge for the registered-device count.

    Implemented as a custom collector (collect() runs on every scrape) rather
    than a Gauge mutated on register/delete, so the value can never go stale.
    """

    def collect(self):
        g = GaugeMetricFamily('kpmsx_devices', 'Registered devices (rows with a non-null token)')
        try:
            g.add_metric([], float(db.count_registered_devices()))
        except Exception:
            # Never let a transient DB error break a metrics scrape.
            return
        yield g


_initialised = False


def init():
    """Register the custom collector once (idempotent)."""
    global _initialised
    if _initialised:
        return
    REGISTRY.register(_DeviceCollector())
    _initialised = True
