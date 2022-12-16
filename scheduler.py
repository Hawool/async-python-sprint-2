import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from job import Job
from log_settings import logger
from tasks import TASKS


@dataclass
class SchedulerStatus:
    STATE_INIT = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2


class Scheduler:
    """
    Задание выдалось крайне тяжелым и неприятным для такого короткого срока, поставлено не очень понятно, много времени
    ушло на понимание требований.
    Поэтому сейчас не реализованно:
    - ретраи и зависимости у задач (плохо выстроена логика, лучше идей сейчас не вижу)
    - длительность выполнения задачи (аналогичная ситуация, т.к логика работы на корутинах мне плохо понятна, то и время
      не совсем ясно как засекать)
    - сохранение джобов в файл реализовано, но оно ужасно (как можно это сделать с объектами функций?)

    Изначально хотел сделать выполнение планировщика в отдельном потоке на фоне, но судя по отзывам
    это не подходит под условия про корутины.
    """
    _file = 'convert.json'
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
                    next(job_con)
                    if next(job_con):
                        self.job_list.remove(job)
            except StopIteration:
                self.status = self._status.STATE_PAUSED
                break

    def shutdown(self) -> None:
        self.status = self._status.STATE_PAUSED

    def save_jobs(self) -> None:
        with open(self._file, 'w') as convert_file:
            convert_file.write(json.dumps([job.dict() for job in self.job_list]))

    def restore_jobs(self) -> None:
        with open(self._file, 'r') as convert_file:
            file = convert_file.read()
        json_file = json.loads(file)
        self.job_list = Scheduler.json_to_job(json_file)

    @staticmethod
    def json_to_job(json_file: list[dict[str, Any]]) -> list[Job]:
        job_list = []
        for dict_job in json_file:
            job = Job(
                TASKS.get(dict_job.get('task_str')),  # type: ignore
                dict_job.get('task_str'),  # type: ignore
                datetime.fromtimestamp(dict_job.get('start_at')),  # type: ignore
                dict_job.get('tries')  # type: ignore
            )
            job_list.append(job)
        return job_list
