from flask_restful import Resource, reqparse
from testApi.models import db
import psycopg2
from typing import Dict, NamedTuple
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
import requests
import xmltodict
import logging

logging.basicConfig(filename='api_logs.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

logger = logging.getLogger()

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)

parser_currency = reqparse.RequestParser()
parser_currency.add_argument('date1', help='This field cannot be blank', required=True)
parser_currency.add_argument('date2', help='This field cannot be blank', required=True)
parser_currency.add_argument('name', help='This field cannot be blank', required=True)

parser_currency_save = reqparse.RequestParser()
parser_currency_save.add_argument('name', help='This field cannot be blank', required=True)
parser_currency_save.add_argument('date', help='This field cannot be blank', required=True, action='append')
parser_currency_save.add_argument('price', help='This field cannot be blank', required=True, action='append')


class UserModel(NamedTuple):
    """
    represents user data in UserRegistration and UserLogin
    """
    name: str
    password: str

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, _hash):
        return sha256.verify(password, _hash)


class Currency(NamedTuple):
    """
    represents currency data in GetCurrency
    """
    date1: str
    date2: str
    code: str


class UserRegistration(Resource):
    def post(self) -> Dict:
        """
        accept json format:
            {
                "username": str: user name, ex: "Vasya",
                "password": str: password, ex: "qwerty"
            }
        todo finalize exceptions processing
        :return:
        """
        data = parser.parse_args()
        current_user = UserModel
        current_user.name, current_user.password = data['username'], UserModel.generate_hash(data['password'])
        print(current_user.password)
        try:
            db.insert('test_user', {'username': current_user.name, 'password': current_user.password})
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                    'message': 'User registration',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }
        except psycopg2.errors.UniqueViolation:
            return {'message': 'This name already existed'}
        except Exception as e:
            logger.exception(f'There is exception: {e} in api.endpoint module in UserRegistration class')
            return {'message': 'something goes wrong'}


class UserLogin(Resource):
    def post(self) -> Dict:
        """
        accept json format:
            {
                "username": "str: user name, ex: "Vasya",
                "password": "str: password, ex: "qwerty"
            }
        todo finalize exceptions processing
        """
        data = parser.parse_args()
        current_user = UserModel
        current_user.name, current_user.password = data['username'], UserModel.generate_hash(data['password'])
        try:
            password_FromDatabase = db.select('test_user',
                                              {'select_values': 'password',
                                               'condition': {'username': current_user.name}})[0]
            if len(password_FromDatabase) == 0:
                return {'message': f'User {current_user.name} doesn\'t exist'}
            if current_user.verify_hash(current_user.password, password_FromDatabase[0]):
                access_token = create_access_token(identity=data['username'])
                refresh_token = create_refresh_token(identity=data['username'])
                return {
                        'message': f'Logged as {current_user.name}',
                        'access_token': access_token,
                        'refresh_token': refresh_token
                        }
            else:
                return {'message': 'Wrong credentials'}
        except Exception as e:
            logger.exception(f'There is exception: {e} in api.endpoint module in UserLogin class')
            return {'message': 'Can\'t login'}


class GetCurrency(Resource):
    """
    obtain currency prices from http://www.cbr.ru/
    """
    def post(self) -> Dict:
        """
        accept json format:
            {
                "date1": str: %dd/%MM/%YY, ex: "02/11/2020,
                "date2": str: %dd/%MM/%YY, ex: "05/11/2020",
                "name": str: currency name, ex: "Australian Dollar"
            }
        :return: {'currency': list of prices}
        """
        data = parser_currency.parse_args()
        currency_code = _get_currency_code(data['name'])
        currency = Currency
        currency.date1, currency.date2, currency.code = data['date1'], data['date2'], currency_code
        try:
            return {'currency': _get_currency(currency.date1, currency.date2, currency.code)}
        except Exception as e:
            logger.exception(f'There is exception: {e} in api.endpoint module in GetCurrency class')
            return {'message': 'Can\'t get currency'}


class SaveCurrency(Resource):
    """
    save currency prices to database
    """
    def post(self):
        """
            accept json format:
            {
                "name": str: currency name, ex: "Australian Dollar"),
                "date": list: list of dates, ex: [
                    "05/11/2020",
                    "02/11/2020"
                    ],
                "price": list: list of prices, ex: [
                    1.1,
                    2.2
                    ]
            }
        """
        data = parser_currency_save.parse_args()
        try:
            database_table_name = _currency_database_name(data['name'])
            db.insert_currency(database_table_name, {
                'date': data['date'],
                'price': data['price']
            })
            return {'message': 'Saved'}
        except psycopg2.errors.UniqueViolation as not_unique:
            print(not_unique.detail)
        except Exception as e:
            logger.exception(f'There is exception: {e} in api.endpoint module in SaveCurrency class')
            return {'message': 'Can\'t save to database'}


def _get_currency_code(currency_name: str) -> str:
    """
    internal helper function to obtain the currency code
    details: http://www.cbr.ru/development/sxml/
    """
    url = 'http://www.cbr.ru/scripts/XML_val.asp?d=0'
    currency_name = currency_name
    response = requests.get(url)
    parsed_response = xmltodict.parse(response.content)
    filtered = list(filter(lambda x: x['EngName'] == currency_name, parsed_response['Valuta']['Item']))[0]
    return filtered['ParentCode']


def _get_currency(date1: str, date2: str, code: str) -> xmltodict.OrderedDict:
    """
    internal helper function to obtain the currency prices
    details: http://www.cbr.ru/development/sxml/
    :param date1: format %dd/%MM/%YY
    :param date2: format %dd/%MM/%YY
    :param code: currency code returned from _get_currency_code(currency_name)
    """
    url = f'http://www.cbr.ru/scripts/XML_dynamic.asp?' \
          f'date_req1={date1}&' \
          f'date_req2={date2}&' \
          f'VAL_NM_RQ={code}'
    response = requests.get(url)
    parsed_response = xmltodict.parse(response.content)
    return parsed_response['ValCurs']['Record']


def _currency_database_name(name: str) -> str:
    """
    just forget about this function's existing
    """
    database_names = {
        'Australian Dollar': 'AUD',
        'British Pound Sterling': 'GBP',
        'Japanese Yen': 'JPY',
        'China Yuan': 'CNY'
    }
    return database_names[name]


# tests and haven't implemented
class SecretResource(Resource):
    """
    test jwt
    """
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }


class UserLogoutAccess(Resource):
    """
    will be added later
    """

    def post(self):
        return {'message': 'User logout'}


class UserLogoutRefresh(Resource):
    """
    will be added later
    """

    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    """
    will be added later
    """

    def post(self):
        return {'message': 'Token refresh'}


class TestApi(Resource):
    def get(self):
        return 'Test API'
