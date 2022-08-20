import pytest
import sys, os

service_path=os.getcwd().replace('tests','service')
client_cbr_path=os.getcwd().replace('/tests','')
sys.path.append(service_path)
sys.path.append(client_cbr_path)


import validation
import exceptions


#---------------------------------------------------------------------------
# Проверка валидности ввода даты
@pytest.mark.parametrize('input, expected',[('01.08.2022','01.08.2022'),
                                            pytest.param('31.11.1999','01.08.2022', marks=pytest.mark.xfail)])
def test_validate_date(input, expected):
    assert validation.validate_date(input) == expected
                    # xfail - пометка набора параметров, которые ожидаемо приведут к сбою


#---------------------------------------------------------------------------
# Проверка валидности ввода кодов
@pytest.mark.parametrize('input,expected',[(['36,51,124'],['36','51','124']),
                                           pytest.param(['3346,51,12ds4'],['36','51','124'], marks=pytest.mark.xfail)])
def test_validate_codes(prepare_sys_args,input,expected):
    """

    :param prepare_sys_args: фикстура для временного удаления элементов sys.argv[1] sys.argv[2:]
    :param input: входной параметр
    :param expected: ожидаемый результат
    :return:
    """
    # print(sys.argv)
    # print(input)
    assert validation.validate_codes(input) == expected


#---------------------------------------------------------------------------
@pytest.fixture(scope='function')
def prepare_sys_args():
    """
        Фикстура prepare_sys_args() временно удаляет элементы sys.argv[1] sys.argv[2:]
        для проверки факта ввода даты и списка кодов
        Применяется с тестовыми функциями test_validate_codes() и test_validate_codes()
    """
    args = []
    for i, _ in enumerate(sys.argv):
        if i > 0:
            args.append(sys.argv.pop(i))

    yield prepare_sys_args

    for arg in args:
        sys.argv.append(arg)


#---------------------------------------------------------------------------
# Проверка ожидаемого исключения при невведённых дате и списке кодов
def test_validate_input(prepare_sys_args):
    """
        Проверка факта ввода даты и списка кодов
    :param prepare_sys_args: фикстура для временного удаления элементов sys.argv[1] sys.argv[2:]
    """
    with pytest.raises(Exception):
        validation.validate_input()
