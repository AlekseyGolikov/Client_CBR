import sqlite3
import logs


class DB_manager:
    def __init__(self,db_name='sqlite.db'):
        self.__inst_db = DB(db_name)

    def __enter__(self):
        return self.__inst_db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__inst_db.close()


class DB:

    def __init__(self,db_name='sqlite.db'):
        try:
            self.__con = sqlite3.connect(db_name)
            self.__cur = self.__con.cursor()

                # Проверка существуют ли таблицы в БД
                # Актуально при повторных записях в БД (влияет на запись логов)
            try:
                query = """
                    SELECT COUNT(*) FROM CURRENCY_ORDERS;
                """
                self.__cur.execute(query)
                c = self.__cur.fetchone()
            except sqlite3.OperationalError:
                db_not_created = True
            else:
                db_not_created = False

            if db_not_created is True:
                """
                    Таблица "Распоряжение о загрузке курсов"
                    .id     : int (первичный ключ, автоинкремент)       - номер распоряжения
                    .ondate : text (уникальное, обязательное значение)  - дата установки курсов ЦБ РФ
                """
                query = """
                            CREATE TABLE CURRENCY_ORDERS
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                ondate TEXT UNIQUE NOT NULL
                            );
                        """
                self.__cur.execute(query)
                self.__con.commit()
                logs.logger.info('Создана таблица CURRENCY_ORDERS')

                """
                    Таблица "Курсы валют"
                    .order_id        : int  - номер распоряжения (внешний ключ на CURRENCY_ORDER.id)
                    .name            : text - наименование валюты
                    .numeric_code    : text - цифровой код валюты (обязательное значение)
                    .alphabetic_code : text - буквенный код валюты (обязательное значение)
                    .scale           : int  - номинал курса (обязательное значение)
                    .rate            : text - значение курса (обязательное значение)
                """
                query = """
                            CREATE TABLE CURRENCY_RATES
                            (
                                order_id INTEGER,
                                name TEXT NOT NULL,
                                numeric_code TEXT NOT NULL,
                                alphabetic_code TEXT NOT NULL,
                                scale INTEGER NOT NULL,
                                rate TEXT NOT NULL,
                                FOREIGN KEY (order_id) REFERENCES CURRENCY_ORDER (id) ON DELETE CASCADE
                            );
                        """
                self.__cur.execute(query)
                self.__con.commit()
                logs.logger.info('Создана таблица CURRENCY_RATES')
        except sqlite3.OperationalError as ex:
            logs.logger.error('Ошибка БД [этап создания таблиц]: {}'.format(ex))


    def insert_date(self, date):
        """
            Проверяем существует ли в таблице CURRENCY_ORDER запись со значением date
            сли нет, то записываем новую дату
        :param date: Заданная дата
        :return lastrowid: индекс последней выполненной записи (используется для тестирования)
        """
        try:
            query = """
                        SELECT COUNT(*) FROM CURRENCY_ORDERS WHERE ondate=?
                    """
            self.__cur.execute(query, (date,))
            (res,) = self.__cur.fetchone()
            if res == 0:
                query = """
                            INSERT INTO CURRENCY_ORDERS (ondate) VALUES (?)
                        """
                self.__cur.execute(query, (date,))
                self.__con.commit()
                logs.logger.info('Запись даты {} выполнена'.format(date))
            else:
                logs.logger.warning('Запись даты {} отклонена'.format(date))
        except sqlite3.OperationalError as ex:
                logs.logger.error('Ошибка БД [этап записи даты]: {}'.format(ex))
        else:
            return self.__cur.lastrowid       # Получение ответа от БД о факте удачной записи в БД


    def insert_rates(self, date, items):
        """
            Запись данных в БД
        :param date:  заданная дата
        :param items: список со словарями курсов валют
        :return: None
        """

            # Проверка данных, переданных для записи,
            # и формирование списка курсов, отсутствующих в БД
        try:
            self.check_data(date, items)

            query = """
                        INSERT INTO CURRENCY_RATES 
                        (order_id, name, numeric_code, alphabetic_code, scale, rate)
                        VALUES ((SELECT id FROM CURRENCY_ORDERS WHERE ondate=?), ?, ?, ?, ?, ?);
                    """
            for item in self.__newest_rates_list:
                self.__cur.execute(query, ((date), item['Vname'], item['Vcode'], item['VchCode'], int(item['Vnom']), item['Vcurs']))
                self.__con.commit()
                logs.logger.info('Данные записаны в БД: {}'.format(item))
        except sqlite3.OperationalError as ex:
                logs.logger.error('Ошибка БД [этап записи курсов]: {}'.format(ex))
        else:
            return self.__cur.lastrowid       # Получение ответа от БД о факте удачной записи в БД

    def check_data(self, date, rates):
        """
            Проверка входных данных. Если в БД имеются записи по дате date и по списку rates,
            то функция формирует и возвращает список тех записей из исходного rates,
            которые отсутствуют в БД
            :param date: заданная дата; формат 'ДД.ММ.ГГГГ'
            :param rates: отобранный из ответа сервера список со словарями курсов валют
            :return: список курсов, отсутствующих в БД, которые необходимо дописать для текущей даты date
        """
        try:
            query = """
                        SELECT
                            CURRENCY_RATES.numeric_code
                        FROM CURRENCY_RATES
                            JOIN CURRENCY_ORDERS
                            WHERE CURRENCY_ORDERS.id=CURRENCY_RATES.order_id AND CURRENCY_ORDERS.ondate=?
                    """
            self.__cur.execute(query, (date,))

                # Формат written_rates_list: [(numeric_code_1,), (numeric_code_2,), ...]
            written_rates_list = self.__cur.fetchall()
            written_rates_list = [val for (val,) in written_rates_list]
            c=1
            self.__newest_rates_list = []

            for rate in rates:
                if not rate['Vcode'] in written_rates_list:
                    self.__newest_rates_list.append(rate)
                else:
                    logs.logger.warning('Запись отклонена: {}'.format(rate))
        except sqlite3.OperationalError as ex:
                logs.logger.error('Ошибка БД [этап проверки наличия ранее записанных курсов]: {}'.format(ex))
        else:
            return self.__newest_rates_list         # Получение списка кодов под запись в БД для тестовой функции

    def select(self, date):
        """
            Метод выводит на экран все курсы из БД за дату,
            указанную во входных аргументах скрипта
        :param date: заданная дата
        :return: Выборка курсов за заданную дату
        """
        try:
            query = """
                SELECT
                    CURRENCY_RATES.order_id,
                    CURRENCY_RATES.name,
                    CURRENCY_RATES.alphabetic_code,
                    CURRENCY_RATES.numeric_code,
                    CURRENCY_RATES.scale,
                    CURRENCY_RATES.rate
                FROM CURRENCY_RATES
                    JOIN CURRENCY_ORDERS
                    WHERE CURRENCY_ORDERS.id=CURRENCY_RATES.order_id AND CURRENCY_ORDERS.ondate=?
                    ORDER BY CURRENCY_RATES.alphabetic_code
            """
            res = self.__cur.execute(query, (date,))
            res = self.__cur.fetchall()
            if res == []:
                res = False
            return res
        except sqlite3.OperationalError as ex:
                logs.logger.error('Ошибка БД [этап чтения курсов за определённую дату]: {}'.format(ex))

    def close(self):
        self.__con.close()


if __name__=='__main__':
    date1 = '08.08.2022'
    test1 = [('test1', 'test1', 'test1', 111, '11111'),
             ('test2', 'test2', 'test2', 222, '22222'),
             ('test3', 'test3', 'test3', 333, '33333')]
    date2 = '09.08.2022'
    test2 = [('test4', 'test4', 'test4', 444, '44444')]
    date3 = '10.08.2022'
    test3 = [('test5', 'test5', 'test5', 555, '55555'),
             ('test6', 'test6', 'test6', 666, '66666')]
    date4 = '09.08.2022'
    test4 = [('test2', 'test2', 'test2', 222, '22222'),
             ('test3', 'test3', 'test3', 333, '33333'),
             ('test4', 'test4', 'test4', 444, '44444'),
             ('test7', 'test7', 'test7', 777, '77777')]


    with DB_manager() as d:
        d.insert_date(date1)
        d.insert_rates(date1, test1)
        d.insert_date(date2)
        d.insert_rates(date2, test2)
        d.insert_date(date3)
        d.insert_rates(date3, test3)
        d.insert_date(date4)
        d.insert_rates(date4, test4)

        print(d.select(date1))
        print(d.select(date2))
        print(d.select(date3))
        print(d.select(date4))
