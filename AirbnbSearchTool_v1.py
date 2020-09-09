"""
This program asks for input of user's name and prints a friendly welcome
message.  It then asks for user's home currency.
Then it will ask the user to input header and validate header.
The table with options for converting from home currency will display.
Then it prints a total of 9 menu options for the
user to choose from along with the validated header displayed on top.
If user selects 1,2, or 3: Display airbnb rates cross table
(min, avg, or max) but if data not loaded, display error message.
If user selects 4 to 7:  Display rate field tables & allow user to
change filter (by boroughs and/or property types).
If user selects 8:  Load airbnb data.
If user selects 9:  Quit & display goodbye msg.
"""


from enum import Enum
import copy

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

home_currency = ""  # set up global var at module level


class Categories(Enum):  # 2 Enums added for asst 8
    LOCATION = 0  # member of class
    PROPERTY_TYPE = 1


class Stats(Enum):
    MIN = "Minimum"
    AVG = "Average"
    MAX = "Maximum"


class EmptyDatasetError(Exception):
    """ Raise this customized error when a method is asked to do
    calc on the dataset but no data is loaded
    """
    def __init__(self, message):  # updated from 'pass'
        self.message = message


class DataSet:
    """ This class will allow user's input of menu header to be
    validated, retrieved (getter), and changed (setter).
    """

    header_length = 30  # header_length is class attribute

    def __init__(self, header=""):  # default value assigned
        """ This is the constructor method.

        Args:
            header (str):  instance attribute
            _data (str):  airbnb data (list of tuples)
            _labels (dict):  Categories.LOCATION &
                Categories.PROPERTY_TYPE as keys; sets as values
            _active_labels (dict):  Categories.LOCATION &
                Categories.PROPERTY_TYPE as keys;  sets as values
        """
        self._data = None
        try:
            self.header = header
        except ValueError:
            self.header = ""

        self._labels = {}  # initialize 2 dict
        self._active_labels = {}

    @property
    def header(self):  # @property is descriptor
        """ getter method with property decorator which simply returns
        the self._header
        """
        return self._header

    @header.setter
    def header(self, header: str):
        """ setter method with decorator which checks that proposed
        header is string type and less than 30 characters long
        """
        while True:
            if type(header) is str:
                length = len(header)
                if length <= DataSet.header_length and length > 0:
                    self._header = header
                    break
                elif length > DataSet.header_length:
                    raise ValueError
                    continue
                else:
                    raise ValueError
                    continue
            else:
                raise TypeError
                continue

    def _initialize_sets(self):  # for asst 8
        """ This method will populate two dictionaries _labels and
        _active_labels.  Keys are from enums and values are derived from
        self._data which are stored into 4 sets.
        sets for _active_labels represent deepcopies of set1 and set2.
        """
        if self._data == None:
            raise EmptyDatasetError("Please load data first")
        else:
            set1 = set()  # create 4 empty set obj as dict values
            set2 = set()
            for entry in self._data:  # add data into sets
                set1.add(entry[0])
                set2.add(entry[1])
            self._labels = {Categories.LOCATION: set1,
                            Categories.PROPERTY_TYPE: set2}
            self._active_labels = \
                {Categories.LOCATION: copy.deepcopy(set1),
                 Categories.PROPERTY_TYPE: copy.deepcopy(set2)}
        # print(f"self._data:  {self._data}")  # testing asst 8,9
        # print(f"_labels: {self._labels}")
        # print(f"_active_labels: {self._active_labels}")
        # print(f"IDs for labels:  "
        #       f"{id(self._labels)}, {id(self._active_labels)}")
        # IDs differ so ok.

    def load_file(self):
        """ Load csv file as 'ds', remove header in csv, set self._data,
        and return new_ds
        """
        import csv

        with open('AB_NYC_2019.csv', 'r', newline='') as file:
            csvreader = csv.reader(file)
            ds = [row[1:] for row in csvreader]  # skip column_1 csv
            # ds = list(map(tuple, [item[1:] for item in csv_reader]))
        new_ds = ds[1:]  # skip header row from csv
        self._data = new_ds
        total_rows = len(self._data)
        # print(f"self._data:  {self._data}")
        # print(f"new_ds is: {new_ds}")
        self._initialize_sets()
        return new_ds
        return total_rows
        print(new_ds)


    def load_default_data(self):  # not in use for Final Asst
        """ Load sample data into self._data """
        self._data = [("Staten Island", "Private room", 70),
                      ("Brooklyn", "Private room", 50),
                      ("Bronx", "Private room", 40),
                      ("Brooklyn", "Entire home / apt", 150),
                      ("Manhattan", "Private room", 125),
                      ("Manhattan", "Entire home / apt", 196),
                      ("Brooklyn", "Private room", 110),
                      ("Manhattan", "Entire home / apt", 170),
                      ("Manhattan", "Entire home / apt", 165),
                      ("Manhattan", "Entire home / apt", 150),
                      ("Manhattan", "Entire home / apt", 100),
                      ("Brooklyn", "Private room", 65),
                      ("Queens", "Entire home / apt", 350),
                      ("Manhattan", "Private room", 99),
                      ("Brooklyn", "Entire home / apt", 200),
                      ("Brooklyn", "Entire home / apt", 150),
                      ("Brooklyn", "Private room", 99),
                      ("Brooklyn", "Private room", 120)]
        self._initialize_sets()

    def _cross_table_statistics(self, des1: str,
                                des2: str):
        """ This method will provide list of rents for all properties
        that match both descriptors.  If no properties matched both
        descriptors, return a tuple [None, None, None].  Otherwise,
        return min, max, and average rent as a tuple of floats.

        Args:
            des1 (str):  borough
            des2 (str):  property type
        Returns:
            results (float): min, average, max rent as a tuple of floats
        """
        if self._data == None:
            raise EmptyDatasetError("Please load data first")
        try:
            summary = [float(item[2]) for item in self._data if
                       item[0] == des1 and item[1] == des2]
            if summary == []:
                results = [None, None, None]
            results = [min(summary), sum(summary) / len(summary),
                       max(summary)]
        except ValueError:
            results = [None, None, None]

        return results

    def display_cross_table(self, stat: Stats):
        """ This method will print a table of rates for each borough
        and property type.  Print values based on:  Stats.MIN,
        Stats.AVG, Stats.MAX by calling _cross_table_statistics()
        method.  Where results equal to tuple [None, None, None],
        display '$N/A' within rate table instead.

        Args:
            stat(Stats):  MIN, MAX, AVG Enum from class Stats
        """
        if self._data == None:
            raise EmptyDatasetError("Please load data first")
        else:  # dict values into lists to freeze display order
            property_types = list(self._labels.get(Categories.PROPERTY_TYPE))
            boroughs = list(self._labels.get(Categories.LOCATION))
            print("                    ", end="")
            for pt in property_types:  # print col headers first
                print(f"{pt:<26}", end="")
            print("")
            for i in boroughs:  # print row headers
                print(f"{i:<20}", end="")
                for j in property_types:  # calc results for table
                    results = \
                        self._cross_table_statistics(i, j)
                    if results == [None, None, None]:
                        print("$N/A", end="                      ")
                    else:
                        if stat == Stats.MIN:
                            print(f"${results[0]:<25.2f}", end="")
                        elif stat == Stats.AVG:
                            print(f"${results[1]:<25.2f}", end="")
                        elif stat == Stats.MAX:
                            print(f"${results[2]:<25.2f}", end="")
                print("")

    # def total_number_of_items(self):
    #     """ Return total number of lines in the dataset """
    #     return len(self._data)

    def get_labels(self, category: Categories):
        """ getter method which simply returns a list of the items in
        _labels[category]
        """
        if self._data is None or not self._data:
            raise EmptyDatasetError("Please load data first")

        return list(self._labels.get(category))

    def get_active_labels(self, category: Categories):
        """ getter method which simply returns a list of the items in
        _active_labels[category]
        """
        if self._data is None or not self._data:
            raise EmptyDatasetError("Please load data first")

        return list(self._active_labels.get(category))

    def _table_statistics(self, row_category: Categories, label: str):
        """ This method will calc min, max, avg rent for all properties
        in filtered property types

        Args:
            row_category(Categories):  either Category.LOCATION
                or Category.PROPERTY_TYPE for use as row headers in the
                field table  (ie. Category.LOCATION)
            label(str):  match of an item in that row_category
                (ie. "Manhattan")

        Returns:
            results_f(float):  min, avg, max rent as a tuple of floats
                for filtered categories
        """
        active_pts = self._active_labels[Categories.PROPERTY_TYPE]
        active_locations = self._active_labels[Categories.LOCATION]
        summary = []
        if row_category == Categories.LOCATION:
            try:
                for pt in active_pts:
                    for item in self._data:
                        if item[0] == label and item[1] == pt and label \
                                in active_locations:
                            summary.append(float(item[2]))
                if summary == []:
                    results_f = [None, None, None]
                results_f = [min(summary), sum(summary) / len(summary),
                             max(summary)]
            except ValueError:
                results_f = [None, None, None]
        elif row_category == Categories.PROPERTY_TYPE:
            try:
                for location in active_locations:
                    for item in self._data:
                        if item[0] == location and item[1] == label and \
                                label in active_pts:
                            summary.append(float(item[2]))
                if summary == []:
                    results_f = [None, None, None]
                results_f = [min(summary), sum(summary) / len(summary),
                             max(summary)]
            except ValueError:
                results_f = [None, None, None]

        return results_f

    def display_field_table(self, rows: Categories):
        """ This method will print field rates table with labels that
        are currently active & with a display of the filters applied at
        the top

        Args:
            rows(Categories):  either Categories.PROPERTY_TYPES
                or Categories.LOCATION
        """
        if self._data == None:
            raise EmptyDatasetError("Please load data first")
        else:  # change from tuples to lists
            if rows == Categories.LOCATION:
                active_filter_list = list(
                    self._active_labels.get(Categories.PROPERTY_TYPE))
                row_list = list(
                    self._labels.get(Categories.LOCATION))
                active_row_list = list(
                    self._active_labels.get(Categories.LOCATION))
            elif rows == Categories.PROPERTY_TYPE:
                active_filter_list = list(
                    self._active_labels.get(Categories.LOCATION))
                row_list = list(
                    self._labels.get(Categories.PROPERTY_TYPE))
                active_row_list = list(
                    self._active_labels.get(Categories.PROPERTY_TYPE))
            print("The following data are from properties matching "
                  "these criteria:  ")
            for ft in active_filter_list:
                print(f"-  {ft}")  # print A/I filters
            print("")
            print("                    ", end="")
            for sta in Stats:  # print col headers first
                print(f"{sta.value:<21}", end="")
            print("")

            for x in row_list:  # print row headers
                print(f"{x:<20}", end="")
                # for y in active_filter_list:  # calc values for table
                results_f = self._table_statistics(rows, x)
                if results_f == [None, None, None]:
                    print("$N/A                 $N/A                 $N/A",
                          end="")
                    print("")
                else:
                    print(f"${results_f[0]:<20.2f}"
                          f"${results_f[1]:<20.2f}"
                          f"${results_f[2]:<20.2f}", end="")
                    print("")
        print("")

    def toggle_active_label(self, category: Categories, descriptor: str):
        """ This method will add/remove labels from _active_labels.

        Args:
            category(Categories):  either Category.LOCATION or
                Category.PROPERTY_TYPE
            descriptor(str):  values of self._active_labels
        """
        if descriptor in self._labels.get(category):
            if descriptor not in self._active_labels.get(category):
                # round () bracket used along with .get  Else use []
                self._active_labels[category].add(descriptor)
            elif descriptor in self._active_labels.get(category):
                self._active_labels[category].remove(descriptor)
        elif descriptor not in self.get_labels(category):
            raise KeyError


def manage_filters(dataset: DataSet, category: Categories):
    """ This method will print menu-like list of all the labels for the
    given category, show which are active/inactive, then allow user to
    change labels ACTIVE to INACTIVE (or vice versa), loop until user
    is done toggling.
    Note signature line updated from instruction as Enum Classes are at
    module level
    """
    active_flag = ""
    menu_list = []  # create empty list
    if dataset._data == None:
        raise EmptyDatasetError("Please load data first")
    while True:
        print("The following labels are in the dataset:")
        for menu_num, item in enumerate(dataset.get_labels(category), 1):
            active_flag = "ACTIVE" if item in dataset._active_labels[category]\
                else "INACTIVE"
            print(f"{menu_num}:  {item:<20}  {active_flag:<20}")
            menu_list.append(item)
        try:
            my_num = int(input("Please select an item to toggle or "
                               "enter a blank line when you are "
                               "finished:  "))
            if my_num == "":
                break
            item = menu_list[my_num - 1]
            dataset.toggle_active_label(category, item)
            continue
        except ValueError:  # if user enters blank line
            break
        except IndexError:  # if user input number not in menu
            print("Please enter valid number only")
            break


def print_menu():
    """ Display the main menu text. """
    print("Main Menu\n"
          "1 - Print Average Rent by Location and Property Type\n"
          "2 - Print Minimum Rent by Location and Property Type\n"
          "3 - Print Maximum Rent by Location and Property Type\n"
          "4 - Print Min/Avg/Max by Location\n"
          "5 - Print Min/Avg/Max by Property Type\n"
          "6 - Adjust Location Filters\n"
          "7 - Adjust Property Type Filters\n"
          "8 - Load Data\n"
          "9 - Quit")


def menu(dataset: DataSet):
    """ Call currency_options function. Print menu header with menu and
    ask user to input option, then print message after.  Also present
    user with options to access the Airbnb dataset

    Args:
        dataset (str): air_bnb argument from main() function
    """
    currency_options(home_currency)
    my_choice = ""
    print()
    # dataset = DataSet()
    while True:
        print(f"{dataset.header}")  # print menu header
        print_menu()
        try:
            int_my_choice = int(input("What is your choice?"))
        except ValueError:
            print("Please enter a number only")
            continue
        if int_my_choice == 1:
            try:
                dataset.display_cross_table(Stats.AVG)
            except EmptyDatasetError:
                print("Please load data first")
        elif int_my_choice == 2:
            try:
                dataset.display_cross_table(Stats.MIN)
            except EmptyDatasetError:
                print("Please load data first")
        elif int_my_choice == 3:
            try:
                dataset.display_cross_table(Stats.MAX)
            except EmptyDatasetError:
                print("Please load data first")
        elif int_my_choice == 4:
            try:
                dataset.display_field_table(Categories.LOCATION)
            except EmptyDatasetError:
                print("Please load data first")
        elif int_my_choice == 5:
            try:
                dataset.display_field_table(Categories.PROPERTY_TYPE)
            except EmptyDatasetError:
                print("Please load data first")
        elif int_my_choice == 6:
            try:
                manage_filters(dataset, Categories.LOCATION)
            except EmptyDatasetError:
                print("Please load data first")
        elif int_my_choice == 7:
            try:
                manage_filters(dataset, Categories.PROPERTY_TYPE)
            except EmptyDatasetError:
                print("Please load data first")
        elif int_my_choice == 8:
            # ds = DataSet("AB_NYC_2019.csv")
            dataset.load_file()  # to load csv
            print("Data successfully loaded!\n")
        elif int_my_choice == 9:
            break
        else:
            print("Please enter a number between 1 and 9")
    print("Goodbye!  Thank you for using the database\n")


def currency_converter(quantity: float, source_curr: str,
                       target_curr: str):
    """ Convert from one unit of currency to another.

    Args:
        quantity (float): amount of money in the original currency
        source_curr (str): original currency
        target_curr (str): currency after exchange
    Returns:
        converted_amount (float): converted amount post foreign exchange
    """
    converted_amount: float = 0
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
    print(f"Options for converting from {base_curr}:")
    for item in conversions:
        print(f"{item:10}", end="")
    print()
    for number in range(10, 100, 10):  # iterate from 10 to 90 inclusive
        currency_table = ""
        for item in conversions:
            converted_amount = currency_converter(number, base_curr,
                                                  item)
            currency_table = currency_table + f"{converted_amount:<10.2f}"
        print(currency_table)


def main():
    """ Obtain user's name and home currency.  Also ask user for a
    header until a valid header is entered.
    """
    my_name = input("Please enter your name: ")
    print("Hi " + my_name + ", welcome to AirBnB database project.")
    global home_currency
    global conversions
    while home_currency not in conversions:
        home_currency = input("What is your home currency?")
        try:
            source_value = conversions[home_currency]
            break
        except KeyError:
            continue
        return home_currency
    while True:
        my_header = input("Enter a header for the menu:\n")
        try:
            air_bnb = DataSet(my_header)
            break
        except ValueError:
            if len(my_header) > 30:
                print("Header must be less than 30 characters long.")
            else:
                print("Try again.")
            continue
        # return air_bnb
    menu(air_bnb)


def unit_test():  # for Assignment 7
    """ Test _cross_table_statistics """
    print("Testing _cross_table_statistics")

    # testing (asst8)
    ds = DataSet("Airbnb.csv")
    ds.load_default_data()
    # results = ds._cross_table_statistics("Manhattan", "Private room")
    # print("results:  ", results)
    # ds.display_cross_table(Stats.MAX)

    # unit test for menu 4 (asst 9)
    # results_f = ds._table_statistics(Categories.LOCATION, "Manhattan")
    #results_f = ds._table_statistics(Categories.LOCATION, "Queens")
    results_f = ds._table_statistics(Categories.LOCATION, "Manhattan")
    print("results_f (by location) is:  ", results_f)
    ds.display_field_table(Categories.LOCATION)
    # labels_list = ds.get_labels(Categories.LOCATION)
    # print("labels_list from getter method is:", labels_list)
    # active_labels_list = ds.get_active_labels(Categories.LOCATION)
    # print("active_labels_list from getter method is:", active_labels_list)
    # active_labels_list = ds.get_active_labels(Categories.PROPERTY_TYPE)
    # print("active_labels_list from getter method is:", active_labels_list)

    # unit test for menu 5 (asst 9)
    results_f = ds._table_statistics(Categories.PROPERTY_TYPE,
                                     "Entire home / apt")
    results_f = ds._table_statistics(Categories.PROPERTY_TYPE, "Private room")
    print("results_f (by property type) is:  ", results_f)
    ds.display_field_table(Categories.PROPERTY_TYPE)

    # unit test for menu 6 (asst 9)
    #ds.toggle_active_label(Categories.LOCATION, "Manhattan")
    #manage_filters(ds, Categories.LOCATION)

    # unit test for asst 10
    ds.load_file()
    print("Total # rows uploaded from csv: ", len(ds._data))

if __name__ == "__main__":
    main()
    # unit_test()  # for asst 7 but also used for testing 8,9,FinalAsst


r"""
--- sample run #1  ---
Please enter your name: Michelle
Hi Michelle, welcome to AirBnB database project.
What is your home currency?CAD
Enter a header for the menu:
I am Done!!
Options for converting from CAD:
USD       EUR       CAD       GBP       CHF       NZD       AUD       JPY       
7.14      6.43      10.00     5.71      6.79      11.86     11.57     770.86    
14.29     12.86     20.00     11.43     13.57     23.71     23.14     1541.71   
21.43     19.29     30.00     17.14     20.36     35.57     34.71     2312.57   
28.57     25.71     40.00     22.86     27.14     47.43     46.29     3083.43   
35.71     32.14     50.00     28.57     33.93     59.29     57.86     3854.29   
42.86     38.57     60.00     34.29     40.71     71.14     69.43     4625.14   
50.00     45.00     70.00     40.00     47.50     83.00     81.00     5396.00   
57.14     51.43     80.00     45.71     54.29     94.86     92.57     6166.86   
64.29     57.86     90.00     51.43     61.07     106.71    104.14    6937.71   

I am Done!!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice?8
Data successfully loaded!

I am Done!!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice?1
                    Private room              Entire home/apt           Shared room               
Bronx               $66.79                    $127.51                   $59.80                    
Manhattan           $116.78                   $249.24                   $88.98                    
Staten Island       $62.29                    $173.85                   $57.44                    
Brooklyn            $76.50                    $178.33                   $50.53                    
Queens              $71.76                    $147.05                   $69.02                    
I am Done!!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice?2
                    Private room              Entire home/apt           Shared room               
Bronx               $0.00                     $28.00                    $20.00                    
Manhattan           $10.00                    $0.00                     $10.00                    
Staten Island       $20.00                    $48.00                    $13.00                    
Brooklyn            $0.00                     $0.00                     $0.00                     
Queens              $10.00                    $10.00                    $11.00                    
I am Done!!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice?3
                    Private room              Entire home/apt           Shared room               
Bronx               $2500.00                  $1000.00                  $800.00                   
Manhattan           $9999.00                  $10000.00                 $1000.00                  
Staten Island       $300.00                   $5000.00                  $150.00                   
Brooklyn            $7500.00                  $10000.00                 $725.00                   
Queens              $10000.00                 $2600.00                  $1800.00                  
I am Done!!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice?4
The following data are from properties matching these criteria:  
-  Private room
-  Entire home/apt
-  Shared room

                    Minimum              Average              Maximum              
Bronx               $0.00                $87.50               $2500.00             
Manhattan           $0.00                $196.88              $10000.00            
Staten Island       $13.00               $114.81              $5000.00             
Brooklyn            $0.00                $124.38              $10000.00            
Queens              $10.00               $99.52               $10000.00            

I am Done!!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice?5
The following data are from properties matching these criteria:  
-  Bronx
-  Manhattan
-  Staten Island
-  Brooklyn
-  Queens

                    Minimum              Average              Maximum              
Private room        $0.00                $89.78               $10000.00            
Entire home/apt     $0.00                $211.79              $10000.00            
Shared room         $0.00                $70.13               $1800.00             

I am Done!!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice?9
Goodbye!  Thank you for using the database
"""