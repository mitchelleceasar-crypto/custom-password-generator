import secrets
import string
import pyperclip

def evaluate_strength(pwd):
    score = 0
    
    # Length scoring
    if len(pwd) >= 16:
        score += 3
    elif len(pwd) >= 12:
        score += 2
    elif len(pwd) >= 8:
        score += 1

    # Character variety checks
    if any(c.isupper() for c in pwd) and any(c.islower() for c in pwd):
        score += 1
    if any(c.isdigit() for c in pwd):
        score += 1
    if any(c in string.punctuation for c in pwd):
        score += 1

    # Rating determination
    if score >= 5:
        return "Strong"
    elif score >= 3:
        return "Medium"
    else:
        return "Weak"

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    # Map choices to their respective character sets
    categories = []
    if use_upper:
        categories.append(string.ascii_uppercase)
    if use_lower:
        categories.append(string.ascii_lowercase)
    if use_digits:
        categories.append(string.digits)
    if use_symbols:
        categories.append(string.punctuation)

    if not categories:
        raise ValueError("At least one character type must be selected.")

    if length < len(categories):
        raise ValueError(
            f"Length ({length}) is too short to guarantee at least one character "
            f"from each of the {len(categories)} selected categories."
        )

    # Step 1: Guarantee at least 1 character from each selected category
    password_chars = [secrets.choice(pool) for pool in categories]

    # Step 2: Fill the rest of the length from the full combined pool
    all_allowed = "".join(categories)
    remaining_length = length - len(password_chars)
    password_chars.extend(secrets.choice(all_allowed) for _ in range(remaining_length))

    # Step 3: Cryptographically shuffle the characters to randomize order
    secure_random = secrets.SystemRandom()
    secure_random.shuffle(password_chars)

    return "".join(password_chars)

def main():
    print("=== Cryptographically Secure Password Generator ===")

    try:
        length = int(input("Enter desired password length (minimum 4 recommended): "))
        if length <= 0:
            print("Error: Length must be a positive integer.")
            return
    except ValueError:
        print("Error: Please enter a valid whole number.")
        return

    use_upper = input("Include uppercase letters (A-Z)? (y/n): ").strip().lower() == 'y'
    use_lower = input("Include lowercase letters (a-z)? (y/n): ").strip().lower() == 'y'
    use_digits = input("Include numbers (0-9)? (y/n): ").strip().lower() == 'y'
    use_symbols = input("Include special characters (!@#$)? (y/n): ").strip().lower() == 'y'

    try:
        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        strength = evaluate_strength(password)

        print("\n" + "=" * 48)
        print(f"Generated Password : {password}")
        print(f"Password Strength  : {strength}")
        print("=" * 48)
        pyperclip.copy(password)
        print("Password copied to clipboard.")
    except ValueError as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()