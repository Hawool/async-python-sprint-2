from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass
from typing import Optional, Any

from pydantic import ValidationError

from log_settings import logger
from old_project.api_client import YandexWeatherAPI
from old_project.pydantic_dataclass import RespModel, TownMathMethods


@dataclass
class DataFetchingTask:
    """Class for getting weather data for cities"""
    yandex_api = YandexWeatherAPI()
    cities: dict[str, str]

    def get_town_weather_data(self) -> list[Optional[RespModel]]:
        logger.info('Launch of weather assembly in towns')
        with ThreadPoolExecutor() as pool:
            weather_data = pool.map(self.get_town_data, self.cities)
        logger.info('Towns weather was collected')
        return [town for town in weather_data]

    def get_town_data(self, town: str) -> Optional[RespModel]:
        resp = self.yandex_api.get_forecasting(town)
        logger.info(f'{town} weather was get received')
        return DataFetchingTask.validate_town_data(resp, town)

    @staticmethod
    def validate_town_data(resp: dict[str, Any], town: str) -> Optional[RespModel]:
        try:
            resp_model = RespModel(city_name=town, **resp)
            return resp_model
        except ValidationError as e:
            logger.error(f'Error: {e.json()}')
            return None


@dataclass
class DataCalculationTask:
    weather_data: list[RespModel]

    def calculated_weather_data(self) -> list[TownMathMethods]:
        with ProcessPoolExecutor() as pool:
            weather_data = pool.map(TownMathMethods, self.weather_data, chunksize=10)
        return [town for town in weather_data]

