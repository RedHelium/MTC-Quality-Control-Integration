import os
from dotenv import load_dotenv

from IO.handler import FileHandler
from MTC.handler import MTCQualityControlHandler


load_dotenv()

# Инициализируем модуль взаимодействия с Контроль качества.API
MTC = MTCQualityControlHandler(os.environ.get("USER_LOGIN"), os.environ.get("USER_PASSWORD"))

# Инициализируем модуль выгрузок записей звонков
fileHandler = FileHandler("records", MTC)

# Выгрузка всех тел. записей, сгруппированная по номерам телефонов за указанный период
fileHandler.download_all_records("2024-06-20T00:00:00", "2024-06-21T00:00:00")
