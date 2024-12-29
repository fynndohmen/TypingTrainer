import sqlite3
import os

# Pfad zur SQLite-Datenbank
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/database.db')


def get_connection():
    """
    Erstellt eine Verbindung zur SQLite-Datenbank.
    """
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """
    Stellt sicher, dass die Datenbank und die notwendigen Tabellen existieren.
    Wenn die Tabellen nicht existieren, werden sie erstellt.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Tabelle für Tippstatistiken
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            duration REAL NOT NULL,
            error_count INTEGER NOT NULL,
            total_chars INTEGER NOT NULL
        );
    """)

    conn.commit()
    conn.close()


def save_session_stats(duration, error_count, total_chars_typed):
    """
    Speichert die Statistiken einer abgeschlossenen Tipp-Session.

    Parameters:
    - duration: Dauer der Tippübung in Sekunden (float)
    - error_count: Anzahl der Tippfehler (int)
    - total_chars_typed: Anzahl der insgesamt getippten Zeichen (int)
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Aktueller Zeitstempel in UTC
    from datetime import datetime
    timestamp = datetime.utcnow().isoformat()

    cursor.execute("""
        INSERT INTO sessions (timestamp, duration, error_count, total_chars)
        VALUES (?, ?, ?, ?)
    """, (timestamp, duration, error_count, total_chars_typed))

    conn.commit()
    conn.close()


def get_all_sessions():
    """
    Optional: Gibt alle gespeicherten Tippstatistiken aus der Datenbank zurück.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sessions")
    rows = cursor.fetchall()

    conn.close()
    return rows
