# Design a library catalog system with a base class LibraryItem and subclasses for different types
# of items like Book, DVD, and Magazine. Include methods to check out, return, and display 
# information about each item.

class LibraryItem:
    def __init__(self, title, author, item_id):
        self.title = title
        self.author = author
        self.item_id = item_id
        self.checked_out = False

    def display_info(self):
        print(f"Title: {self.title}\nAuthor: {self.author}\nItem ID: {self.item_id}\nStatus: {'Checked Out' if self.checked_out else 'Available'}\n")

    def check_out(self):
        if not self.checked_out:
            print(f"Checking out {self.title}")
            self.checked_out = True
        else:
            print(f"{self.title} is already checked out.")

    def return_item(self):
        if self.checked_out:
            print(f"Returning {self.title}")
            self.checked_out = False
        else:
            print(f"{self.title} is not checked out.")


class Book(LibraryItem):
    def __init__(self, title, author, item_id, genre):
        super().__init__(title, author, item_id)
        self.genre = genre


class DVD(LibraryItem):
    def __init__(self, title, director, item_id, duration):
        super().__init__(title, director, item_id)
        self.duration = duration


class Magazine(LibraryItem):
    def __init__(self, title, publisher, item_id, issue_number):
        super().__init__(title, publisher, item_id)
        self.issue_number = issue_number

book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "B001", "Fiction")
dvd1 = DVD("Inception", "Christopher Nolan", "D001", "2 hours 28 minutes")
magazine1 = Magazine("National Geographic", "National Geographic Society", "M001", "March 2023")

book1.display_info()
dvd1.display_info()
magazine1.display_info()

book1.check_out()
dvd1.check_out()
magazine1.check_out()

book1.return_item()
dvd1.return_item()
magazine1.return_item()

book1.display_info()
dvd1.display_info()
magazine1.display_info()
