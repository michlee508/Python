def currency_converter(quantity: float, source_curr: str, target_curr: str):
    """ Calculate value after converting money from one currency to
    another

    Args:
        quantity (float): amount of money in the original currency
        source_curr (str): original currency
        target_curr (str): currency after exchange
    Returns:
        float:
    """
    conversions = {
        "USD": 1,
        "EUR": .9,
        "CAD": 1.4,
        "GBP": .8,
        "CHF": .95,
        "NZD": 1.66,
        "AUD": 1.62,
        "JPY": 107.92
    }
    print(conversions)
    print(conversions.keys())
    print(conversions.values())
    target_amount = quantity * conversions["USD"] / conversions[source_curr] \
                    * conversions[target_curr]
    return target_amount

print(f"\nForeign Exchange Rate (from USD to CAD) is:  ",currency_converter(1,"USD","CAD"))


r"""
--- Sample Run  ---
{'USD': 1, 'EUR': 0.9, 'CAD': 1.4, 'GBP': 0.8, 'CHF': 0.95, 'NZD': 1.66, 'AUD': 1.62, 'JPY': 107.92}
dict_keys(['USD', 'EUR', 'CAD', 'GBP', 'CHF', 'NZD', 'AUD', 'JPY'])
dict_values([1, 0.9, 1.4, 0.8, 0.95, 1.66, 1.62, 107.92])

Foreign Exchange Rate (from USD to CAD) is:   1.4
"""