
from datetime import datetime
import sys
import logs


def validate_input():
    """
        Проверка введены ли дата и список цифровых кодов
    """
    try:
        sys.argv[1]
        sys.argv[2]
    except Exception:
        print('     Дата и/или список кодов не введены!')
        print('     Пожалуйста, повторите ввод.')
        print('     Формат ввода даты: ДД.ММ.ГГГГ')
        print('     Формат ввода кодов: ХХ,ХХХ,...; кол-во цифр в коде: 2 или 3;')
        logs.logger.error('Дата и/или список кодов не введены!')
    else:
        return True


def validate_date(date):
    """
        Функция валидации введеных кодов
        Дата должна соответствовать шаблону ДД.ММ.ГГГГ
    :param date: введенная дата
    """
    try:
        datetime.strptime(date, "%d.%m.%Y")
        logs.logger.info('Дата введена корректно: {}'.format(date))
        return date
    except Exception:
        print('     Дата введена не корректно!')
        print('     Пожалуйста, повторите ввод.')
        print('     Формат ввода: ДД.ММ.ГГГГ')
        logs.logger.error('Дата введена не корректно!')


def validate_codes(s):
    """
        Функция валидации введеных кодов.
        Значения кодов должны соответствовать шаблону:
            ХХ,ХХХ,...;
        Пробелы вводить запрещается!
        Допустимое количество цифр в коде: 2 или 3.
    :param s: список цифровых кодов
    """
    try:

        if len(sys.argv)>3:                # проверка на присутствие пробелов в списке с кодами
            raise Exception

        l = s[0].split(',')                # преобразование строки с кодами в список

        try:
            m = [int(x) for x in l]        # проверка на наличие нецифровых символов во введенном списке с цифровыми кодами
        except:
            raise Exception

        n = [x for x in l if len(x)!=2 and len(x)!=3]     # каждый введенный код должен быть либо 2-х, либо 3-х значным числом
        if len(n)>0:
            raise Exception
        logs.logger.info('Список кодов введён корректно: {}'.format(l))
        return l
    except Exception:
        print('     Список кодов введён не корректно!')
        print('     Пожалуйста, повторите ввод.')
        print('     Формат ввода: ХХ,ХХХ,...; кол-во цифр в коде: 2 или 3;')
        logs.logger.error('Список кодов введён не корректно!')


if __name__=='__main__':
    print(sys.argv)
    print(validate_input())
    print(validate_date(sys.argv[1]))
    print(validate_codes(sys.argv[2]))
