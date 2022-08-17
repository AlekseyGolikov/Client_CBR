
import pytest
import sys
from os import path, remove
import os

service_path=os.getcwd().replace('tests','service')
client_cbr_path=os.getcwd().replace('/tests','')
sys.path.append(service_path)
sys.path.append(client_cbr_path)

import db

date = '08.08.2022'
rates1 = [{'Vname':'test1', 'Vnom':'111', 'Vcurs':'11111', 'Vcode':'test1', 'VchCode':'test1'}]
rates2 = [{'Vname':'test1', 'Vnom':'111', 'Vcurs':'11111', 'Vcode':'test1', 'VchCode':'test1'},
          {'Vname':'test2', 'Vnom':'222', 'Vcurs':'22222', 'Vcode':'test2', 'VchCode':'test2'}]
date2 = '09.09.2022'

#---------------------------------------------------------------------------
# Данная фикстура позволяет установить соединение с тестовой БД,
# которая является копией рабочей БД
# После завершения тестовой функции тестовая БД закрывается,
# файл БД автоматически удаляется из каталога
@pytest.fixture(scope='function')
def db_cursor():
    with db.DB_manager('test_db.db') as d:
        yield d
    if path.isfile('test_db.db'):
        remove('test_db.db')

#---------------------------------------------------------------------------
# Проверка корректности работы функции записи даты в БД
def test_insert_date(db_cursor):
    lastrowid = db_cursor.insert_date(date)
    assert lastrowid == 1

#---------------------------------------------------------------------------
# Проверка корректности работы функции записи кодов в БД
def test_insert_rates(db_cursor):
    lastrowid = db_cursor.insert_rates(date, rates1)
    assert lastrowid == 1

#---------------------------------------------------------------------------
# Проверка корректности работы функции проверки входных данных.
# По условию: если в БД имеются записи по дате date и по списку rates,
# то функция формирует и возвращает список тех записей из исходного rates,
# которые отсутствуют в БД
def test_check_data(db_cursor):
    db_cursor.insert_date(date)
    db_cursor.insert_rates(date, rates1)
    result = db_cursor.check_data(date,rates2)
    assert result == [{'Vname':'test2', 'Vnom':'222', 'Vcurs':'22222', 'Vcode':'test2', 'VchCode':'test2'}]


#---------------------------------------------------------------------------
# Проверка корректности работы функции выборки данных из БД
# Фикстура db_cursor
class TstSelect:
    def __init__(self, db_cursor):
        self._db_cursor = db_cursor

@pytest.fixture(scope='function')
def tst_slсt(db_cursor):
    return TstSelect(db_cursor)

@pytest.mark.parametrize('input,expected',[('08.08.2022',[(1, 'test1', 'test1', 'test1', 111, '11111')]),
                                           ('09.09.1999', False)])
def test_select(tst_slсt,input,expected):
    tst_slсt._db_cursor.insert_date('08.08.2022')
    tst_slсt._db_cursor.insert_rates('08.08.2022',rates1)
    result = tst_slсt._db_cursor.select(input)
    assert result == expected
