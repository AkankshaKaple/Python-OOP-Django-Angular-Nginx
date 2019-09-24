import re
from datetime import date
from OOP_with_python.utility.My_utility import *


class Regex:
    def __init__(self):
        self.number = "1122334455"

    def regex(self, data):
        # Replace name at every position by user_name
        replace_name = re.sub('<<name>>', "Akanksha", data)
        replace_f_name = re.sub('<<.*name>>', "Akanksha Kaple", replace_name)

        # Replace xxxxxxxxx with contact number
        replace_num = re.sub("\w*x", self.number, replace_f_name)

        # Get current date
        today = date.today().strftime("%d/%m/%Y")
        replace_date = re.sub("\w+(\/)\w+(\/)\w+", today, replace_num)
        return replace_date


obj = Regex()
utility = MyUtility()
data = utility.load_file("/home/akanksha/Akanksha/Company_Work/Felloship/OOP_with_python/persons_info.txt")
print("ORIGINAL DATA :\n", data)
result = obj.regex(data)
print("RESULT : \n", result)
utility.store_file(result, "regex_output.txt")