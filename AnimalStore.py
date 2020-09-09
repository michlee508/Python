# To print dictionary keys, values
def prefix():
    return "|->"

def main():
    animal_classes = {
        "frog": 2.37,
        "elephant": 1000.4362,
        "cat": 35.2375,
        "crow": 0
    }
    for item in animal_classes:
        print(f"The best way to move {item} from A to B.  "
              f"Price is {animal_classes[item]}.")
    print("\nANIMAL              PRICE")
    for item in animal_classes:
        print(f"{prefix()}{item:20}{animal_classes[item]:>10.2f}")  # 2f means 2 decimal places and float

if __name__ == "__main__":
    main()


r"""
--- Sample run ---
The best way to move frog from A to B.  Price is 2.37.
The best way to move elephant from A to B.  Price is 1000.4362.
The best way to move cat from A to B.  Price is 35.2375.
The best way to move crow from A to B.  Price is 0.

ANIMAL              PRICE
|->frog                      2.37
|->elephant               1000.44
|->cat                      35.24
|->crow                      0.00
"""