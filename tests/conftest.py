import json
import os
from datetime import datetime
from pathlib import Path

import pytest

from job import Job
from scheduler import Scheduler
from tasks import TASKS


@pytest.fixture(scope='function')
def job_1():
    dt = datetime.fromtimestamp(123456789)
    return Job(TASKS.get('task_1'), 'task_1', dt, 1)


@pytest.fixture(scope='function')
def scheduler_1():
    s = Scheduler()
    s._file = Path(__file__).resolve().parent.joinpath('test_convert.json')
    return s
