import re


def get_money_dict(price):

    def _get_value(str):
        return re.sub("[^0-9]", "", str)

    def _get_currency(str):
        return re.sub("[0-9,.,' ']", "", str)
    
    value = _get_value(price)
    if not value:
        return

    return {
        'value': value,
        'currency': _get_currency(price)
    }
