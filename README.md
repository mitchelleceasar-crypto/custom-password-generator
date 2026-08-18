#  Password Studio: Secure Generator & Live Tester

A cryptographically secure password generator, evaluator, and testing suite built in Python. Includes both an interactive Command-Line Interface (CLI) and a desktop Graphical User Interface (GUI).

---

##  Features

- **Cryptographically Secure:** Uses Python's built-in `secrets` module instead of pseudo-random generators for unpredictable output.
- **Guaranteed Variety:** Enforces inclusion of at least one character from every active character group (uppercase, lowercase, digits, symbols).
- **Live Password Strength Tester:** Real-time visual scoring meter (Weak / Medium / Strong) with dynamic color feedback.
- **Automatic Clipboard Integration:** Copies generated passwords directly to your clipboard using `pyperclip`.
- **Dual Interface Modes:**
  - **Desktop GUI:** Built with native `tkinter` featuring length sliders, real-time strength bars, and live custom input testing.
  - **CLI / Script Mode:** Supports interactive prompts and direct command-line automation flags via `argparse`.

---

##  Installation & Setup

### Prerequisites
- Python 3.8+ installed on your system.

### Install Dependencies
Clone this repository and install the required packages:

```bash
git clone [https://github.com/Mitchelle/mitchelleceasar-crypto.git](https://github.com/Mitchelle/mitchelleceasar-crypto.git)
cd mitchelleceasar-crypto
pip install -r requirements.txt