"""
Database connection and table setup for the Library Management System.

This module is responsible for:
- Creating a connection to the SQLite database file.
- Creating the required tables (books, members, loans) if they
  do not already exist.
"""

import sqlite3
import os

# The database file will be created in the project root folder.
DB_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(DB_FOLDER, "library.db")


def get_connection():
    """Create and return a new SQLite database connection.

    Foreign key support is off by default in SQLite, so we turn it on
    for every connection we create.
    """
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create all required tables if they do not already exist."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication_year INTEGER,
            isbn TEXT UNIQUE,
            is_available INTEGER NOT NULL DEFAULT 1
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            borrow_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (member_id) REFERENCES members (id)
        )
        """
    )

    connection.commit()
    connection.close()
