'''
This file contains the code to interact with the SQLite database
for the Library Management Program. 

Written by: Mary Nelson
Date: 05/10/2024
'''

import sqlite3
from contextlib import closing

from business import Book, Library

conn = None

def connect():
    global conn
    if not conn:
        DB_FILE = "Final.sqlite"
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def create_book(row):
    return Book(row["title"], row["author"], row["pages"],
                row["readStatus"], row["review"],
                row["notes"],row["bookID"], row["serial"])

def get_books():
    query = '''SELECT serial, bookID, title, author, pages, readStatus, review, notes
                FROM Books
                ORDER BY bookID'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    books = []
    for row in results:
        book = create_book(row)
        books.append(book)
    return books

def get_book(bookID):
    query = '''SELECT serial, bookID, title, author, pages, readStatus, review, notes
                FROM Books
                WHERE bookID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (bookID,))
        row = c.fetchone()
        if row:
            book = create_book(row)
            return book  
        else:
            return None

def add_book(book):
    query = '''INSERT INTO Books
            (title, author, pages, readStatus, review, notes, bookID)
            VALUES
                (?,?,?,?,?,?,?)'''
    with closing(conn.cursor()) as c:
        # Set the review to an empty string if the book status is unread
        # otherwise pass review
        review = "" if book.readStatus == "unread" else book.review
        
        c.execute(query, (book.title, book.author, book.pages,
                          book.readStatus, review, book.notes, book.bookID))
        conn.commit()
        

def remove_book(bookID):
    query = '''DELETE FROM Books WHERE bookID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (bookID,))
        conn.commit()
            # After removing a book, renumber the remaining books sequentially.
            # Without this it was incorrectly renumbering books that
            # were added during current session.
    update_bookIDs()
            
def update_library(library):
    for num, book in enumerate(library, start=1):
        book.bookID = num
        query = '''UPDATE Books
                    SET bookID = ?
                    WHERE serial = ?'''
        with closing(conn.cursor()) as c:
            c.execute(query, (book.bookID, book.serial))
            conn.commit()

def update_book(book):
    query = '''UPDATE Books
              SET readStatus = ?, review = ?, notes = ?
              WHERE bookID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (book.readStatus, book.review, book.notes, book.bookID))
        conn.commit()

# Update all bookIDs sequentially after a removal
def update_bookIDs():
    query = '''SELECT serial FROM Books ORDER BY serial'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        serials = c.fetchall()

    for index, serial in enumerate(serials, start=1):
        query = '''UPDATE Books SET bookID = ? WHERE serial = ?'''
        with closing(conn.cursor()) as c:
            c.execute(query, (index, serial["serial"]))
            conn.commit()

def main():
    connect()
    books = get_books()
    for book in books:
        print(book.bookID, book.title, book.author, book.pages,
              book.readStatus, book.review, book.notes)

if __name__ == "__main__":
    main()  
