import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "warehouse.db"


def setup() -> None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS enterprise_users (
                user_id INTEGER PRIMARY KEY,
                email TEXT,
                status TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS spending_logs (
                log_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount REAL,
                transaction_date TEXT
            )
            """
        )
        connection.executemany(
            "INSERT OR IGNORE INTO enterprise_users VALUES (?, ?, ?)",
            [
                (1, "alice@test.com", "completed"),
                (2, "bob@internal.com", "internal"),
            ],
        )
        connection.executemany(
            "INSERT OR IGNORE INTO spending_logs VALUES (?, ?, ?, ?)",
            [
                (100, 1, 500.0, "2026-10-01"),
                (101, 2, 9000.0, "2026-10-02"),
            ],
        )


if __name__ == "__main__":
    setup()
    print("Warehouse initialized successfully.")
