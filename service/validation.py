
from service.exceptions import DateOutOfRangeError, ValidateInputError, ValidateDateError, ValidateCodeError
from datetime import datetime
import sys
import logs
import re


def validate_input():
    """
        Проверка введены ли дата и список цифровых кодов
    """
    try:
        sys.argv[1]
        sys.argv[2]
    except:
        logs.logger.error('Дата и/или список кодов не введены!')
        raise ValidateInputError()
    else:
        return True


def validate_date(date):
    """
        Функция валидации введеных кодов
        Дата должна соответствовать шаблону ДД.ММ.ГГГГ
    :param date: введенная дата
    """
    try:
        current_date = datetime.now()
        input_date = datetime.strptime(date, "%d.%m.%Y")
    except:
        logs.logger.error('Дата введена не корректно!')
        raise ValidateDateError()

    if input_date > current_date:
        logs.logger.error('Введенная дата {} больше текущей!'.format(date))
        raise DateOutOfRangeError(date)

    logs.logger.info('Дата введена корректно: {}'.format(date))
    return date


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

        # if len(sys.argv)>3:
        if len(s) > 1:                      # проверка на присутствие пробелов в списке с кодами
            raise

        l = s[0].split(',')                 # преобразование строки с кодами в список

        pat = re.compile('\D+')             # шаблон для проверки наличия в строке нецифровых символов
        m = [x for x in l if pat.findall(x) != [] or len(x) > 3 or len(x) < 2]
        # print(m)
        if m != []:
            raise

        logs.logger.info('Список кодов введён корректно: {}'.format(l))

        return l

    except:
        logs.logger.error('Список кодов введён не корректно!')
        raise ValidateCodeError()


if __name__=='__main__':
    print(sys.argv)
    print(validate_input())
    print(validate_date(sys.argv[1]))
    print(validate_codes(sys.argv[2]))
