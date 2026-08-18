import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip

# --- Core Logic ---

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

    # Return (label, progress_percentage, hex_color)
    if score >= 5:
        return "Strong", 100, "#28a745"   # Green
    elif score >= 3:
        return "Medium", 60, "#ffc107"   # Yellow / Amber
    else:
        return "Weak", 25, "#dc3545"     # Red

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
        raise ValueError("Select at least one character type.")

    if length < len(categories):
        raise ValueError(f"Length ({length}) is too short for the {len(categories)} selected sets.")

    # Guaranteed pick from each enabled group
    password_chars = [secrets.choice(pool) for pool in categories]

    # Fill remaining slots
    all_allowed = "".join(categories)
    remaining = length - len(password_chars)
    password_chars.extend(secrets.choice(all_allowed) for _ in range(remaining))

    # Secure shuffle
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)

# --- GUI Application Class ---

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("460x520")
        self.root.resizable(False, False)

        # State variables
        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        self.setup_ui()
        self.on_generate()  # Generate initial password on startup

    def setup_ui(self):
        # Main container frame with padding
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        # Output Field Frame
        output_frame = ttk.LabelFrame(container, text="Generated Password", padding=10)
        output_frame.pack(fill="x", pady=(0, 15))

        self.pwd_entry = ttk.Entry(output_frame, font=("Consolas", 13), justify="center")
        self.pwd_entry.pack(fill="x", pady=(0, 8))

        copy_btn = ttk.Button(output_frame, text="📋 Copy to Clipboard", command=self.on_copy)
        copy_btn.pack()

        # Strength Meter Frame
        strength_frame = ttk.LabelFrame(container, text="Strength Indicator", padding=10)
        strength_frame.pack(fill="x", pady=(0, 15))

        self.strength_label = ttk.Label(strength_frame, text="Strength: Evaluating...", font=("Segoe UI", 9, "bold"))
        self.strength_label.pack(anchor="w", pady=(0, 5))

        # Canvas used as a custom colored progress bar
        self.bar_canvas = tk.Canvas(strength_frame, height=12, bg="#e0e0e0", highlightthickness=0)
        self.bar_canvas.pack(fill="x")

        # Configuration Settings Frame
        settings_frame = ttk.LabelFrame(container, text="Preferences", padding=10)
        settings_frame.pack(fill="x", pady=(0, 15))

        # Length Slider
        slider_header = ttk.Frame(settings_frame)
        slider_header.pack(fill="x")
        ttk.Label(slider_header, text="Length:").pack(side="left")
        self.length_display = ttk.Label(slider_header, text="16", font=("Segoe UI", 9, "bold"))
        self.length_display.pack(side="right")

        self.slider = ttk.Scale(
            settings_frame,
            from_=6,
            to=64,
            variable=self.length_var,
            orient="horizontal",
            command=self.update_length_display
        )
        self.slider.pack(fill="x", pady=(4, 10))

        # Character Set Checkboxes
        ttk.Checkbutton(settings_frame, text="Include Uppercase Letters (A-Z)", variable=self.upper_var).pack(anchor="w", pady=2)
        ttk.Checkbutton(settings_frame, text="Include Lowercase Letters (a-z)", variable=self.lower_var).pack(anchor="w", pady=2)
        ttk.Checkbutton(settings_frame, text="Include Numbers (0-9)", variable=self.digits_var).pack(anchor="w", pady=2)
        ttk.Checkbutton(settings_frame, text="Include Special Characters (!@#$)", variable=self.symbols_var).pack(anchor="w", pady=2)

        # Generate Action Button
        generate_btn = tk.Button(
            container,
            text="Generate New Password",
            font=("Segoe UI", 10, "bold"),
            bg="#007acc",
            fg="white",
            activebackground="#005999",
            activeforeground="white",
            relief="flat",
            pady=8,
            command=self.on_generate
        )
        generate_btn.pack(fill="x")

    def update_length_display(self, val):
        self.length_display.config(text=str(int(float(val))))

    def update_strength_bar(self, percentage, color):
        self.bar_canvas.delete("all")
        width = self.bar_canvas.winfo_width()
        if width <= 1:
            width = 400  # Fallback for initial render before geometry stabilizes
        fill_width = (percentage / 100) * width
        self.bar_canvas.create_rectangle(0, 0, fill_width, 12, fill=color, outline="")

    def on_generate(self):
        try:
            pwd = generate_password(
                length=self.length_var.get(),
                use_upper=self.upper_var.get(),
                use_lower=self.lower_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get()
            )
            self.pwd_entry.delete(0, tk.END)
            self.pwd_entry.insert(0, pwd)

            strength, pct, color = evaluate_strength(pwd)
            self.strength_label.config(text=f"Strength: {strength}", foreground=color)
            self.root.update_idletasks()
            self.update_strength_bar(pct, color)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def on_copy(self):
        pwd = self.pwd_entry.get()
        if pwd:
            pyperclip.copy(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()