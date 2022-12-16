from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Job:
    _task = None
    def __init__(self, start_at: datetime, max_working_time=-1, tries=0, dependencies=[]):
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies

    def run(self):
        print(f'Job {id(self)}')

    def pause(self):
        pass

    def stop(self):
        pass

    def dict(self):
        return {
            'task': self._task,
            'start_at': self.start_at,
            'max_working_time': self.max_working_time,
            'tries': self.tries,
            'dependencies': self.dependencies
        }
