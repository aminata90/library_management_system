"""Book model: handles all CRUD database operations for books."""

from database.db import get_connection


class Book:
    """Represents a single book and provides CRUD operations."""

    def __init__(self, id, title, author, publication_year, isbn, is_available=1):
        self.id = id
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.isbn = isbn
        self.is_available = is_available

    @staticmethod
    def add(title, author, publication_year, isbn):
        """Insert a new book into the database."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO books (title, author, publication_year, isbn)
            VALUES (?, ?, ?, ?)
            """,
            (title, author, publication_year, isbn),
        )
        connection.commit()
        new_id = cursor.lastrowid
        connection.close()
        return new_id

    @staticmethod
    def get_all():
        """Return a list of all books."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books ORDER BY id")
        rows = cursor.fetchall()
        connection.close()
        return rows

    @staticmethod
    def get_by_id(book_id):
        """Return a single book by its id, or None if not found."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        connection.close()
        return row

    @staticmethod
    def update(book_id, title, author, publication_year, isbn):
        """Update an existing book's details."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE books
            SET title = ?, author = ?, publication_year = ?, isbn = ?
            WHERE id = ?
            """,
            (title, author, publication_year, isbn, book_id),
        )
        connection.commit()
        rows_changed = cursor.rowcount
        connection.close()
        return rows_changed > 0

    @staticmethod
    def delete(book_id):
        """Delete a book by its id."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        connection.commit()
        rows_changed = cursor.rowcount
        connection.close()
        return rows_changed > 0

    @staticmethod
    def set_availability(book_id, is_available):
        """Mark a book as available (1) or borrowed (0)."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE books SET is_available = ? WHERE id = ?",
            (is_available, book_id),
        )
        connection.commit()
        connection.close()
