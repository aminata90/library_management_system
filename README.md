# Library Management System

A beginner-friendly command-line Library Management System built with
Python 3 and SQLite. It supports full CRUD management of books and
members, plus a borrowing/returning workflow for tracking loans.

## Features

- **Books**: add, view, update, and delete books.
- **Members**: add, view, update, and delete library members.
- **Loans**: borrow a book, return a book, view active loans, and view
  full loan history.
- Data is persisted in a local SQLite database file (`library.db`),
  which is created automatically the first time the app runs.
- Uses parameterized SQL queries to prevent SQL injection.
- Simple, readable, object-oriented code organized into models.

## Project Structure

```text
library_management_system/
│
├── database/
│   └── db.py            # Database connection + table creation
│
├── models/
│   ├── book.py           # Book CRUD operations
│   ├── member.py         # Member CRUD operations
│   └── loan.py           # Borrow/return logic
│
├── tests/
│   └── test_basic.py     # Unit tests
│
├── main.py                # CLI entry point
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.8 or newer
- No external packages are required (only the Python standard library
  is used: `sqlite3`, `unittest`, `datetime`).

## Installation

1. Clone or download this repository.
2. Navigate into the project folder:

   ```bash
   cd library_management_system
   ```

   (No `pip install` step is needed — see `requirements.txt`.)

## Running the Application

From inside the `library_management_system` folder, run:

```bash
python main.py
```

You will see a numbered menu in the terminal. Enter the number of the
action you want to perform and follow the prompts. The database file
`library.db` is created automatically in the project folder the first
time you run the app.

## Database Schema

**books**

| Column           | Type    | Notes                          |
|------------------|---------|---------------------------------|
| id               | INTEGER | Primary key, auto-increment     |
| title            | TEXT    | Required                        |
| author           | TEXT    | Required                        |
| publication_year | INTEGER |                                  |
| isbn             | TEXT    | Unique                          |
| is_available     | INTEGER | 1 = available, 0 = borrowed     |

**members**

| Column     | Type    | Notes                       |
|------------|---------|------------------------------|
| id         | INTEGER | Primary key, auto-increment |
| first_name | TEXT    | Required                    |
| last_name  | TEXT    | Required                    |
| email      | TEXT    | Required, unique            |

**loans**

| Column      | Type    | Notes                                 |
|-------------|---------|----------------------------------------|
| id          | INTEGER | Primary key, auto-increment            |
| book_id     | INTEGER | Foreign key → books.id                 |
| member_id   | INTEGER | Foreign key → members.id               |
| borrow_date | TEXT    | ISO date, set when the loan is created |
| return_date | TEXT    | ISO date, NULL while still on loan     |

## Example Usage

```text
===== LIBRARY MANAGEMENT SYSTEM =====
1.  Add a book
2.  View all books
...
Choose an option: 1
Title: Clean Code
Author: Robert C. Martin
Publication year: 2008
ISBN: 9780132350884
Book added successfully with id 1.

Choose an option: 5
First name: Aminata
Last name: Ba
Email: aminata.ba@example.com
Member added successfully with id 1.

Choose an option: 9
Book id to borrow: 1
Member id: 1
Book borrowed successfully. Loan id: 1
```

## Running the Tests

From inside the `library_management_system` folder, run:

```bash
python -m unittest tests.test_basic -v
```

The tests use temporary, isolated SQLite database files, so they will
never modify your real `library.db`. They cover:

- Adding a book
- Adding a member
- Borrowing a book (including the rule that an already-borrowed book
  cannot be borrowed again)
- Returning a book
