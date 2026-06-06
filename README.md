Corporate Password Generator & Validator
A simple, secure, and lightweight Python CLI tool designed to generate random, policy-compliant passwords and evaluate their strength instantly. It runs entirely in the terminal without requiring any databases or external dependencies.

Features
Enterprise Compliance: Generates passwords including lowercase, uppercase, numbers, and special characters (!@#$%^&*()-_=+).

Cryptographically Secure: Uses Python's native secrets module instead of random to ensure defense against predictability.

Strength Evaluator: Automatically audits the password and scores its complexity on a scale from 0 to 5.

Zero Dependencies: Runs out-of-the-box on any local machine or remote server (like Amazon EC2).

How to Use
1. Run the Script
Execute the script using Python 3 from your terminal:
python3 password_generator.py
2. Enter Password Length
The tool will prompt you for a length. Type a number (e.g., 16) and press Enter:
=== Secure Password / Key Generator ===
Enter desired password length (e.g., 16): 16
3. Get Your Output
The application will securely output your new password alongside its strength audit:
========================================
Generated Password : kX9!mP2v$Q_rA7wB
Password Strength  : 5/5
========================================
