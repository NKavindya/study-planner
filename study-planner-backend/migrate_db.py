"""
Database Migration Script
Run this script to update the database schema
"""
from app.models.database import migrate_subjects_table, init_db

if __name__ == "__main__":
    print("Running database migration...")
    init_db()
    migrate_subjects_table()
    print("Migration completed!")

