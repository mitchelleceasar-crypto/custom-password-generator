import random #handles picking random items
import string #gives you ready made collections of letters (string.ascii_letters) ,numbers(string.digits), and special characters(string.punctuation)

#collect user preferences
print("--- Custom Password Generator ---")

# Ask for password length
length = int(input("Enter password length (e.g., 12): "))

# Ask for optional character types (yes/no)
use_digits = input("Include numbers? (y/n): ").lower() == 'y'
use_symbols = input("Include special characters? (y/n): ").lower() == 'y'

#build the character pool based on user preferences
# Start with all uppercase and lowercase letters
characters = string.ascii_letters

# Add numbers if requested
if use_digits:
    characters += string.digits

# Add symbols if requested
if use_symbols:
    characters += string.punctuation

# Safety check: ensure at least one character set is available
if not characters:
    print("Error: No character types selected.")

#generate the random password
# Pick a random character from 'characters' 'length' times
password = "".join(random.choice(characters) for _ in range(length))

print(f"\nGenerated Password: {password}")

#create the strength meter function
def evaluate_strength(pwd):
    score = 0
    
    # Criterion 1: Length check
    if len(pwd) >= 12:
        score += 2
    elif len(pwd) >= 8:
        score += 1

    # Criterion 2: Contains both uppercase and lowercase letters
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    if has_upper and has_lower:
        score += 1

    # Criterion 3: Contains digits
    if any(c.isdigit() for c in pwd):
        score += 1

    # Criterion 4: Contains punctuation / special characters
    if any(c in string.punctuation for c in pwd):
        score += 1

    # Determine rating based on score
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