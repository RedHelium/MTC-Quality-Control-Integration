from xmlrpc.client import ResponseError
import requests


class MTCQualityControlHandler:
    def __init__(self, login, password) -> None:
        """
        Создание сессии по логину и паролю от услуги "Контроль качества"
        @login: Логин
        @password: Пароль
        """
        self.url = "https://mrecord.mts.ru/api/v3"
        self.login = login
        self.password = password
        self.session = requests.Session()
        self.session.auth = (self.login, self.password)

    def __get(self, url, as_json=True):
        """
        Общий GET запрос
        @url: Адрес
        @as_json: Вернуть ответ в формате JSON, иначе в байтовом представлении
        """
        response = self.session.get(url)

        try:
            if response.status_code == 200:
                if as_json:
                    return response.json()
                else:
                    return response.content
            elif response.status_code == 404:
                return 404
            else:
                raise ResponseError(
                    "Ошибка выполнения запроса! Код: %s,\n ответ: %s"
                    % (response.status_code, response.json())
                )
        except Exception as ex:
            raise ResponseError("Ошибка отправки запроса!\n %s" % (ex))

    def __put(self, url, body):
        """
        Общий PUT запрос
        @url: Адрес
        @body: Тело запроса
        """

        response = self.session.put(url, data=body)

        try:
            if response.status_code == 200:
                return response.json()
            else:
                raise ResponseError(
                    "Ошибка выполнения запроса! Код: %s,\n ответ: %s"
                    % (response.status_code, response.json())
                )
        except Exception as ex:
            raise ResponseError("Ошибка отправки запроса!\n %s" % (ex))

    def __delete(self, url):
        """
        Общий DELETE запрос
        @url: Адрес
        """
        response = self.session.delete(url)

        try:
            if response.status_code == 200:
                return {
                    "status": response.status_code,
                    "message": "Удаление прошло успешно.",
                }
            else:
                raise ResponseError(
                    "Ошибка выполнения запроса! Код: %s,\n ответ: %s"
                    % (response.status_code, response.json())
                )
        except Exception as ex:
            raise ResponseError("Ошибка отправки запроса!\n %s" % (ex))

    def get_numbers(self) -> dict:
        """
        Получить список тел.номеров, которые настроены в ЛК
        """
        return self.__get("%s/numbers" % (self.url))

    def update_numbers(self, number, body):
        """
        Обновить параметры номера
        @number: Номер, параметры которого необходимо обновить
        @body: Набор обновленных параметров в формате словаря
        """
        return self.__put(url="%s/numbers/%s" % (self.url, number), body=body)

    def get_number_report(self, number, begin_date, end_date):
        """
        Получить отчёт по записям разговоров
        @number: Номер телефона
        @begin_date: Начало звонка после даты
        @end_date: Начало звонка до даты
        """
        return self.__get(
            url="%s/recs/%s/%s/%s" % (self.url, number, begin_date, end_date)
        )

    def get_record(self, number, filename, as_mp3=True):
        """
        Получить запись разговора в формате MP3
        @number: Номер телефона
        @filename: Имя файла
        @as_mp3: Получить файл разговора в формате MP3, либо в формате WAV
        """
        if as_mp3:
            url = "%s/file/%s/%s" % (self.url, number, filename)
        else:
            url = "%s/file/wav/%s/%s" % (self.url, number, filename)

        return self.__get(url=url, as_json=False)

    def delete_record(self, number, filename):
        """
        Удалить файл записи разговора
        @number: Номер телефона
        @filename: Имя файла
        """
        return self.__delete(url="%s/file/%s/%s" % (self.url, number, filename))

    def get_stereo(self):
        """
        Получить параметры стерео главного ТПО
        """
        return self.__get(url="%s/stereo" % (self.url))

    def update_stereo(self, data):
        """
        Обновить параметры стерео
        @data: Обновленные параметры стерео
        """
        return self.__put(url="%s/stereo" % (self.url), body=data)
