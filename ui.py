'''
Library Management Program
This program allows a user to manage their personal library by adding, removing,
and updating books by interacting with a database.
This file contains the user interface code.

Written by: Mary Nelson
Date: 05/10/2024
'''

import db
from business import Book, Library

STATUS = ("read", "unread")
REVIEW_OPTIONS = (1, 2, 3, 4, 5)

def add_book(library):
    while True:
        title_valid = False
        author_valid = False
        pages_valid = False
        
        while not title_valid:
            title = input("Title: ").strip()
            if not title:
                print("Title cannot be blank. Please try again.")
            else:
                title_valid = True
        
        while not author_valid:
            author = input("Author: ").strip()
            if not author:
                print("Author cannot be blank. Please try again.")
            else:
                author_valid = True
        
        while not pages_valid:
            pages_input = input("Number of pages: ").strip()
            if not pages_input:
                print("Pages cannot be blank. Please try again.")
            elif not pages_input.isdigit():
                print("Pages must be a number. Please try again.")
            else:
                pages = int(pages_input)
                if pages <= 0:
                    print("Pages must be a number. Please try again.")
                else:
                    pages_valid = True
                    break  

        if title_valid and author_valid and pages_valid:
            # Break once above input is valid and continues 
            break  
        
    readStatus = get_read_status()
    
    if readStatus == "unread":
        bookID = len(library.books) + 1
        review = ""  
        book = Book(title, author, pages, readStatus, bookID=bookID)
        library.add(book)
        db.add_book(book)
        print(f"{book.title} was added.\n")
    else:
        # Prompt for review only if the book is marked as read
        review = get_review(readStatus)  
        notes = None
        
        bookID = len(library.books) + 1
        book = Book(title, author, pages, readStatus, review, notes, bookID=bookID)
        library.add(book)
        db.add_book(book)

        # Get notes for book (It was having trouble linking the notes to the correct bookID)
        notes = get_notes(library, library.count)
        book.notes = notes
        db.update_book(book)
        print(f"{book.title} was added.\n")
    

def get_read_status(bookID=None):
    if bookID is None:
        while True:
            readStatus = input("Status (read or unread): ").lower()
            if readStatus in STATUS:
                return readStatus
            else:
                print("Invalid entry. Please enter 'read' or 'unread'.")
    else:
        while True:
            readStatus = input(f"Status for book {bookID} (read or unread): ").lower()
            if readStatus in STATUS:
                return readStatus
            else:
                print("Invalid entry. Please enter 'read' or 'unread'.")

# Get review when book status is marked "read", skips if "unread"
def get_review(readStatus):
    if readStatus == "read":
        while True:
            review = input("Please enter a number between 1 and 5\nfor your review where 5 = great and 1 = terrible: ")
            if review == "":
                print("Review cannot be blank. Please try again.")
            elif review.isdigit():
                review = int(review)
                if review in REVIEW_OPTIONS:
                    return review
                else:
                    print("Invalid entry. Please try again.")
            else:
                print("Invalid entry. Please try again.")
    else:
        return None

def get_notes(library, bookID=None, is_get_notes=True, is_menu_option_5=False):
    if library.count == 0:
        print("Your library is empty. There are no books to edit notes.\n")
        return
    
    if bookID is None:
        bookID = get_bookID(library, "Book ID: ")
    
    # Get the selected book
    book = library.get(bookID)
    # Only print if is_get_notes is True and called from menu option 5
    if book and is_get_notes and is_menu_option_5:
        print(f"You selected {book.title}")
    
    while True:
        notes = input("Please enter notes (optional - up to 15 characters): ")

        # Check if notes are provided and validate length
        if notes:
            max_notes_length = 15  
            if len(notes) > max_notes_length:
                print(f"Note exceeds max of {max_notes_length} characters. Please try again.")
            else:
                # Update notes for the book in the library and database
                if book:
                    book.notes = notes
                    db.update_book(book)
                    if is_menu_option_5:  
                        print(f"Notes for {book.title} updated.")
                    return notes
                else:
                    print("Book not found.")
        else:
            # Update notes to an empty string to overwrite existing notes
            if book:
                book.notes = ""
                db.update_book(book)
                if is_menu_option_5:  
                    print(f"Notes for {book.title} updated.")
            else:
                print("Book not found.")
            return ""

# Retrieve book from library for actions
def get_bookID(library, prompt):
    while True:
        try:
            num = int(input(prompt))
        except ValueError:
            print ("Invalid entry, please enter a number between 1 and {library.count}.")
            continue

        if num < 1 or num > library.count:
            print(f"Invalid entry, please enter a number between 1 and {library.count}.")

        else:
            return num

def remove_book(library):
    if library.count == 0:
        print("Your library is empty. There are no books to remove.\n")
        return

    while True:
        num = get_bookID(library, "Book ID: ")
        if num < 1 or num > library.count:
            print(f"Invalid book ID. Please enter a number between 1 and {library.count}.")
        else:
            break  

    book = library.remove(num)
    db.remove_book(book.bookID)
    db.update_library(library)
    print(f"{book.title} was removed.\n")

# Update status, review, and ntoes for a book in library
def update_book(library, bookID=None):  
    if library.count == 0:
        print("Your library is empty. There are no books to update.\n")
        return

    if bookID is None:
        while True:
            bookID = get_bookID(library, "Book ID: ")
            if bookID < 1 or bookID > library.count:
                print(f"Invalid book ID. Please enter a number between 1 and {library.count}.")
            else:
                break  
    book = library.get(bookID)
    print(f"You selected {book.title}. Read Status = {book.readStatus}, Review = {book.review}, Notes = {book.notes}")

    readStatus = get_read_status(bookID)
    previous_read_status = book.readStatus   
    book.readStatus = readStatus

    # Set review field to empty string in db if status changes from "read" to unread"
    if previous_read_status == "read" and readStatus == "unread":
        book.review = ""
    else:
        if readStatus == "read":
            book.review = get_review(readStatus)
        else:
            book.review =""
    
    get_notes(library, bookID)
    db.update_book(book)
    print(f"{book.title} was updated.\n")

def display_library(library):
    if library.count == 0:
        print("\nYour library is empty. Please add some books to get started.")        
    else:
        print()
        print(f"Total Books Read: {library.totalBooksRead}\t---\tBooks To Be Read: {library.numBooksTBR}\nTotal Pages Read: {library.totalPagesRead}")
        line()
        print(f"{'ID':3} {'Title':24} {'Author':17} {'Pages':6} {'Status':7} {'Review':7} {'Notes'}")
        line()

        # Ensure review/notes display either data or nothing at all if null.
        for book in library:
            review = "" if book.readStatus == "unread" else str(book.review) if book.review is not None else ""
            notes = book.notes 

            # Adjust formatting for title and author for long entries
            title = str(book.title)[:20] + "..." if len(str(book.title)) > 20 else str(book.title)
            author = str(book.author)[:14] + "..." if len(str(book.author)) > 14 else str(book.author)

            print(f"{book.bookID:<3} {title:<24} {author:<17} {book.pages:<6} {book.readStatus:<7} {review:<7} {notes}")
    print()


def line():
    print("-" * 85)
    
def main_header():
    print("\t\t\t\tMY LIBRARY")
    
def main_menu():
    print("MENU OPTIONS")
    print("1 – Display Library")
    print("2 – Add a Book")
    print("3 – Remove a Book")
    print("4 - Update a Book (Status, Review, Notes)")
    print("5 – Edit Book Notes")
    print("6 - Show Menu")
    print("7 - Exit Library")
    print()

def main():
    main_header()
    main_menu()
    line()

    db.connect()

    library = Library()
    books = db.get_books()  
    if books:
        for book in books:
            library.add(book)  
            
    while True:
        try:
            option = int(input("Menu option (6 to show main menu): "))
        except ValueError:
            option = -1
            
        if option == 1:
            display_library(library)
        elif option == 2:
            add_book(library)
        elif option == 3:
            remove_book(library)
        elif option == 4:
            update_book(library)
        elif option == 5:
            get_notes(library, is_menu_option_5=True)
        elif option == 6:
            main_menu()
        elif option == 7:
            print("Happy reading! Bye for now.")
            break
        else:
            print("Please enter a valid option.\n")
            main_menu()

if __name__ == "__main__":
    main()
    
  
