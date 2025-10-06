from collections import defaultdict

class SessionStats:
    """
    In-memory counters + session duration holder.
    Only bump() after the gesture passes stability + confidence threshold.
    """
    def __init__(self):
        self.counts = defaultdict(int)
        self.duration_sec = 0

    def bump(self, label: str):
        self.counts[label] += 1

    def set_duration(self, seconds: int):
        self.duration_sec = int(seconds)

    def as_dict(self):
        d = dict(self.counts)
        d["duration_sec"] = self.duration_sec
        return d
