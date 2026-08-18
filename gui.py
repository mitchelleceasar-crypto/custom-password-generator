import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip

# --- Core Logic ---

def evaluate_strength(pwd):
    if not pwd:
        return "Enter a password", 0, "#cccccc"

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
        return "Strong", 100, "#28a745"   # Green
    elif score >= 3:
        return "Medium", 60, "#ffc107"    # Yellow / Amber
    else:
        return "Weak", 25, "#dc3545"      # Red

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

    password_chars = [secrets.choice(pool) for pool in categories]
    all_allowed = "".join(categories)
    remaining = length - len(password_chars)
    password_chars.extend(secrets.choice(all_allowed) for _ in range(remaining))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)

# --- GUI Application ---

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Studio: Generator & Tester")
        self.root.geometry("480x620")
        self.root.resizable(False, False)

        # State variables
        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        self.setup_ui()
        self.on_generate()

    def setup_ui(self):
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)

        # 1. Custom / Manual Password Testing Area
        test_frame = ttk.LabelFrame(container, text="Type & Test Your Own Password (Live)", padding=10)
        test_frame.pack(fill="x", pady=(0, 12))

        self.custom_entry = ttk.Entry(test_frame, font=("Consolas", 11))
        self.custom_entry.pack(fill="x", pady=(0, 6))
        # Listen for keypress events to update strength instantly
        self.custom_entry.bind("<KeyRelease>", self.on_custom_type)

        # 2. Strength Indicator
        strength_frame = ttk.LabelFrame(container, text="Strength Indicator", padding=10)
        strength_frame.pack(fill="x", pady=(0, 12))

        self.strength_label = ttk.Label(strength_frame, text="Strength: Evaluating...", font=("Segoe UI", 9, "bold"))
        self.strength_label.pack(anchor="w", pady=(0, 5))

        self.bar_canvas = tk.Canvas(strength_frame, height=12, bg="#e0e0e0", highlightthickness=0)
        self.bar_canvas.pack(fill="x")

        # 3. Generator Output Box
        gen_frame = ttk.LabelFrame(container, text="Generated Password", padding=10)
        gen_frame.pack(fill="x", pady=(0, 12))

        self.pwd_entry = ttk.Entry(gen_frame, font=("Consolas", 12), justify="center")
        self.pwd_entry.pack(fill="x", pady=(0, 6))

        copy_btn = ttk.Button(gen_frame, text="📋 Copy Generated Password", command=self.on_copy)
        copy_btn.pack()

        # 4. Generator Controls
        settings_frame = ttk.LabelFrame(container, text="Generator Settings", padding=10)
        settings_frame.pack(fill="x", pady=(0, 12))

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
        self.slider.pack(fill="x", pady=(2, 6))

        ttk.Checkbutton(settings_frame, text="Include Uppercase (A-Z)", variable=self.upper_var).pack(anchor="w", pady=1)
        ttk.Checkbutton(settings_frame, text="Include Lowercase (a-z)", variable=self.lower_var).pack(anchor="w", pady=1)
        ttk.Checkbutton(settings_frame, text="Include Numbers (0-9)", variable=self.digits_var).pack(anchor="w", pady=1)
        ttk.Checkbutton(settings_frame, text="Include Special Characters (!@#$)", variable=self.symbols_var).pack(anchor="w", pady=1)

        # 5. Generate Button
        generate_btn = tk.Button(
            container,
            text="🎲 Generate Secure Password",
            font=("Segoe UI", 10, "bold"),
            bg="#007acc",
            fg="white",
            activebackground="#005999",
            activeforeground="white",
            relief="flat",
            pady=6,
            command=self.on_generate
        )
        generate_btn.pack(fill="x")

    def update_length_display(self, val):
        self.length_display.config(text=str(int(float(val))))

    def update_strength_bar(self, percentage, color):
        self.bar_canvas.delete("all")
        width = self.bar_canvas.winfo_width()
        if width <= 1:
            width = 420
        fill_width = (percentage / 100) * width
        self.bar_canvas.create_rectangle(0, 0, fill_width, 12, fill=color, outline="")

    def on_custom_type(self, event=None):
        """Evaluates custom password typed by user in real-time."""
        user_pwd = self.custom_entry.get()
        strength, pct, color = evaluate_strength(user_pwd)
        self.strength_label.config(text=f"Custom Password Strength: {strength}", foreground=color)
        self.update_strength_bar(pct, color)

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

            # Clear custom input so indicator focuses on generated output
            self.custom_entry.delete(0, tk.END)

            strength, pct, color = evaluate_strength(pwd)
            self.strength_label.config(text=f"Generated Strength: {strength}", foreground=color)
            self.root.update_idletasks()
            self.update_strength_bar(pct, color)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def on_copy(self):
        pwd = self.pwd_entry.get()
        if pwd:
            pyperclip.copy(pwd)
            messagebox.showinfo("Copied", "Generated password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()