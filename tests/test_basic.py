"""
Basic unit tests for the Library Management System.

Each test runs against a fresh, temporary SQLite database file so that
tests never touch the real library.db used by the application.
"""

import os
import sys
import tempfile
import unittest

# Allow running these tests directly with "python -m unittest" from the
# project root, by making sure the project root is on the import path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database.db as db
from models.book import Book
from models.member import Member
from models.loan import Loan


class LibraryTestCase(unittest.TestCase):
    def setUp(self):
        # Point the database module at a fresh temporary file for this test.
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_file.close()
        db.DB_NAME = self.temp_file.name
        db.initialize_database()

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_add_book(self):
        book_id = Book.add("Clean Code", "Robert C. Martin", 2008, "9780132350884")
        book = Book.get_by_id(book_id)

        self.assertIsNotNone(book)
        self.assertEqual(book[1], "Clean Code")
        self.assertEqual(book[5], 1)  # is_available should default to True

    def test_add_member(self):
        member_id = Member.add("Aminata", "Ba", "aminata.ba@example.com")
        member = Member.get_by_id(member_id)

        self.assertIsNotNone(member)
        self.assertEqual(member[1], "Aminata")
        self.assertEqual(member[3], "aminata.ba@example.com")

    def test_borrow_book(self):
        book_id = Book.add("The Pragmatic Programmer", "Andrew Hunt", 1999, "9780135957059")
        member_id = Member.add("John", "Doe", "john.doe@example.com")

        loan_id = Loan.borrow_book(book_id, member_id)
        self.assertIsNotNone(loan_id)

        book = Book.get_by_id(book_id)
        self.assertEqual(book[5], 0)  # book should now be unavailable

        active_loans = Loan.get_active_loans()
        self.assertEqual(len(active_loans), 1)

    def test_cannot_borrow_unavailable_book(self):
        book_id = Book.add("Refactoring", "Martin Fowler", 1999, "9780201485677")
        member_id = Member.add("Jane", "Smith", "jane.smith@example.com")

        first_loan_id = Loan.borrow_book(book_id, member_id)
        second_loan_id = Loan.borrow_book(book_id, member_id)

        self.assertIsNotNone(first_loan_id)
        self.assertIsNone(second_loan_id)

    def test_return_book(self):
        book_id = Book.add("Design Patterns", "Erich Gamma", 1994, "9780201633610")
        member_id = Member.add("Mary", "Jones", "mary.jones@example.com")

        loan_id = Loan.borrow_book(book_id, member_id)
        returned = Loan.return_book(loan_id)

        self.assertTrue(returned)

        book = Book.get_by_id(book_id)
        self.assertEqual(book[5], 1)  # book should be available again

        active_loans = Loan.get_active_loans()
        self.assertEqual(len(active_loans), 0)

        history = Loan.get_history()
        self.assertEqual(len(history), 1)


if __name__ == "__main__":
    unittest.main()
