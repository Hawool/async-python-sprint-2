import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from threading import Thread, Event

from job import Job
from log_settings import logger


class StopScheduler(Exception):
    pass


@dataclass
class SchedulerStatus:
    STATE_INIT = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2


class Scheduler:
    _thread = None
    _event = Event()
    _status = SchedulerStatus
    main_loop = None

    def __init__(self, pool_size=10):
        self.pool_size = pool_size
        self.job_list: list[Job] = []
        self.status = self._status.STATE_INIT

    def schedule(self, job):
        print('schedule')
        if not len(self.job_list) >= self.pool_size:
            # self.run()
            # self._event.wait()
            self.job_list.append(job)
        else:
            logger.warning('Job was not added')

    def run(self):
        print('run')
        if self.status == self._status.STATE_RUNNING:
            print(self.status)
            return
        #
        # self.status = self._status.STATE_RUNNING
        # # if self._event is None or self._event.is_set():
        # #     self._event = Event()
        #
        # self._thread = Thread(target=self._main_loop, name='MyScheduler')
        # self._thread.start()
        #
        # # if self.job_list:
        # #     with ThreadPoolExecutor(max_workers=self.pool_size) as pool:
        # #         pool.map(Job.run, self.job_list)

        self.main_loop = self._main_loop()
        self.main_loop.send(None)
        # for job in self.job_list:
        self.main_loop.send(self.job_list)

    def restart(self):
        print('restart')
        self.status = self._status.STATE_INIT
        self.run()

    def stop(self):
        print('stop')
        self.status = self._status.STATE_PAUSED
        self.main_loop.throw(StopScheduler)

    def _main_loop(self):
        print('loop')

        # wait_seconds = 6000
        # while self.status == STATE_RUNNING:
        # while self.status == self._status.STATE_RUNNING:
        try:
            while tasks := (yield):
                for task in tasks:
                    time.sleep(0.5)
                    print('while')
                    # self._event.wait(wait_seconds)
                    # self._event.clear()
                    self._process_jobs()
        except StopScheduler:
            print('stop')

    def _process_jobs(self):

        now = int(datetime.now().timestamp())
        for job in self.job_list:
            if int(job.start_at.timestamp()) - now < 0:
                job.run()
                self.job_list.remove(job)
                self._event.set()

    def shutdown(self, *args, **kwargs):
        print('shotdown')
        self.status = self._status.STATE_PAUSED
        self._event.clear()



s = Scheduler()
now = datetime.now()
for i in range(15):
    s.schedule(job=Job(now+timedelta(seconds=i), 2, 3, 4))

s.run()


############### BLOK STOP and RESTART ####################
# now = datetime.now().timestamp()
#
# while int(datetime.now().timestamp()) < now + 5:
#     time.sleep(1)


s.stop()
print('sleep 3 sec')
time.sleep(3)
s.restart()
##########################################################


time.sleep(3)
s.shutdown()




