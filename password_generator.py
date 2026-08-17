import random
import string

def evaluate_strength(pwd):
    score = 0
    if len(pwd) >= 12:
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

def main():
    print("=== Custom Password Generator & Strength Checker ===")
    
    try:
        length = int(input("Enter desired password length: "))
        if length <= 0:
            print("Length must be greater than 0.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    use_digits = input("Include numbers? (y/n): ").strip().lower() == 'y'
    use_symbols = input("Include special characters? (y/n): ").strip().lower() == 'y'

    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    # Generate password
    password = "".join(random.choice(characters) for _ in range(length))
    strength = evaluate_strength(password)

    print("\n" + "=" * 40)
    print(f"Generated Password : {password}")
    print(f"Password Strength  : {strength}")
    print("=" * 40)

if __name__ == "__main__":
    main()
