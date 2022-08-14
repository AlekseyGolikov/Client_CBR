
import pytest
import sys, os

service_path=os.getcwd().replace('tests','service')
client_cbr_path=os.getcwd().replace('/tests','')
sys.path.append(service_path)
sys.path.append(client_cbr_path)

import parse

def load_content(date):
    RESPONSE_FILE_NAME = 'response_{}.txt'.format(date.replace('.', '_'))
    try:
        with open(RESPONSE_FILE_NAME, 'r') as f:
            content = f.read()
    except:
        return print('Отказ: файл {} не найден!'.format(RESPONSE_FILE_NAME))
    else:
        return content

#---------------------------------------------------------------------------
# Проверка корректности работы функции парсинга ответа удаленного web-сервиса
@pytest.mark.parametrize('input, expected',[((['364', '51', '124'],load_content('08.08.2022')), [('Армянский драм', '51', 'AMD', 100, '14.8642'), ('Канадский доллар', '124', 'CAD', 1, '46.9656')]), \
                                            pytest.param((['111', '222', '333'],load_content('08.08.2022')), [('Армянский драм', '51', 'AMD', 100, '14.8642'), ('Канадский доллар', '124', 'CAD', 1, '46.9656')], marks=pytest.mark.xfail)])
def test_parse(input,expected):
    (list_of_codes, content) = input
    assert parse.parse(list_of_codes, content) == expected
