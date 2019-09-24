import json
from OOP_with_python.utility.My_utility import *


class DataManagement:
    def __init__(self):
        pass

    # Function to calculate price for total quantity of item present in inventory
    def total_price(self, inventory, item):
        quantity_availabe = inventory[item]['weight']
        item_price = quantity_availabe * inventory[item]['price_per_kg']
        return quantity_availabe, item_price


obj = DataManagement()
utility = MyUtility()
data = utility.load_json("/home/akanksha/Akanksha/Company_Work/Felloship/OOP_with_python/utility/out.json")


item_name = input("Enter the item you want to check : ")
quantity, price = obj.total_price(data, item_name)
print("Price for {} kg {} is {}".format(quantity, item_name, price))

