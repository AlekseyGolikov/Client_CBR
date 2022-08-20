import sqlite3
import datetime


class ValidateInputError(Exception):
    def __str__(self):
        s = '\n\r\tДата и/или список кодов не введены!'
        s += '\n\r\tПожалуйста, повторите ввод.'
        s += '\n\r\tФормат ввода даты: ДД.ММ.ГГГГ'
        s += '\n\r\tФормат ввода кодов: ХХ,ХХХ,...; кол-во цифр в коде: 2 или 3;'
        return s


class ValidateDateError(Exception):
    def __str__(self):
        s = '\n\r\tДата введена не корректно!'
        s += '\n\r\tПожалуйста, повторите ввод.'
        s += '\n\r\tФормат ввода: ДД.ММ.ГГГГ'
        return s


class DateOutOfRangeError(Exception):
    def __init__(self,date):
        self.__date = date
    def __str__(self):
        s = '\n\r\tВведенная дата {} больше текущей!'.format(self.__date)
        s += '\n\r\tПожалуйста, повторите ввод.'
        s += '\n\r\tФормат ввода: ДД.ММ.ГГГГ'
        return s


class ValidateCodeError(Exception):
    def __str__(self):
        s = '\n\r\tСписок кодов введён не корректно!'
        s += '\n\r\tПожалуйста, повторите ввод.'
        s += '\n\r\tФормат ввода: ХХ,ХХХ,...; кол-во цифр в коде: 2 или 3;'
        return s


class DB_Error_CreateTables(sqlite3.OperationalError):
    def __str__(self):
        s = '\n\r\tОшибка БД [этап создания таблиц]'
        return s


class DB_Error_InsertDate(sqlite3.OperationalError):
    def __str__(self):
        s = '\n\r\tОшибка БД [этап записи даты]'
        return s


class DB_Error_InsertRates(sqlite3.OperationalError):
    def __str__(self):
        s = '\n\r\tОшибка БД [этап записи курсов]'
        return s

class DB_Error_check_data(sqlite3.OperationalError):
    def __str__(self):
        s = '\n\r\tОшибка БД [этап проверки наличия ранее записанных курсов]'
        return s

class DB_Error_select(sqlite3.OperationalError):
    def __str__(self):
        s = '\n\r\tОшибка БД [этап чтения курсов за определённую дату]'
        return s

if __name__ == '__main__':
    pass