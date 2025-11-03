"""
Run this script to generate proper password hashes for the sample users
Then copy the hashes and update schema.sql
"""

from werkzeug.security import generate_password_hash

# Generate password hashes
student_password = generate_password_hash('student123')
moderator_password = generate_password_hash('admin123')

print("=== Copy these password hashes into schema.sql ===\n")
print(f"Student password hash (password: student123):")
print(f"{student_password}\n")
print(f"Moderator password hash (password: admin123):")
print(f"{moderator_password}\n")
print("Copy these and replace the dummy hashes in schema.sql INSERT statements")
