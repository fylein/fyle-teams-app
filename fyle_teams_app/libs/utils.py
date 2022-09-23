from typing import Any, Dict, Union

import base64
import datetime
import json

from urllib.parse import quote_plus, urlencode
from babel.numbers import get_currency_precision, get_currency_symbol

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models.base import Model

FYLE_BRANCHIO_BASE_URI = settings.FYLE_BRANCHIO_BASE_URI


def get_or_none(model: Model, **kwargs: Any) -> Union[None, Model]:
    try:
        model_object = model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None
    return model_object


def get_formatted_datetime(datetime_value: datetime, required_format: str) -> str:
    datetime_value = datetime.datetime.fromisoformat(datetime_value)
    formatted_datetime = datetime_value.strftime(required_format)
    return formatted_datetime


def convert_to_branchio_url(url: str, query_params: Dict = None) -> str:
    branchio_url = '{}/branchio_redirect?redirect_uri={}'.format(FYLE_BRANCHIO_BASE_URI, quote_plus(url))
    if query_params is not None:
        encoded_query_params = urlencode(query_params)
        branchio_url = '{}?{}'.format(branchio_url, encoded_query_params)
    return branchio_url


def encode_state(state_params: Dict) -> str:
    state = json.dumps(state_params)

    encoded_state = state.encode()
    base64_encoded_state = base64.urlsafe_b64encode(encoded_state).decode()

    return base64_encoded_state


def decode_state(state: str) -> Dict:
    decoded_state = base64.urlsafe_b64decode(state.encode())
    state_params = json.loads(decoded_state.decode())
    return state_params

def format_currency(currency: str) -> str:
    """
    `format_currency('USD') -> '$'`

    `format_currency('OMR') -> 'OMR '`

    - Returns a formatted representation of a currency code following iso4217, to be used only for representational purposes with amount.
    - If given a currency code for which a symbol is found, returns that symbol as is.
    - If given a currency code for which a symbol is not found, returns the code with a space appended for better readability.
    - Throws `ValueError` if currency is `None`

    More info about iso4217 international standard for currencies - https://en.wikipedia.org/wiki/ISO_4217
    """
    if currency is None:
        raise ValueError('Error while formatting currency: Currency is None!')

    # If the currency doesnt have any symbol, the currency code is returned
    currency_symbol = get_currency_symbol(currency)
    currency_has_symbol = currency != currency_symbol

    # Add a space to the currency, if it the currency doesnt have any symbol
    # Example, if currency is OMR, for amount 100 this will end up displaying OMR 100 instead of OMR100
    formatted_currency = currency_symbol if currency_has_symbol else currency_symbol + ' '
    return formatted_currency


def get_display_amount(amount: Union[str, int, float], currency: str) -> str:
    """
    `get_display_amount(10.56, 'USD') -> '$10.56'`

    `get_display_amount(10.56, 'OMR') -> 'OMR 10.560'`

    `get_display_amount(10.56, 'ISK') -> 'kr11'`

    `get_display_amount(10.56, 'CLF', True) -> '10.5600'`

    - Formats the amount given to the appropriate number of decimal digits as specfied in the iso4217 standard.
    - Prepends a formatted representation of the currency code given to the amount.
    - This function can handle negative amount.
    - Throws `ValueError` if amount is `None` or is invalid.
    - Throws `ValueError` if currency is `None`

    More info about iso4217 international standard for currencies - https://en.wikipedia.org/wiki/ISO_4217
    """

    if amount is None:
        raise ValueError('Error while formatting amount: Amount is None!')

    # Convert and clean the amount, if it is a string
    if isinstance(amount, str):
        # An amount with '.' as the decimal separator and ',' as the thousand separator is expected for conversion to work properly
        cleaned_amount = amount.replace(',', '')
        amount = float(cleaned_amount)

    # Sign to add at the beginning
    sign = '-' if amount < 0 else ''
    amount = abs(amount)

    # Gets the currency precision and symbol for currency specified
    formatted_currency = format_currency(currency)
    currency_precision = get_currency_precision(currency)

    # Create a format string and round the amount to currency precision
    format_string = '{:,.' + str(currency_precision) + 'f}'

    # Format fails for cases like 2.665 and 2.675 both returns 2.67 so adding the 1e-9 helps in handling the precision issues
    # link https://docs.python.org/3/tutorial/floatingpoint.html#tut-fp-issues
    formatted_amount = format_string.format(amount + 1e-9)
    formatted_amount = f'{formatted_currency}{formatted_amount}'

    # Finally, add the sign back to the formatted amount and return the result
    formatted_amount = f'{sign}{formatted_amount}'

    return formatted_amount