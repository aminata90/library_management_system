"""Member model: handles all CRUD database operations for library members."""

from database.db import get_connection


class Member:
    """Represents a single library member and provides CRUD operations."""

    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @staticmethod
    def add(first_name, last_name, email):
        """Insert a new member into the database."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO members (first_name, last_name, email)
            VALUES (?, ?, ?)
            """,
            (first_name, last_name, email),
        )
        connection.commit()
        new_id = cursor.lastrowid
        connection.close()
        return new_id

    @staticmethod
    def get_all():
        """Return a list of all members."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM members ORDER BY id")
        rows = cursor.fetchall()
        connection.close()
        return rows

    @staticmethod
    def get_by_id(member_id):
        """Return a single member by id, or None if not found."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        row = cursor.fetchone()
        connection.close()
        return row

    @staticmethod
    def update(member_id, first_name, last_name, email):
        """Update an existing member's details."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE members
            SET first_name = ?, last_name = ?, email = ?
            WHERE id = ?
            """,
            (first_name, last_name, email, member_id),
        )
        connection.commit()
        rows_changed = cursor.rowcount
        connection.close()
        return rows_changed > 0

    @staticmethod
    def delete(member_id):
        """Delete a member by id."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        connection.commit()
        rows_changed = cursor.rowcount
        connection.close()
        return rows_changed > 0
