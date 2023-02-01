from datetime import datetime
from pathlib import Path
from typing import TypedDict
import json

from weather_api_service import Weather
from base import format_weather

# Условия для типа различных "хранилищ"
class WeatherStorage:
	def save(self, weather: Weather) -> None:
		raise NotImplementedError


class HistoryRecord(TypedDict):
	date: str
	weather: str


# Запись в открытый файл
class PlainFileWeatherStorage(WeatherStorage):
	def __init__(self, file: Path):
		self._file = file

	def save(self, weather: Weather) -> None:
		now = datetime.now()
		formatted_weather = format_weather(weather)
		with open(self._file, "a") as file:
			file.write(f"{now}\n {formatted_weather}\n")


# Хранилище в JSON файле
class JSONFileWeatherStorage(WeatherStorage):
	def __init__(self, jsonfile: Path):
		self._jsonfile = jsonfile
		self._init_storage()

	def save(self, weather: Weather) -> None:
		history = self._read_history()
		history.append({
			"date": str(datetime.now()),
			"weather": format_weather(weather)
		})
		self._write(history)

	# Если создался новый файл, то его инициализирую и добавляют [].
	def _init_storage(self) -> None:
		if not self._jsonfile.exists():
			self._jsonfile.write_text("[]")

	def _read_history(self) -> list[HistoryRecord]:
		with open(self._jsonfile, "r", encoding='utf-8') as file:
			return json.load(file)

	def _write(self, history: list[HistoryRecord]) -> None:
		with open(self._jsonfile, "w", encoding='utf-8') as file:
			json.dump(history, file, ensure_ascii=False, indent=4)


def save_weather(weather: Weather, storage: WeatherStorage) -> None:
	storage.save(weather)

