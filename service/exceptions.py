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


if __name__ == '__main__':
    pass