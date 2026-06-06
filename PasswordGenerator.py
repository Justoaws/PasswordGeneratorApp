import secrets
import string

def generate_secure_password(length=16):
    if length < 8:
        print("Minimum recommended length is 8 characters.")
        length = 8
        
    # Define character pools
    letters_lower = string.ascii_lowercase
    letters_upper = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()-_=+"
    
    all_characters = letters_lower + letters_upper + digits + special_chars
    
    # Ensure at least one character from each pool to meet standard compliance
    password = [
        secrets.choice(letters_lower),
        secrets.choice(letters_upper),
        secrets.choice(digits),
        secrets.choice(special_chars)
    ]
    
    # Fill the rest of the password length randomly
    password += [secrets.choice(all_characters) for _ in range(length - 4)]
    
    # Shuffle securely (prevents predictable patterns at the beginning)
    secrets.SystemRandom().shuffle(password)
    
    return "".join(password)

def check_password_strength(pwd):
    score = 0
    if len(pwd) >= 12: score += 1
    if any(c in string.ascii_lowercase for c in pwd): score += 1
    if any(c in string.ascii_uppercase for c in pwd): score += 1
    if any(c in string.digits for c in pwd): score += 1
    if any(c in "!@#$%^&*()-_=+" for c in pwd): score += 1
    
    return f"{score}/5"

if __name__ == "__main__":
    print("=== Secure Password / Key Generator ===")
    try:
        size = int(input("Enter desired password length (e.g., 16): "))
    except ValueError:
        print("Invalid input. Defaulting length to 16.")
        size = 16
        
    generated_pwd = generate_secure_password(size)
    strength = check_password_strength(generated_pwd)
    
    print("\n" + "="*40)
    print(f"Generated Password : {generated_pwd}")
    print(f"Password Strength  : {strength}")
    print("="*40)
    