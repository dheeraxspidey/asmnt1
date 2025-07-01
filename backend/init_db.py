#!/usr/bin/env python3
"""
Database initialization script
Run this to create tables and set up the database
"""

from models import create_tables
import sys

def init_database():
    """Initialize the database with required tables"""
    try:
        print("Creating database tables...")
        create_tables()
        print("Database tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating database tables: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
