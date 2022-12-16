import csv
import threading
from typing import Any, List, Optional, Union

from pydantic import BaseModel

from log_settings import logger
from utils import DRY_WEATHER, TOWN_DATA_FILENAME_CSV


class Town(BaseModel):
    city_name: str


class RespYesterdayModel(BaseModel):
    temp: int


class RespFactModel(BaseModel):
    temp: int
    obs_time: int
    uptime: int
    condition: str
    cloudness: float


class RespForecastHourModel(BaseModel):
    hour: int
    hour_ts: int
    temp: int
    condition: str


class RespForecastModel(BaseModel):
    date: str
    date_ts: int
    week: int
    hours: List[RespForecastHourModel]


class DayAverageTemp(BaseModel):
    date: str
    average_temp: float


class DayDryHours(BaseModel):
    date: str
    dry_hours: int


class TownAverageTemp(BaseModel):
    days: Union[list[DayAverageTemp], list]


class TownDryHours(BaseModel):
    days: Union[list[DayDryHours], list]


class TownTableData(Town):
    avarage_temp_in_period: list[TownAverageTemp]
    average_temp: float
    sum_dry_hours_in_period: list[TownDryHours]
    average_dry_hours: float
    rating: int


class RespModel(Town):
    now: int
    now_dt: str
    yesterday: RespYesterdayModel
    fact: RespFactModel
    forecasts: List[RespForecastModel]


class TownMathMethods:
    START_HOUR: int = 9
    END_HOUR: int = 19
    locker = threading.Lock()

    def __init__(self, town: RespModel):
        self.city_name = town.city_name
        self.now = town.now
        self.now_dt = town.now_dt
        self.yesterday = town.yesterday
        self.fact = town.fact
        self.forecasts = town.forecasts
        self.average_temp_in_period = self.calculation_average_temp_in_period()
        self.dry_hours_in_period = self.sum_dry_hours_in_period()
        self.total_average_temp = self._average_temp_in_request_days()
        self.total_dry_hours = self._average_dry_hours_in_request_days()
        self.rating: Optional[int] = None

    def calculation_average_temp_in_period(self,
                                           start_hour: int = START_HOUR,
                                           end_hour: int = END_HOUR) -> TownAverageTemp:
        town_average_temp = TownAverageTemp(days=[])
        difference = end_hour - start_hour
        for day in self.forecasts:
            total = 0
            if not day.hours:
                continue
            for hour in day.hours:
                if start_hour <= hour.hour < end_hour:
                    total += hour.temp
            average_temp = total / difference
            town_average_temp.days.append(DayAverageTemp(date=day.date, average_temp=average_temp))

        logger.info(f'average_temp_in_period was calculated for {self.city_name}')
        return town_average_temp

    def sum_dry_hours_in_period(self,
                                start_hour: int = START_HOUR,
                                end_hour: int = END_HOUR) -> TownDryHours:
        town_dry_hours = TownDryHours(days=[])
        for day in self.forecasts:
            hours_sum = 0
            if not day.hours:
                continue
            for hour in day.hours:
                if start_hour <= hour.hour < end_hour and hour.condition in DRY_WEATHER:
                    hours_sum += 1
            town_dry_hours.days.append(DayDryHours(date=day.date, dry_hours=hours_sum))

        logger.info(f'dry_hours_in_period was calculated for {self.city_name}')
        return town_dry_hours

    def _average_temp_in_request_days(self) -> float:
        sum_temp: float = sum(day.average_temp for day in self.average_temp_in_period.days)
        return round(sum_temp / len(self.average_temp_in_period.days), 1)

    def _average_dry_hours_in_request_days(self) -> float:
        dry_hours: float = sum(day.dry_hours for day in self.dry_hours_in_period.days)
        return round(dry_hours / len(self.dry_hours_in_period.days), 1)

    def get_day_headers(self) -> list[str]:
        days_date = []
        for day in self.average_temp_in_period.days:
            days_date.append(day.date)
        return days_date

    def get_first_row_town_data_for_csv(self):

        return [
            self.city_name,
            'Температура, среднее',
            *[day.average_temp for day in self.average_temp_in_period.days],
            self.total_average_temp,
            self.rating
        ]

    def get_second_row_town_data_for_csv(self):
        return [
            '',
            'Без осадков, часов',
            *[day.dry_hours for day in self.dry_hours_in_period.days],
            self.total_average_temp,
            ''
        ]

    def write_data_in_csv_file(self) -> None:
        """
        Cделал на всякий случай блокировку перед открытием файла, думаю можно блокировку поставить и после открытия.
        """
        self.locker.acquire()
        with open(TOWN_DATA_FILENAME_CSV, 'a', newline='') as f:
            writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(self.get_first_row_town_data_for_csv())
            writer.writerow(self.get_second_row_town_data_for_csv())
        self.locker.release()

    def to_dict(self) -> dict[str, Any]:
        return {
            'town': self.city_name,
            'total_average_temp': self.total_average_temp,
            'total_dry_hours': self.total_dry_hours,
            'average_temp_in_period': [day.dict() for day in self.average_temp_in_period.days],
            'dry_hours_in_period': [day.dict() for day in self.dry_hours_in_period.days],
        }
