from datetime import datetime, timedelta

from job import Job
from scheduler import Scheduler
from tasks import task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8

now = datetime.now()
job_1 = Job(task_1, 'task_1', now + timedelta(seconds=5), 1)
job_2 = Job(task_2, 'task_2', now + timedelta(seconds=6), 2)
job_3 = Job(task_3, 'task_3', now + timedelta(seconds=7), 3)
job_4 = Job(task_4, 'task_4', now + timedelta(seconds=8), 1)
job_5 = Job(task_5, 'task_5', now + timedelta(seconds=9), 2)
job_6 = Job(task_6, 'task_6', now + timedelta(seconds=10), 3)
job_7 = Job(task_7, 'task_7', now + timedelta(seconds=11), 1)
job_8 = Job(task_8, 'task_8', now + timedelta(seconds=15), 2)


s = Scheduler()
s.schedule(job_1)
s.schedule(job_2)
s.schedule(job_3)
s.schedule(job_4)
s.schedule(job_5)
s.schedule(job_6)
s.schedule(job_7)
s.schedule(job_8)


if __name__ == '__main__':
    s.run()
