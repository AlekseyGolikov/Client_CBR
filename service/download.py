
import requests
import datetime
import logs
from random import randint

def getRandomUserAgent():
    user_agents = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
                   "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
                   "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
                   'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0']
    return user_agents[randint(0, len(user_agents) - 1)]

def download(date):
    """
        Загрузка с веб-сервиса DailyInfoWebServ официального курса валют ЦБ РФ
        Используемый метод: GetCursOnDateXML
        Формат даты для передачи в запрос: ГГГГ-ММ-ДДT00:00:00, тип str
    :param date: заданная дата в формате ДД.ММ.ГГГГ, тип str
    :return: XML-ответ сервера в формате протокола SOAP 1.2 (тип bytes)
    """
    url="https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL"
    headers = {'Host': 'www.cbr.ru',
               'Content-Type': 'application/soap+xml; charset=utf-8',
               'Content-Length': '284',
               'user-agent': getRandomUserAgent(),
               'SOAPAction': 'http://web.cbr.ru/GetCursOnDateXML',
    }
    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
      <soap12:Body>
        <GetCursOnDateXML xmlns="http://web.cbr.ru/">
          <On_date>{}</On_date>
        </GetCursOnDateXML>
      </soap12:Body>
    </soap12:Envelope>""".format(str(datetime.datetime.strptime(date, "%d.%m.%Y")).replace(' ','T'))

    # код для реального режима использования (подробно см. README.md)
    try:
        response = requests.post(url, data=body, headers=headers, timeout=5)
    except requests.exceptions.RequestException:
        logs.logger.warning('Невозможно установить соединение с web-сервером: {}'.format(response.status_code))
        return False
    else:
        if response.status_code != 200:
            logs.logger.warning('Отказ. Код ответа сервера: {}'.format(response.status_code))
            return False
        logs.logger.info('Успешно получен ответ от сервера')
        return response.text

    # код для тестового режима (подробно см. README.md)
    # RESPONSE_FILE_NAME = 'tests/response_08_08_2022.txt'
    # try:
    #     with open(RESPONSE_FILE_NAME, 'r') as f:
    #         response = f.read()
    #     logs.logger.warning('Исходные данные успешно загружены из файла {}'.format(RESPONSE_FILE_NAME))
    # except:
    #     logs.logger.warning('Файл {} не найден'.format(RESPONSE_FILE_NAME))
    #     response = False
    # finally:
    #     return response

if __name__=='__main__':
    download(str(datetime.datetime(year=2022, month=8, day=8)).replace(' ','T'))

