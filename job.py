from datetime import datetime
from typing import Callable, Optional


class Job:
    def __init__(self,
                 task: Callable,
                 task_str: str,
                 start_at: datetime,
                 tries: int = 0,
                 dependencies: Optional[list[str]] = None):

        self.start_at = start_at
        self.tries = tries
        self.dependencies = dependencies if dependencies else None
        self.task = task
        self.task_str = task_str
        self.actual_tries: int = 0

    def run(self):
        if self.check_run():
            self.task()
            _ = (yield)
            yield True

    def dict(self):
        return {
            'task_str': self.task_str,
            'start_at': self.start_at.timestamp(),
            'tries': self.tries,
            'dependencies': self.dependencies
        }

    def check_run(self):
        if datetime.now() < self.start_at:
            return False
        if self.dependencies:
            return False
        if self.actual_tries >= self.tries:
            return False
        return True
