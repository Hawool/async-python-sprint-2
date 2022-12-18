import pickle
from dataclasses import dataclass

from job import Job
from log_settings import logger


@dataclass
class SchedulerStatus:
    STATE_INIT = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2


class Scheduler:
    """
    Планировщик
    """
    _file = 'jobs.lock'
    _status = SchedulerStatus
    job_list: list[Job] = []

    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.status = self._status.STATE_INIT

    def schedule(self, job: Job) -> None:
        if not len(self.job_list) >= self.pool_size:
            self.job_list.append(job)
        else:
            logger.warning('Job was not added')

    def run(self) -> None:
        self.status = self._status.STATE_RUNNING
        self._main_loop()

    def restart(self) -> None:
        self.status = self._status.STATE_INIT
        self.restore_jobs()
        self.run()

    def stop(self) -> None:
        self.status = self._status.STATE_PAUSED
        self.save_jobs()

    def _main_loop(self) -> None:
        while self.status == self._status.STATE_RUNNING and self.job_list:
            try:
                for job in self.job_list:
                    job_con = job.run()
                    if job.check_run():
                        next(job_con)
                        if next(job_con):
                            self.job_list.remove(job)
            except StopIteration:
                self.status = self._status.STATE_PAUSED
                break

    def shutdown(self) -> None:
        self.status = self._status.STATE_PAUSED

    def save_jobs(self) -> None:
        with open(self._file, 'wb') as config_dictionary_file:
            pickle.dump(self.job_list, config_dictionary_file)

    def restore_jobs(self) -> None:
        try:
            with open(self._file, 'rb') as config_dictionary_file:
                self.job_list = pickle.load(config_dictionary_file)
        except FileNotFoundError as error:
            logger.error(f'File for restoring jobs was not found, {error=}')
