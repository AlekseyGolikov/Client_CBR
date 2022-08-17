
import logs
import xmltodict


def parse(list_of_codes, content):
    """
        Функция парсинга ответа от сервера
    :param date: заданная дата; формат ДД.ММ.ГГГГ
    :param list_of_rates: список заданных кодов; формат [XX, XXX, ...]
    :param content: отклик сервера; формат строка типа данных str
    :return: list_of_currency_data - список словарей с информацией по выбранным курсам валют              -
    """
    try:

        d1 = xmltodict.parse(content)
        d2 = d1['soap:Envelope']
        d3 = d2['soap:Body']
        d4 = d3['GetCursOnDateXMLResponse']
        d5 = d4['GetCursOnDateXMLResult']
        d6 = d5['ValuteData']
        d7 = d6['ValuteCursOnDate']
        list_of_currency_data = [valutecurs for valutecurs in d7 if valutecurs['Vcode'] in list_of_codes]

        logs.logger.info('Успешно завершена расшифровка загруженных данных')

        if list_of_currency_data == []:
            list_of_currency_data = False
            logs.logger.info('Отсутствуют данные к загрузке в БД (заданы несуществующие коды)')
    except:
        logs.logger.warning('Обшибка при расшифровке ответа сервера')
        pass
    else:
        return list_of_currency_data


if __name__ == '__main__':

    with open('response_08_08_2022.txt', 'r') as f:
        content = f.read()
    list_of_codes = ['826','840','978','960']
    list_of_currency_data = parse(list_of_codes, content)
    pprint(list_of_currency_data)
