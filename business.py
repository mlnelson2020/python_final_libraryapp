'''
This file contains the code associated with objects for the Library Management Program.

Written by: Mary Nelson
Date: 05/10/2024
'''

from dataclasses import dataclass

@dataclass
class Book:
    title:str = ""
    author:str = ""
    pages:int = 0
    readStatus:str = ""
    review:int = 0
    notes:str = ""
    bookID:int = 0
    serial:int = 0


class Library:
    def __init__(self):
        self.books = []

    # calculate total pages read
    @property
    def totalPagesRead(self):
        totalPagesRead = sum(book.pages for book in self.books if book.readStatus == "read")
        return totalPagesRead

    # calculate total books marked read
    @property
    def totalBooksRead(self):
        totalBooksRead = len([book for book in self.books if book.readStatus == "read"])
        return totalBooksRead

    # calculate total books marked unread
    @property
    def numBooksTBR(self):
        numBooksTBR = len([book for book in self.books if book.readStatus == "unread"])
        return numBooksTBR

    @property
    def count(self):
        return len(self.books)

    def add(self, book):
        return self.books.append(book)

    def remove(self, bookID):
        return self.books.pop(bookID-1)

    def get(self, bookID):
        return self.books[bookID-1]

    def set(self, bookID, book):
        self.books[bookID-1] = book

    def move(self, oldBookID, newBookID):
        book = self.books.pop(oldBookID-1)
        self.books.insert(newBookID-1, book)

    def __iter__(self):
        for book in self.books:
            yield book

def main():
    library = Library()
    for book in library:
        print(book.bookID, book.title, book.author, book.pages, book.readStatus, book.review, book.totalPagesRead)

    print("Bye!")

if __name__ == "__main__":
    main()
