import time

class Timer:
    def __init__(self):
        self.api_calls = 0
        self.items_processed = 0
        self.start_time = time.time()

    def add_call(self, items_processed=1):
        self.api_calls += 1
        self.items_processed += items_processed

    def end(self):
        self.end_time = time.time()

    @property
    def duration(self):
        return self.end_time - self.start_time
