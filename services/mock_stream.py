"""
Mock IoT data stream: generates patient vitals in a background thread
and maintains a bounded buffer of recent readings for the dashboard.
"""
import time
import random
from collections import deque
from threading import Lock, Thread

# Default buffer size for vitals history (e.g. last 100 readings)
VITALS_BUFFER_SIZE = 100
# Interval between mock readings (seconds)
STREAM_INTERVAL = 2.0


def _random_in_range(min_val: float, max_val: float, decimals: int = 0) -> float:
    val = min_val + random.random() * (max_val - min_val)
    return round(val, decimals) if decimals else int(round(val))


def _generate_one_reading() -> dict:
    """Produce a single mock vital reading."""
    return {
        "timestamp": int(time.time() * 1000),
        "heartRate": _random_in_range(60, 100),
        "systolic": _random_in_range(110, 130),
        "diastolic": _random_in_range(70, 85),
        "bloodOxygen": _random_in_range(96, 100),
        "temperature": _random_in_range(362, 374, 1) / 10,  # 36.2–37.4 °C
        "respiratoryRate": _random_in_range(12, 20),
    }


class MockStreamService:
    def __init__(self, buffer_size: int = VITALS_BUFFER_SIZE, interval: float = STREAM_INTERVAL):
        self._buffer: deque = deque(maxlen=buffer_size)
        self._lock = Lock()
        self._interval = interval
        self._running = False
        self._thread: Thread | None = None
        self._on_reading = None  # optional callback(reading) for alert evaluation

    def start(self, on_reading=None):
        """Start background thread. on_reading(reading) is called for each new reading."""
        if self._running:
            return
        self._on_reading = on_reading
        # Seed one reading so /api/vitals/latest is valid immediately
        with self._lock:
            self._buffer.append(_generate_one_reading())
        self._running = True
        self._thread = Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=self._interval * 2)
            self._thread = None

    def _run_loop(self):
        while self._running:
            reading = _generate_one_reading()
            with self._lock:
                self._buffer.append(reading)
            if self._on_reading:
                try:
                    self._on_reading(reading)
                except Exception:
                    pass
            time.sleep(self._interval)

    def get_latest(self) -> dict | None:
        with self._lock:
            return self._buffer[-1] if self._buffer else None

    def get_history(self, limit: int = 50) -> list:
        with self._lock:
            return list(self._buffer)[-limit:]


# Singleton used by the app
mock_stream_service = MockStreamService()
