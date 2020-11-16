from typing import Dict, List
from testApi.models import cursor, connection


def insert(table: str, column_values: Dict):
    """
    todo add try/except and exceptions processing; for now it's suitable only for registration case
    """
    columns = ', '.join(column_values.keys())
    values = [v for v in column_values.values()]
    placeholders = f'\'{values[0]}\', \'{values[1]}\''
    cursor.execute(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders});")
    connection.commit()


def select(table: str, values: Dict) -> List:
    """
    todo add try/except and exceptions processing; for now it's suitable only for login case
    """
    values_ToSelect = values['select_values']
    condition = values['condition']
    cursor.execute(
        f"SELECT {values_ToSelect} "
        f"FROM {table} "
        f"WHERE username =\'{condition['username']}\';")
    result = cursor.fetchall()
    return result


def insert_currency(table: str, values: Dict):
    """
    add prices for chosen currency. if on these dates data already exist do nothing.
    :param table:
    :param values:
    """
    placeholders = ', '.join([f"('{date}',{price})" for date, price in zip(values['date'], values['price'])])
    query = f"INSERT INTO {table} " \
            f"(date, price) " \
            f"VALUES {placeholders} on conflict (date) do nothing;"
    cursor.execute(query)
    connection.commit()
