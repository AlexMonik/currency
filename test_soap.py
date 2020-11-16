import requests
import xmltodict
data = {
    'date1': '02/03/2018',
    'date2': '02/04/2018',
    'code': 'R01010'
}


def _get_currencies():
    url = f'http://www.cbr.ru/scripts/XML_dynamic.asp?' \
          f'date_req1={data["date1"]}&' \
          f'date_req2={data["date2"]}&' \
          f'VAL_NM_RQ={data["code"]}'
    response = requests.get(url)
    answer = xmltodict.parse(response.content)
    print(answer['ValCurs']['Record'])


def _get_currency_code():
    url_code = 'http://www.cbr.ru/scripts/XML_val.asp?d=0'
    cur_name = 'Australian Dollar'
    response = requests.get(url_code)
    answer = xmltodict.parse(response.content)
    filtered = list(filter(lambda x: x['EngName'] == cur_name, answer['Valuta']['Item']))[0]
    print(filtered['ParentCode'])


def _make():
    value1 = [1, 2, 3]
    value2 = [55, 66, 77]
    rez = ', '.join([f'({v1},"{v2}")' for v1, v2 in zip(value1, value2)])
    print(rez)

_make()