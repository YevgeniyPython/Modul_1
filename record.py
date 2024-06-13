from name import Name
from phone import Phone
from birthday import Birthday

class Record():
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_phone(self, phone):
        if self.phones:
            phone_list = []
            for i in self.phones:
                phone_list.append(i.value)
            if phone not in phone_list:
                self.phones.append(Phone(phone))
        else:
            self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)

    def edit_phone(self, phone, new_phone):
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                self.phones[i]=Phone(new_phone)

    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                return i 
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
    
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_birthday("12.01.2021")
# john_record.add_birthday("13.01.2021")
# john_record.add_phone("5555555555")
# john_record.add_phone("1211121212")
# john_record.remove_phone("1211121212")
# john_record.edit_phone("1234567890", "0987654321")
# john_record.find_phone("5555555555")

# print(f"{john_record.find_phone("5555555555")}")

# print(str(john_record))
