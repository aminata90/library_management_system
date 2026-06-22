"""Loan model: handles borrowing and returning books."""

from datetime import date

from database.db import get_connection
from models.book import Book


class Loan:
    """Represents a borrowing transaction between a member and a book."""

    def __init__(self, id, book_id, member_id, borrow_date, return_date):
        self.id = id
        self.book_id = book_id
        self.member_id = member_id
        self.borrow_date = borrow_date
        self.return_date = return_date

    @staticmethod
    def borrow_book(book_id, member_id):
        """Create a new loan for a book, if that book is currently available.

        Returns the new loan id on success, or None if the book
        could not be borrowed (e.g. it does not exist or is already
        borrowed).
        """
        book = Book.get_by_id(book_id)
        if book is None:
            return None

        is_available = book[5]
        if not is_available:
            return None

        connection = get_connection()
        cursor = connection.cursor()
        today = date.today().isoformat()
        cursor.execute(
            """
            INSERT INTO loans (book_id, member_id, borrow_date, return_date)
            VALUES (?, ?, ?, NULL)
            """,
            (book_id, member_id, today),
        )
        connection.commit()
        new_id = cursor.lastrowid
        connection.close()

        Book.set_availability(book_id, 0)
        return new_id

    @staticmethod
    def return_book(loan_id):
        """Mark a loan as returned and make the book available again."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT book_id, return_date FROM loans WHERE id = ?", (loan_id,))
        row = cursor.fetchone()

        if row is None or row[1] is not None:
            connection.close()
            return False

        book_id = row[0]
        today = date.today().isoformat()
        cursor.execute(
            "UPDATE loans SET return_date = ? WHERE id = ?",
            (today, loan_id),
        )
        connection.commit()
        connection.close()

        Book.set_availability(book_id, 1)
        return True

    @staticmethod
    def get_active_loans():
        """Return all loans that have not yet been returned."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM loans WHERE return_date IS NULL ORDER BY id"
        )
        rows = cursor.fetchall()
        connection.close()
        return rows

    @staticmethod
    def get_history():
        """Return all loans, returned and active, ordered by id."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM loans ORDER BY id")
        rows = cursor.fetchall()
        connection.close()
        return rows
