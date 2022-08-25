class TaskRecord:
    start: int
    finished: int

    def __init__(self, start: int, finished: int = None):
        self.start = start
        self.finished = finished

    def get_duration(self) -> int:
        if self.finished is None:
            return 0
        return self.finished - self.start

    def is_timestamp_in_range(self, from_ts: int, to_ts: int) -> bool:
        if self.finished is None:
            return False
        return self.start >= from_ts and self.finished <= to_ts
