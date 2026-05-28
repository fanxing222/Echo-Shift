# core/recorder.py
# Records player positions every N frames for ghost replay.

from core.settings import RECORD_INTERVAL, MAX_RECORDING_FRAMES


class RunRecorder:
    def __init__(self):
        self.positions = []
        self.frame_counter = 0

    def record(self, x, y):
        """Record position if on the right frame interval."""
        self.frame_counter += 1
        if self.frame_counter % RECORD_INTERVAL == 0:
            if len(self.positions) < MAX_RECORDING_FRAMES:
                self.positions.append((x, y))

    def get_recording(self):
        """Return a copy of the recorded positions list."""
        return self.positions.copy()

    def reset(self):
        """Clear recording for a new run."""
        self.positions = []
        self.frame_counter = 0

    def is_full(self):
        """Check if recording has reached max length."""
        return len(self.positions) >= MAX_RECORDING_FRAMES

    @property
    def length(self):
        """Number of recorded positions."""
        return len(self.positions)
