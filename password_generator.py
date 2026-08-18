import argparse
import secrets
import string
import sys
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

    # Guarantee at least 1 character from each chosen category
    password_chars = [secrets.choice(pool) for pool in categories]

    # Fill the remaining length
    all_allowed = "".join(categories)
    remaining_length = length - len(password_chars)
    password_chars.extend(secrets.choice(all_allowed) for _ in range(remaining_length))

    # Secure shuffle
    secure_random = secrets.SystemRandom()
    secure_random.shuffle(password_chars)

    return "".join(password_chars)

def run_interactive_mode():
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
            pwd = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
            strength = evaluate_strength(pwd)
            pyperclip.copy(pwd)

            print("\n" + "=" * 48)
            print(f"Generated Password : {pwd}")
            print(f"Password Strength  : {strength}")
            print("✓ Copied to clipboard automatically!")
            print("=" * 48)
        except ValueError as e:
            print(f"\nConfiguration Error: {e}")

        repeat = input("\nGenerate another password? (y/n): ").strip().lower()
        if repeat != 'y':
            print("\nGoodbye!")
            break

def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="Generate secure, randomized passwords from the command line."
    )
    parser.add_argument("-l", "--length", type=int, default=16, help="Password length (default: 16)")
    parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters")
    parser.add_argument("--no-lower", action="store_true", help="Exclude lowercase letters")
    parser.add_argument("--no-digits", action="store_true", help="Exclude numeric digits")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude special punctuation characters")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of passwords to generate (default: 1)")

    return parser.parse_args()

def main():
    # If no flags/arguments were passed, launch interactive prompt mode
    if len(sys.argv) == 1:
        run_interactive_mode()
        return

    # Otherwise, parse CLI flags
    args = parse_cli_args()

    use_upper = not args.no_upper
    use_lower = not args.no_lower
    use_digits = not args.no_digits
    use_symbols = not args.no_symbols

    try:
        passwords = [
            generate_password(args.length, use_upper, use_lower, use_digits, use_symbols)
            for _ in range(args.count)
        ]

        # Copy the first (or only) generated password to the clipboard
        pyperclip.copy(passwords[0])

        print("=" * 48)
        for idx, pwd in enumerate(passwords, start=1):
            strength = evaluate_strength(pwd)
            label = f"Password {idx}" if args.count > 1 else "Password"
            print(f"{label:<12}: {pwd}  [{strength}]")
        print("✓ Copied to clipboard automatically!")
        print("=" * 48)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()