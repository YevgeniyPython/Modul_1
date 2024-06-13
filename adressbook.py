from collections import UserDict
from datetime import datetime

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value]=record

    def find(self, name):
        for n, record in self.data.items():
            if name==n:
                return record

    def delete(self, name):
        if self.find(name):
            del self.data[name]

    def birthdays(self):
        nowday = datetime.now()
        upcoming_birthdays_list = []
        for name, record in self.data.items():
            if record.birthday:
                this_year_birthday = record.birthday.value.replace(year=nowday.year)
                difference = (nowday - this_year_birthday).days
                if difference >= -7 and difference <= 0:
                    upcoming_birthdays_list.append(f"{name}'s birthday is coming up on {this_year_birthday.strftime("%d.%m.%Y")}")
        return upcoming_birthdays_list