# backend/database.py

import sqlite3

DB_NAME = "disasterguard.db"


# ---------------- DATABASE CONNECTION ----------------


def get_connection():
    return sqlite3.connect(DB_NAME)


# ---------------- CREATE TABLES ----------------


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Reports Table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_id TEXT,
        name TEXT,
        location TEXT,
        disaster_type TEXT,
        severity TEXT,
        description TEXT,
        image_path TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """
    )

    # Volunteers Table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS volunteers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        skill TEXT NOT NULL
    )
    """
    )

    conn.commit()
    conn.close()


# ---------------- REPORT FUNCTIONS ----------------


def save_report(tracking_id, name, location, disaster_type, severity, description, image_path):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO reports (
        tracking_id,
        name,
        location,
        disaster_type,
        severity,
        description,
        image_path
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (tracking_id, name, location, disaster_type, severity, description, image_path),
    )

    conn.commit()
    conn.close()


def get_reports():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT *
    FROM reports
    ORDER BY id DESC
    """
    )

    data = cursor.fetchall()

    conn.close()

    return data


# ---------------- VOLUNTEER FUNCTIONS ----------------


def save_volunteer(name, phone, skill):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO volunteers (
        name,
        phone,
        skill
    )
    VALUES (?, ?, ?)
    """,
        (name, phone, skill),
    )

    conn.commit()
    conn.close()


def get_volunteers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT
        id,
        name,
        phone,
        skill
    FROM volunteers
    ORDER BY id DESC
    """
    )

    data = cursor.fetchall()

    conn.close()

    return data


# ---------------- REPORT STATUS ----------------


def update_report_status(report_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    UPDATE reports
    SET status = ?
    WHERE id = ?
    """,
        (status, report_id),
    )

    conn.commit()
    conn.close()


# ---------------- DASHBOARD COUNTS ----------------


def get_dashboard_counts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Pending'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Rescued'")
    rescued = cursor.fetchone()[0]

    conn.close()

    return total, pending, rescued


# ---------------- AUTO INIT ----------------

init_db()
