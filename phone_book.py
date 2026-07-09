class members:
    def __init__(self, first_name, last_name, number):
        self.first_name = first_name
        self.last_name = last_name
        self.number = number

    def __str__(self):
        return f"first name: {self.first_name} | last name: {self.last_name} | number: {self.number}"

class cell_phone:
    def __init__(self):
        self.members = []

    def add_member(self, first_name, last_name, number):
        for member in self.members:
            if member.first_name.lower() == first_name.lower() and member.last_name.lower() == last_name.lower():
                print(f"this member is already exists!")
                return
        if not number.isdigit() or len(number) != 11:
            print("input is invaild, please try agine.")
            return
        elif not first_name.strip() or not last_name.strip():
             print("input is invaild, please try agine.")
             return
        m_info = members(first_name, last_name, number)
        self.members.append(m_info)
        print(f"{first_name} {last_name} added successfully.")

    def remove_member(self, first_name, last_name):
        member_to_remove = None
        for member in self.members:
            if member.first_name.lower() == first_name.lower() and member.last_name.lower() == last_name.lower():
                member_to_remove = member
                break
        if member_to_remove:
            self.members.remove(member_to_remove)
            print(f"{first_name} {last_name} removed")
        else:
            print(f"{first_name} {last_name} is not in list")

    def search_member(self, first_name, last_name):
        found = False
        for member in self.members:
            if member.first_name.lower() == first_name.lower() and member.last_name.lower() == last_name.lower():
                print(f"found: {member}")
                found = True
                break
        if not found:
            print("this member is not exists!")

    def all_members(self):
        if not self.members:
            print("List is empty.")
            return
        print("The members:\n↓↓↓↓↓↓↓↓↓")
        for member in self.members:
            print(member)

phonebook = cell_phone()

while True:
    print("-----phone book-----")
    print("1. members list")
    print("2. add member")
    print("3. remove member")
    print("4. search member")
    print("5. exit")
    print("------------------------------------------------------")

    choice = input("enter a number between 1 and 5: ")

    if choice == "1":
        phonebook.all_members()

    elif choice == "2":
        first_name = input("first name: ")
        last_name = input("last name: ")
        number = input("number: ")
        phonebook.add_member(first_name, last_name, number)

    elif choice == "3":
        first_name = input("first name: ")
        last_name = input("last name: ")
        phonebook.remove_member(first_name, last_name)

    elif choice == "4":
        first_name = input("first name: ")
        last_name = input("last name: ")
        phonebook.search_member(first_name, last_name)

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid input. Please try again.")
        continue
