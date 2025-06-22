#!/usr/bin/env python3
"""
Script to generate a secure Django secret key.
Run this script to generate a new secret key for your Django application.
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure secret key for Django"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Remove characters that might cause issues in environment variables
    alphabet = alphabet.replace('"', '').replace("'", '').replace('\\', '')
    
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated Django Secret Key:")
    print(f"DJANGO_SECRET_KEY={secret_key}")
    print("\nAdd this to your .env file or environment variables.")
    print("Make sure to keep this key secret and never commit it to version control!") 