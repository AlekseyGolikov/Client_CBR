
import sys
from service import download, parse, db, display, pretty_display
from service.validation import validate_date, validate_codes, validate_input
import logs
from service.exceptions import ValidateInputError, ValidateDateError, ValidateCodeError, DateOutOfRangeError


def init_handler(func):
    def wrapper(*args,**kwargs):
        gen = func(*args,**kwargs)
        next(gen)
        return gen
    return wrapper


@init_handler
def download_handler(successor=None):
    date, list_of_codes = (yield)
    try:
        xml_response = download.download(date)
        if xml_response is None:
            raise
        data = (date, list_of_codes, xml_response)
    except:
        sys.exit(1)
    else:
        successor.send(data)


@init_handler
def parse_handler(successor=None):
    date, list_of_codes, xml_response = (yield)
    try:
        if xml_response:        # xml_response == False, если ответ сервер != 200 или не найден тестовый файл для загрузки в тестовом режиме
            list_of_currency_data = parse.parse(list_of_codes, xml_response)
                # Проверка на наличие исключений
            if list_of_currency_data is None:
                raise
        else:
            list_of_currency_data = False
        data = (date, list_of_currency_data)

    except:
        sys.exit(1)
    else:
        successor.send(data)


@init_handler
def db_handler(successor=None):
    date, list_of_currency_data = (yield)
    with db.DB_manager() as d:
            # list_of_currency_data == False, если в списке кодов переданы значения, которым нет соответствий в ответе сервера
            #                                 либо получен ответ от сервера со статусом != 200,
            #                                 либо не найден файл для загрузки исходных данных в тестовом режиме
            # list_of_currency_data == [(name_1, numeric_code_1,...),(...)], если соответствия есть
        if list_of_currency_data:
            d.insert_date(date)
            d.insert_rates(date, list_of_currency_data)
        successor.send(date)


@init_handler
def print_handler():
    date = (yield)
    with db.DB_manager() as d:
        d.select_pretty(date)
    sys.exit(0)


@init_handler
def validation_handler(successor=None):

    event = (yield)
    try:
        if validate_input() is None:
            raise

        if (date := validate_date(sys.argv[1])) is None:
            raise

        if (list_of_codes := validate_codes(sys.argv[2:])) is None:
            raise

        data = (date, list_of_codes)
    except Exception as ex:
        print(ex)
        sys.exit(1)
    else:
        successor.send(data)


pipeline = validation_handler(download_handler(parse_handler(db_handler(print_handler()))))


if __name__=='__main__':
    pipeline.send('go!')

