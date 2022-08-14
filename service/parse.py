import re
import logs
# with open('response10_08_2022.txt','rb') as f:
#     bcontent = f.read()
#     content = bcontent.decode('utf-8')
#     content = content[content.find('<ValuteCursOnDate>'):]


def parse(list_of_codes, content):
    """
        Функция парсинга ответа от сервера
    :param date: заданная дата; формат ДД.ММ.ГГГГ
    :param list_of_rates: список заданных кодов; формат [XX, XXX, ...]
    :param bcontent: отклик сервера; формат строка типа данных bytes
    :return: (date, list_of_codes), где
                - date формат ДД.ММ.ГГГГ тип данных str
                - list_of_currency_data - список с информацией по выбранным курсам валют
                            формат вывода [(name_1, numeric_code_1, alphabetic_code_1, scale_1, rate_1),
                                           (name_2, numeric_code_2, alphabetic_code_2, scale_2, rate_2), ...]
    """
    try:
        # content = bcontent.decode('utf-8')
        content = content[content.find('<ValuteCursOnDate>'):]

            # поиск названий валют
            # на выходе ['Австралийский доллар', 'Азербайджанский манат', ...]
        name_pat = re.compile('[А-Яа-я() ?]+')
        names = [m.group().strip() for m in name_pat.finditer(content) if len(m.group()) > 1]
        # print('Qty: {}; names: {}'.format(len(names), names))

            # поиск номиналов валют
            # на выходе: список с ожидаемыми числами 1, 10, 100, 1000 или 10000
        vnom_pat = re.compile('[1_0?]+')
        subtext = content.replace('<Vnom>','_').replace('</Vnom>','_').replace(' ','')
        scales = [int(m.group().strip('_')) for m in vnom_pat.finditer(subtext) if '_' in m.group()]
        # print('Qty: {}; scales: {}'.format(len(scales), scales))

            # поиск значений курсов валют
            # на выходе список с числами типа float
        vcurs_pat = re.compile('[0-9.]+')
        subtext = content.replace('<Vcurs>','__').replace('</Vcurs>','__').replace(' ','')
        rates = [m.group().strip('__') for m in vcurs_pat.finditer(subtext) if '_' and '.' in m.group()]
        # print('Qty: {}; rates: {}'.format(len(rates), rates))

            # поиск цифровых кодов валют
            # на выходе список с числами типа str
        vcodes_pat = re.compile('[0-9_]+')
        subtext = content.replace('<Vcode>','___').replace('</Vcode>','___').replace(' ','')
        numeric_codes = [m.group().strip('___') for m in vcodes_pat.finditer(subtext) if '_' in m.group()]
        # print('Qty: {}; numeric_codes: {}'.format(len(numeric_codes), numeric_codes))

        # поиск буквенных кодов валют
        # На выходе список строк
        vchcode_pat = re.compile('[A-Z_]+')
        subtext = content.replace('<VchCode>','____').replace('</VchCode>','____').replace(' ','')
        alphabetic_codes = [m.group().strip('____') for m in vchcode_pat.finditer(subtext) if '_' in m.group()]
        # print('Qty: {}; alphabetic_codes: {}'.format(len(alphabetic_codes), alphabetic_codes))

            # выбираем из полного списка курсов валют только те,
            # которые соответствуют заданному перечню кодов
        list_of_currency_data = [x for x in zip(names, numeric_codes, alphabetic_codes, scales, rates) \
                                 if x[1] in list_of_codes]

        logs.logger.info('Успешно завершена расшифровка загруженных данных')

        if list_of_currency_data == []:
            list_of_currency_data = False
            logs.logger.info('Отсутствуют данные к загрузке в БД (заданы несуществующие коды)')
    except:
        logs.logger.warning('Обшибка при расшифровке ответа сервера')
    else:
        return list_of_currency_data


if __name__ == '__main__':

    with open('response10_08_2022.txt', 'rb') as f:
        bcontent = f.read()
    list_of_codes = ['826','840','978','960']
    list_of_currency_data = parse(list_of_codes, bcontent)
    # [print(x) for x in list_of_currency_data if x[1] in list_of_codes]
    # [print(x) for x in zip(names, numeric_codes, alphabetic_codes, scales, rates)]
    # [print(x) for x in list_of_currency_data]
