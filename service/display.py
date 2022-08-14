
class MakeTable:
    """
        Класс для графического представления списка информации по заданным цифровым кодам за заданную дату
    """
    def __init__(self, date, list_of_courses):
        """
        :param date: заданная дата
        :param list_of_courses: cписок с курсами, отобранными на предыдущих этапах
                                Пример: [(1, 'Фунт стерлингов Соединенного королевства', '826', 'GBP', 1, '73.1136'),
                                         (1, 'СДР (специальные права заимствования)', '960', 'XDR', 1, '79.7036'),
                                         (1, 'Доллар США', '840', 'USD', 1, '60.3696'),
                                         (1, 'Евро', '978', 'EUR', 1, '61.361')]
        """
        self.__date = date
        self.__list_of_courses = list_of_courses


    def table_width(self):
        """
            Определяем ширину таблицы по максимальной длине поля name
        """
            # self.__list_of_courses == False, если нет данных для отображения за выбранную дату
            # self.__list_of_courses == [(order_id_1, name_1, numeric_code_1,...),(...)], если есть данные для отображения
        if self.__list_of_courses:
            self.__max_len_name = max([len(r[1]) for r in self.__list_of_courses])+2
                # Если максимальная длина поля name меньше чем наименование столбца ("Название валюты"),
                # то задаем длину строки "Название валюты"
            if self.__max_len_name < 21:
                self.__max_len_name = 21
            table_width = self.__max_len_name + 59
        else:
            table_width = 78
            self.__max_len_name = 19
        return table_width


    def header(self):
        header = 'Перечень курсов валют, загруженных в БД, за {}'.format(self.__date)
        print('+', end='')
        print(header.center(self.table_width(),'-'),end='')
        print('+')
        print('|',end='')
        print(' Номер р-я ', end='')
        print('|', end='')
        print('Наименование валюты'.center(self.__max_len_name,' '),end='')
        print('|', end='')
        print(' Цифр. код ', end='')
        print('|', end='')
        print(' Букв. код ', end='')
        print('|', end='')
        print(' Номинал ', end='')
        print('|', end='')
        print(' Зн-е курса ', end='')
        print('|')
        print('+',end='')
        print('-'.center(self.table_width(), '-'),end='')
        print('+')


    def row(self,items=None):
            # аналогично предыдущей функции
        if self.__list_of_courses:
            for item in self.__list_of_courses:
                print('|', end='')
                print(str(item[0]).center(11), end='')
                print('|', end='')
                print(item[1].center(self.__max_len_name), end='')
                print('|', end='')
                print(item[2].center(11), end='')
                print('|', end='')
                print(item[3].center(11), end='')
                print('|', end='')
                print(str(item[4]).center(9), end='')
                print('|', end='')
                print(item[5].center(12), end='')
                print('|')
        else:
            print('|', end='')
            print('Нет данных для отображения за указанную дату'.center(78), end='')
            print('|', end='\n')


    def footer(self):
        print('+',end='')
        print('-'.center(self.table_width(), '-'),end='')
        print('+')


if __name__ == '__main__':
    list_of_courses = [
                       ('Фунт стерлингов Соединенного королевства', '826', 'GBP', 1, '73.1136'),
                       ('Доллар США', '840', 'USD', 1, '60.3696'),
                       ('Евро', '978', 'EUR', 1, '61.361'),
                       ('СДР (специальные права заимствования)', '960', 'XDR', 1, '79.7036')
    ]
    p = MakeTable('08.08.2022', list_of_courses)
    p.header()
    p.row(list_of_courses)
    p.footer()

