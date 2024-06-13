from record import Record
from adressbook import AddressBook
import pickle
from abc import ABC, abstractmethod

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

class UserInput:
    def __init__(self):
        self.text = input("Enter a command: ")

class ParseInput(UserInput):
    def __init__(self, text):
        self.text = text

    def parse_input(self, text):
        self.text = text
        self.cmd, *self.args = self.text.split()
        self.cmd = self.cmd.strip().lower()
        return self.cmd, *self.args 

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone(s) please."
        except IndexError:
            return "Give me name"
        except KeyError:
            return "There is no such name in the contact list"
        except AssertionError: 
            return "Phone should include 10 digits"

    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error    
def change_username_phone(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
    else:
        return "Contact not found."

@input_error
def phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        if record.phones:
            return ', '.join(phone.value for phone in record.phones)
        else:
            return "No phone numbers available for this contact."
    else:
        return "Contact not found."
    
def all(book):
    list = []
    for name, record in book.items():
        list.append(f"{name}: {', '.join(phone.value for phone in record.phones)}")
    return list


@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    print(args)
    record = book.find(name)
    if record:
        if record.birthday:
            return "Record already has date of Birth"
        else:
            record.add_birthday(birthday)
            return "Birthday added"
    else:
        return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return f"{name}'s birthday is {record.birthday.value.strftime("%d.%m.%Y")}"
        else:
            return "Record hasn't Birthday"
    else:
        return "Contact not found."

@input_error
def birthdays(book):
    return book.birthdays()


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class ComandHello(Command):
    def __init__(self):
        self.text = "How can I help you?"

    def execute(self) -> None:    
        print(self.text)

class CommandExit(Command):
    def __init__(self, book) -> None:
        self.book = book

    def execute(self) -> None:
        save_data(self.book, filename="addressbook.pkl")
        print("Good bye!")

class CommandAddContact(Command):
    def __init__(self, args, book) -> None:
        self.args = args
        self.book = book

    def execute(self) -> None:
        print(add_contact(self.args, self.book))

class CommandChange(Command):
    def __init__(self, args, book) -> None:
        self.args = args
        self.book = book

    def execute(self) -> None:
        print(change_username_phone(self.args, self.book))

class CommandPhone(Command):
    def __init__(self, args, book) -> None:
        self.args = args
        self.book = book

    def execute(self) -> None:
        print(phone(self.args, self.book)) 

class CommandAll(Command):
    def __init__(self, book) -> None:
        self.book = book

    def execute(self) -> None:
        print(all(self.book))

class CommandAddBirthday(Command):
    def __init__(self, book, args) -> None:
        self.args = args
        self.book = book

    def execute(self) -> None:
        print(add_birthday(self.args, self.book))

class CommandShowBirthday(Command):
    def __init__(self, book, args) -> None:
        self.args = args
        self.book = book

    def execute(self) -> None:
        print(show_birthday(self.args, self.book))

class CommandBirthdays(Command):
    def __init__(self, book) -> None:
        self.book = book

    def execute(self) -> None:
        print(birthdays(self.book))

class Invoker:
    def __init__(self) -> None:
        self._hello = None
        self._exit = None
        self._add_contact = None
        self._change = None
        self._phone = None
        self._all = None
        self._add_birthday = None
        self._show_birthday = None
        self._birthdays = None

    def set_hello(self, command: Command):
        self._hello = command
        self._hello.execute()    
        
    def set_add_contact(self, command: Command):
        self._add_contact = command
        self._add_contact.execute()

    def set_exit(self, command: Command):
        self._exit = command
        self._exit.execute()

    def set_change(self, command: Command):
        self._change = command
        self._change.execute()

    def set_phone(self, command: Command):
        self._phone = command
        self._phone.execute()    

    def set_all(self, command: Command):
        self._all = command
        self._all.execute() 

    def set_add_birthday(self, command: Command):
        self._add_birthday = command
        self._add_birthday.execute()     

    def set_show_birthday(self, command: Command):
        self._show_birthday = command
        self._show_birthday.execute() 

    def set_birthdays(self, command: Command):
        self._birthdays = command
        self._birthdays.execute()


def main():
    book = load_data(filename="addressbook.pkl")
    print("Welcome to the assistant bot!")
    while True:
        user_input = UserInput()
        parse = ParseInput(user_input)
        command, *args = parse.parse_input(user_input.text)

        invoker = Invoker()

        if command in ["close", "exit"]:
            invoker.set_exit(CommandExit(book))
            break
        elif command == "hello":
            invoker.set_hello(ComandHello())
        elif command == "add":
            invoker.set_add_contact(CommandAddContact(args, book))
        elif command == "change":
            invoker.set_change(CommandChange(args, book))
        elif command == "phone":
            invoker.set_phone(CommandPhone(args, book))
        elif command == "all":
            invoker.set_all(CommandAll(book))
        elif command == "add-birthday":
            invoker.set_add_birthday(CommandAddBirthday(args, book))
        elif command == "show-birthday":
            invoker.set_show_birthday(CommandShowBirthday(args, book))
        elif command == "birthdays":
            invoker.set_birthdays(CommandBirthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()