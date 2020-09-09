""" Currency Converter Table v1 """


home_currency = ""  # set up global variable in module
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


class DataSet:
    """ This DataSet class will allow user's input of menu header to be
    validated, retrieved (getter), and changed (setter).
    """
    header_length = 30  # class attribute

    def __init__(self, header: str):
        """ This is the constructor method.

        Args:
            header (str):  instance attribute
        """
        self._data = None
        self.header = header

    @property
    def header(self):
        """ getter method with property decorator which simply returns
        the self._header
        """
        return self._header

    @header.setter
    def header(self, header: str):
        """ setter method with decorator which checks that proposed
        header is string type and less than 30 characters long
        """
        while type(header) is str:
            length = (len(header))
            if length == 0:
                self._header = ""
                header = input("No blanks. Enter a header for the menu:\n")
                continue
            elif length > DataSet.header_length:
                print("Header must be a string less than 30 characters "
                      "long.")
                self._header = ""
                header = input("Enter a header for the menu:\n")
                continue
            else:
                self._header = header
                break


def currency_options(base_curr='EUR'):
    """ Print table of options for converting base_curr to all other
    currencies

    Args:
        base_curr (str):  user's home currency
    Returns:
        converted_amount (float):  converted amount post foreign exchg
        currency_table (str):  converted amounts in all other currencies
    """
    global home_currency
    base_curr = home_currency
    print("Options for converting from USD:\n"
          "USD      EUR      CAD      GBP      CHF      NZD      AUD"
          "      JPY")
    for number in range(10, 100, 10):  # iterate from 10 to 90 inclusive
        currency_table = ""
        for item in conversions:
            converted_amount = currency_converter(number, base_curr, item)
            currency_table = currency_table + f"{converted_amount:<9.2f}"
        print(currency_table)


def currency_converter(quantity: float, source_curr: str,
                       target_curr: str):
    """ Calculate value after converting money from one currency to
    another

    Args:
        quantity (float): amount of money in the original currency
        source_curr (str): original currency
        target_curr (str): currency after exchange
    Returns:
        converted_amount (float): converted amount post foreign exchange
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
    target_amount : float = 0
    if quantity <= 0:
        raise ValueError
    while quantity > 0:
        try:
            source_value = conversions[source_curr]
            target_value = conversions[target_curr]
        except KeyError:
            raise KeyError
        converted_amount = round(quantity * target_value /
                              source_value, 2)
        return converted_amount


def menu(dataset):  # Add a parameter dataset of type DataSet
    """ Call currency_options function. Print menu header with menu and
    ask user to input option, then print message after

    Args:
        dataset (str): air_bnb argument from main()
    """
    currency_options(home_currency)
    print(f"\nThank you for using the currency converter!  Goodbye!")


def main():
    """ Obtain user's name and home currency.  Also ask user for a
    header until a valid header is entered.
    """
    print("Welcome to my currency converter tool")
    global home_currency
    global conversions
    while home_currency not in conversions:
        home_currency = input("What is your home currency?  (ie. CAD/USD/EUR/JPY/GBP): ")
        try:
            source_value = conversions[home_currency]
            break
        except KeyError:
            continue
        return home_currency
    while True:
        my_header = input("Enter your name:  ")
        if my_header == None:
            continue
        try:
            air_bnb = DataSet(my_header)
            break
        except ValueError:
            continue
        return air_bnb
    menu(air_bnb)


if __name__ == "__main__":
    main()


r"""
--- Sample output ---
Welcome to my currency converter tool
What is your home currency?  (ie. CAD/USD/EUR/JPY/GBP): JPY
Enter your name:  Michelle
Options for converting from USD:
USD      EUR      CAD      GBP      CHF      NZD      AUD      JPY
0.09     0.08     0.13     0.07     0.09     0.15     0.15     10.00    
0.19     0.17     0.26     0.15     0.18     0.31     0.30     20.00    
0.28     0.25     0.39     0.22     0.26     0.46     0.45     30.00    
0.37     0.33     0.52     0.30     0.35     0.62     0.60     40.00    
0.46     0.42     0.65     0.37     0.44     0.77     0.75     50.00    
0.56     0.50     0.78     0.44     0.53     0.92     0.90     60.00    
0.65     0.58     0.91     0.52     0.62     1.08     1.05     70.00    
0.74     0.67     1.04     0.59     0.70     1.23     1.20     80.00    
0.83     0.75     1.17     0.67     0.79     1.38     1.35     90.00    

Thank you for using the currency converter!  Goodbye!

"""