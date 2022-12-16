import os
from typing import Optional

from old_project.pydantic_dataclass import RespModel, TownMathMethods
from old_project.utils import CITIES
from old_project.weather_tasks import DataFetchingTask, DataCalculationTask

FILE = 'mydocument.txt'
RENAMED_FILE = 'mysuperdocument.txt'
NEW_DIR = 'new_dir'


def task_1():
    with open(FILE, mode='w') as f:
        f.write('This text is written with Python')


def task_2():
    os.rename(FILE, RENAMED_FILE)


def task_3():
    os.mkdir(NEW_DIR)


def task_4():
    os.rmdir(NEW_DIR)


def task_5():
    with open(RENAMED_FILE, mode='a') as f:
        f.write('This text is written with Python. CHAPTER 2!')


def task_6():
    os.remove(RENAMED_FILE)


def task_7() -> list[Optional[RespModel]]:
    return DataFetchingTask(CITIES).get_town_weather_data()


def task_8(weather_data: list[RespModel]) -> list[TownMathMethods]:
    return DataCalculationTask(weather_data).calculated_weather_data()


TASKS = {
    'task_1': task_1,
    'task_2': task_2,
    'task_3': task_3,
    'task_4': task_4,
    'task_5': task_5,
    'task_6': task_6,
    'task_7': task_7,
    'task_8': task_8,
}
