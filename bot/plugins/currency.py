from typing import Dict

import requests

from .plugin import Plugin


# Author: https://github.com/Chen-IL
class CurrencyPlugin(Plugin):
    """
    A plugin to fetch the daily conversion rate between currencies
    """
    def get_source_name(self) -> str:
        return "exchangerate.host"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "currency_conversion",
            "description": "Convert amounts between various foreign currencies using current day or historic rates",
            "parameters": {
                "type": "object",
                "properties": {
                    "from": {"type": "string", "description": "3-letter currency code of the currency to convert from"},
                    "to": {"type": "string", "description": "3-letter currency code of the currency to convert to"},
                    "date": {"type": "string", "description": "Historic date to get exchange rate (format YYYY-MM-DD). Only if user requests exchange rate for specific date, rather than current rate"},
                    "amount": {"type": "number", "description": "Amount to be converted (defaults to 1)"}
                },
                "required": ["from", "to"],
            },
        }]

    async def execute(self, function_name, **kwargs) -> Dict:
        url = f"https://api.exchangerate.host/convert?from={kwargs['from']}&to={kwargs['to']}"
        if 'date' in kwargs:
            url += f"&date={kwargs['date']}"
        if 'amount' in kwargs:
            url += f"&amount={kwargs['amount']}"
        return requests.get(url).json()
