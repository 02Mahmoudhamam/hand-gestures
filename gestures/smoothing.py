from collections import deque, Counter

class DecisionSmoother:
    """Majority vote over a sliding window for stable labeling."""
    def __init__(self, window_size=7):
        self.window = deque(maxlen=max(3, window_size))
        self.conf_window = deque(maxlen=max(3, window_size))

    def update(self, label: str, confidence: float):
        self.window.append(label)
        self.conf_window.append(confidence)

        counts = Counter(self.window)
        winner, freq = counts.most_common(1)[0]
        win_ratio = freq / len(self.window)

        avg_conf = sum(self.conf_window) / len(self.conf_window) if self.conf_window else 0.0
        combined = 0.5 * win_ratio + 0.5 * avg_conf
        return winner, combined
