import prettytable
from prettytable import PrettyTable
from . import db

class MakeTable:
    """
        Класс для графического представления списка информации по заданным цифровым кодам за заданную дату
    """
    def __init__(self, date):
        """
        :param date: заданная дата
        :param list_of_courses: cписок с курсами, отобранными на предыдущих этапах
                                Пример: [(1, 'Фунт стерлингов Соединенного королевства', '826', 'GBP', 1, '73.1136'),
                                         (1, 'СДР (специальные права заимствования)', '960', 'XDR', 1, '79.7036'),
                                         (1, 'Доллар США', '840', 'USD', 1, '60.3696'),
                                         (1, 'Евро', '978', 'EUR', 1, '61.361')]
        """
        self.__date = date
        self.__mytable = PrettyTable()
        self.__mytable.field_names = ['Номер р-я','Наименование валюты','Цифр. код', 'Букв. код', 'Номинал', 'Зн-е курса']

    def show_table(self):
        with db.DB_manager() as d:
            self.__mytable = prettytable.from_db_cursor(d.select(self.__date))
            print(self.__mytable)


if __name__ == '__main__':
    pass