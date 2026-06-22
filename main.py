"""
Library Management System
--------------------------
A simple command-line application for managing books, members,
and borrowing transactions, backed by an SQLite database.

Run with:
    python main.py
"""

from database.db import initialize_database
from models.book import Book
from models.member import Member
from models.loan import Loan


def print_menu():
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1.  Add a book")
    print("2.  View all books")
    print("3.  Update a book")
    print("4.  Delete a book")
    print("5.  Add a member")
    print("6.  View all members")
    print("7.  Update a member")
    print("8.  Delete a member")
    print("9.  Borrow a book")
    print("10. Return a book")
    print("11. View active loans")
    print("12. View loan history")
    print("0.  Exit")


def prompt_int(prompt_text):
    """Ask the user for an integer, looping until a valid one is given."""
    while True:
        value = input(prompt_text).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid whole number.")


# ---------- Book actions ----------

def add_book():
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    publication_year = prompt_int("Publication year: ")
    isbn = input("ISBN: ").strip()

    try:
        new_id = Book.add(title, author, publication_year, isbn)
        print(f"Book added successfully with id {new_id}.")
    except Exception as error:
        print(f"Could not add book: {error}")


def view_books():
    books = Book.get_all()
    if not books:
        print("No books found.")
        return

    print(f"\n{'ID':<4}{'Title':<25}{'Author':<20}{'Year':<6}{'ISBN':<16}{'Available'}")
    for book in books:
        book_id, title, author, year, isbn, is_available = book
        available_text = "Yes" if is_available else "No"
        print(f"{book_id:<4}{title:<25}{author:<20}{year:<6}{isbn:<16}{available_text}")


def update_book():
    book_id = prompt_int("Book id to update: ")
    book = Book.get_by_id(book_id)
    if book is None:
        print("Book not found.")
        return

    print("Leave a field blank to keep its current value.")
    title = input(f"Title [{book[1]}]: ").strip() or book[1]
    author = input(f"Author [{book[2]}]: ").strip() or book[2]
    year_input = input(f"Publication year [{book[3]}]: ").strip()
    publication_year = int(year_input) if year_input else book[3]
    isbn = input(f"ISBN [{book[4]}]: ").strip() or book[4]

    try:
        if Book.update(book_id, title, author, publication_year, isbn):
            print("Book updated successfully.")
        else:
            print("Book could not be updated.")
    except Exception as error:
        print(f"Could not update book: {error}")


def delete_book():
    book_id = prompt_int("Book id to delete: ")
    if Book.delete(book_id):
        print("Book deleted successfully.")
    else:
        print("Book not found.")


# ---------- Member actions ----------

def add_member():
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    email = input("Email: ").strip()

    try:
        new_id = Member.add(first_name, last_name, email)
        print(f"Member added successfully with id {new_id}.")
    except Exception as error:
        print(f"Could not add member: {error}")


def view_members():
    members = Member.get_all()
    if not members:
        print("No members found.")
        return

    print(f"\n{'ID':<4}{'First Name':<15}{'Last Name':<15}{'Email'}")
    for member in members:
        member_id, first_name, last_name, email = member
        print(f"{member_id:<4}{first_name:<15}{last_name:<15}{email}")


def update_member():
    member_id = prompt_int("Member id to update: ")
    member = Member.get_by_id(member_id)
    if member is None:
        print("Member not found.")
        return

    print("Leave a field blank to keep its current value.")
    first_name = input(f"First name [{member[1]}]: ").strip() or member[1]
    last_name = input(f"Last name [{member[2]}]: ").strip() or member[2]
    email = input(f"Email [{member[3]}]: ").strip() or member[3]

    try:
        if Member.update(member_id, first_name, last_name, email):
            print("Member updated successfully.")
        else:
            print("Member could not be updated.")
    except Exception as error:
        print(f"Could not update member: {error}")


def delete_member():
    member_id = prompt_int("Member id to delete: ")
    if Member.delete(member_id):
        print("Member deleted successfully.")
    else:
        print("Member not found.")


# ---------- Loan actions ----------

def borrow_book():
    book_id = prompt_int("Book id to borrow: ")
    member_id = prompt_int("Member id: ")

    loan_id = Loan.borrow_book(book_id, member_id)
    if loan_id is None:
        print("Could not borrow this book (it may not exist or is already borrowed).")
    else:
        print(f"Book borrowed successfully. Loan id: {loan_id}")


def return_book():
    loan_id = prompt_int("Loan id to return: ")
    if Loan.return_book(loan_id):
        print("Book returned successfully.")
    else:
        print("Could not return book (loan not found or already returned).")


def view_active_loans():
    loans = Loan.get_active_loans()
    if not loans:
        print("No active loans.")
        return

    print(f"\n{'Loan ID':<10}{'Book ID':<10}{'Member ID':<12}{'Borrow Date'}")
    for loan in loans:
        loan_id, book_id, member_id, borrow_date, return_date = loan
        print(f"{loan_id:<10}{book_id:<10}{member_id:<12}{borrow_date}")


def view_loan_history():
    loans = Loan.get_history()
    if not loans:
        print("No loan history found.")
        return

    print(f"\n{'Loan ID':<10}{'Book ID':<10}{'Member ID':<12}{'Borrow Date':<14}{'Return Date'}")
    for loan in loans:
        loan_id, book_id, member_id, borrow_date, return_date = loan
        return_text = return_date if return_date else "Not returned"
        print(f"{loan_id:<10}{book_id:<10}{member_id:<12}{borrow_date:<14}{return_text}")


def main():
    initialize_database()

    actions = {
        "1": add_book,
        "2": view_books,
        "3": update_book,
        "4": delete_book,
        "5": add_member,
        "6": view_members,
        "7": update_member,
        "8": delete_member,
        "9": borrow_book,
        "10": return_book,
        "11": view_active_loans,
        "12": view_loan_history,
    }

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid option, please try again.")
            continue

        action()


if __name__ == "__main__":
    main()
