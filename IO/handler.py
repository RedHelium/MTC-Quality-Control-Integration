import os

from MTC.handler import MTCQualityControlHandler


class QualityControlFileHandler:
    def __init__(self, directory_for_records, MTC: MTCQualityControlHandler) -> None:
        """
        Инициализация параметров для выгрузок тел. записей в файлы
        @directory_for_records: Путь до сохранения тел. записей
        @MTC: Модуль взаимодействия с "Контроль качества.API"
        """
        self.MTC = MTC
        self.directory_for_records = directory_for_records

    def write_record(self, phone, download_filename, filename, as_mp3=True):
        """
        Сохранить запись разговора в файле
        @phone: Номер телефона
        @download_filename: Имя файла для загрузки по API
        @filename: Имя файла, которое будет при сохранении без расширения
        """
        record = self.MTC.get_record(phone, download_filename, as_mp3)

        if record == 404:
            return

        if as_mp3:
            ext = ".mp3"
        else:
            ext = ".wav"

        path = "%s/%s/%s%s" % (self.directory_for_records, phone, filename, ext)

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "wb") as file:
            file.write(record)

    def download_records(self, phone, date_begin, date_end):
        """
        Загрузка всех записей по номеру телефона в периоде времени
        @phone: Номер телефона
        @date_begin: Начало звонка после даты
        @date_end: Начало звонка до даты
        """
        reports = self.MTC.get_number_report(phone, date_begin, date_end)

        for report in reports:
            self.write_record(
                phone,
                report["FileName"],
                "%s-%s" % (report["CallType"], report["DateTime"].replace(":", "-")),
            )

    def download_all_records(self, date_begin, date_end):
        """
        Загрузка всех записей разговоров по всем имеющимся номерам
        @date_begin: Начало звонка после даты
        @date_end: Начало звонка до даты
        """
        phones = [item["Phone"] for item in self.MTC.get_numbers()]

        for phone in phones:
            self.download_records(phone, date_begin, date_end)
