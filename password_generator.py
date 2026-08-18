import secrets
import string
import pyperclip

def evaluate_strength(pwd):
    score = 0
    if len(pwd) >= 16:
        score += 3
    elif len(pwd) >= 12:
        score += 2
    elif len(pwd) >= 8:
        score += 1

    if any(c.isupper() for c in pwd) and any(c.islower() for c in pwd):
        score += 1
    if any(c.isdigit() for c in pwd):
        score += 1
    if any(c in string.punctuation for c in pwd):
        score += 1

    if score >= 5:
        return "Strong"
    elif score >= 3:
        return "Medium"
    else:
        return "Weak"

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
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

    # Pick 1 guaranteed character from each category
    password_chars = [secrets.choice(pool) for pool in categories]

    # Fill the remainder randomly from the full active pool
    all_allowed = "".join(categories)
    remaining_length = length - len(password_chars)
    password_chars.extend(secrets.choice(all_allowed) for _ in range(remaining_length))

    # Cryptographically shuffle
    secure_random = secrets.SystemRandom()
    secure_random.shuffle(password_chars)

    return "".join(password_chars)

def main():
    print("=== Cryptographically Secure Password Generator ===")

    while True:
        try:
            length_input = input("\nEnter desired password length (e.g., 16): ").strip()
            length = int(length_input)
            if length <= 0:
                print("Error: Length must be a positive integer.")
                continue
        except ValueError:
            print("Error: Please enter a valid whole number.")
            continue

        use_upper = input("Include uppercase letters (A-Z)? (y/n): ").strip().lower() == 'y'
        use_lower = input("Include lowercase letters (a-z)? (y/n): ").strip().lower() == 'y'
        use_digits = input("Include numbers (0-9)? (y/n): ").strip().lower() == 'y'
        use_symbols = input("Include special characters (!@#$)? (y/n): ").strip().lower() == 'y'

        try:
            password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
            strength = evaluate_strength(password)

            # Copy to clipboard
            pyperclip.copy(password)

            print("\n" + "=" * 48)
            print(f"Generated Password : {password}")
            print(f"Password Strength  : {strength}")
            print("✓ Copied to clipboard automatically!")
            print("=" * 48)

        except ValueError as e:
            print(f"\nConfiguration Error: {e}")

        # Prompt to repeat or exit
        repeat = input("\nGenerate another password? (y/n): ").strip().lower()
        if repeat != 'y':
            print("\nThank you for using Password Generator. Goodbye!")
            break

if __name__ == "__main__":
    main()