from collections import defaultdict
from tabulate import tabulate
from bisect import insort


class COLOR:
    def __init__(self, color):
        self.color = color

    COLORS = {
        "INFO": '\033[97m',
        "SUCCUSS": '\033[92m',
        "WARNING": '\033[93m',
        "FAIL": '\033[91m',
        "ENDC": '\033[0m',
        "BOLD": '\033[1m',
        "UNDERLINE": '\033[4m'
    }

    def __enter__(self):
        print(self.COLORS[self.color.upper()])
        return self

    def __exit__(self, *args):
        print(self.COLORS['ENDC'], end='')
        return self


class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __str__(self):
        return '{}: {}'.format(self.name, self.phone)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.name < other.name


class PhoneBook:
    def __init__(self):
        self.contacts = defaultdict(list)

    def __getitem__(self, name):
        letter = name[0].upper()
        index = next(i for i, contact in enumerate(
            self.contacts[letter]) if contact.name == name)
        return self.contacts[letter][index]

    def __delitem__(self, name):
        letter = name[0].upper()
        index = next(i for i, contact in enumerate(
            self.contacts[letter]) if contact.name == name)
        del self.contacts[letter][index]

    def add(self, name, phone):
        letter = name[0].upper()
        insort(self.contacts[letter], Contact(name, phone))

    def delete(self, names: list):
        for name in names:
            self._delete_contact(name)

    def delete(self, name: str):
        self._delete_contact(name)

    def _delete_contact(self, name: str):
        try:
            del self[name]
            with COLOR('SUCCUSS'):
                print('Contact deleted')
        except Exception:
            with COLOR('FAIL'):
                print('Contact not found')

    def edit(self, name, phone):
        try:
            self[name].phone = phone
            with COLOR('SUCCUSS'):
                print('Phone number changed')
        except Exception:
            with COLOR('FAIL'):
                print('Contact not found')

    def __str__(self):
        return '\n'.join(
            '{}:\n   {}'.format(letter, ', '.join(map(str, contacts)))
            for letter, contacts in self.contacts.items())


def add_contact():
    with COLOR('INFO'):
        name = input("Please enter the name: ")
        phone = input("Please enter the phone number: ")
        phone_book.add(name, phone)


def delete_contact():
    with COLOR('INFO'):
        name = input("Please enter the name: ")
        phone_book.delete(name)


def edit_contact():
    with COLOR('INFO'):
        name = input("Please enter the name: ")
        phone = input("Please enter the phone number: ")
        phone_book.edit(name, phone)


def print_contacts():
    with COLOR('Warning'):
        print(phone_book)


def quit():
    with COLOR('INFO'):
        print("Goodbye!")
    exit()


def main():
    COMMANDS = {
        1: add_contact,
        2: edit_contact,
        3: delete_contact,
        4: print_contacts,
        5: quit
    }

    while (True):
        # clear the terminal
        print("\033c")

        with COLOR('INFO'):
            print(tabulate(
                [(i, " ".join(command.__name__.split("_")).title())
                    for i, command in COMMANDS.items()],
                headers=['#', 'Command']))

            # get command
            selection = input("\nPlease enter your selection: ")

        # check if selection is valid
        if not selection.isdigit() or int(selection) not in range(1, 6):
            with COLOR('FAIL'):
                print("Invalid selection", end='')
                input("\nPress Enter to continue...")
            continue

        # call the function associated with the command
        COMMANDS[int(selection)]()

        with COLOR('INFO'):
            input("\nPress Enter to continue...")


if __name__ == '__main__':
    phone_book = PhoneBook()
    main()
