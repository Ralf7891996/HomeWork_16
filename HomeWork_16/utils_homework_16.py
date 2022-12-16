import json


def load_json(file):
    """
    Функция принимает Json-файл и возращает данные в списке
    """
    with open(file, 'r', encoding='utf8') as file:
        data = json.load(file)
        return data




