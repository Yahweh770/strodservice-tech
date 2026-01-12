#!/usr/bin/env python3
"""
Script to initialize default users in the database.
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the app directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import DATABASE_URL, Base
from app import crud_user, schemas
from app.auth import get_password_hash

def init_users():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Get admin credentials from environment or use defaults
        admin_username = os.getenv("ADMIN_USERNAME", "Yahweh")
        admin_password = os.getenv("ADMIN_PASSWORD", "90vopepi")
        
        # Check if admin user already exists
        existing_admin = crud_user.get_user_by_username(db, admin_username)
        if existing_admin:
            print(f"Admin user '{admin_username}' already exists.")
            return
        
        # Create admin user
        admin_user = schemas.UserCreate(
            username=admin_username,
            email="admin@strod-service.ru",
            full_name="System Administrator",
            position="Administrator",
            department="IT",
            password=admin_password,
            is_active=True,
            is_admin=True,
            permissions={"admin": True, "manage_users": True, "manage_documents": True, "manage_materials": True}
        )
        
        created_admin = crud_user.create_user(db, admin_user)
        print(f"Successfully created admin user: {created_admin.username}")
        
    except Exception as e:
        print(f"Error initializing users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_users()