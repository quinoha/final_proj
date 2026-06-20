import json
import time

class PerfettoProfiler:
    def __init__(self, filename="baseline_trace.json"):
        self.filename = filename
        self.events = []
        self.start_time = time.time()

    def add_event(self, name, category, start_us, duration_us):
        """Make events that we can view on Perfetto"""
        event = {
            "name" : name,
            "cat": category,
            "ph": "X",
            "ts": start_us,
            "dur": duration_us,
            "pid": 1,
            "tid": 1
        }
        self.events.append(event)

    def save(self):
        """Save the collected data into a JSON file"""
        with open(self.filename, 'w') as f:
            json.dump({"traceEvents": self.events}, f)
        print(f"Perfetto trace saved: {self.filename}")