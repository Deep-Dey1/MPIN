import tkinter as tk
from tkinter import messagebox
import os
import random
import hashlib

# === Load common PINs from file ===
def load_common_pins(file_path='common_pins.txt'):
    common_pins = set()
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                pin = line.strip()
                if pin.isdigit():
                    common_pins.add(pin)
    return common_pins

COMMON_PINS = load_common_pins()
USED_MPINS_FILE = "used_mpin_hashes.txt"

def load_used_hashes():
    if not os.path.exists(USED_MPINS_FILE):
        return set()
    with open(USED_MPINS_FILE, 'r') as f:
        return set(line.strip() for line in f)

def hash_mpin(mpin):
    return hashlib.sha256(mpin.encode()).hexdigest()

def save_mpin_hash(mpin_hash):
    with open(USED_MPINS_FILE, "a") as f:
        f.write(mpin_hash + "\n")

def get_date_variants(date_str):
    parts = date_str.split('-')
    if len(parts) != 3:
        return set()

    year, month, day = parts
    year_short = year[-2:]   # e.g., "04"
    year_century = year[:2]  # e.g., "20"
    variants = set()

    # 4-digit patterns:
    variants.update({
        day + month,
        month + day,
        year_short + month,
        month + year_short,
        year_short + day,
        day + year_short,
        year,                 # full year (e.g., "2004")
        year_century + day,   # e.g., "2004" -> "20" + "04" = "2004"
        day + year_century,
        month + year_century,
        year_century + month,
    })

    # 6-digit patterns:
    variants.update({
        day + month + year_short,
        month + day + year_short,
        year_short + month + day,
        year_short + day + month,
        year + month,
        month + year,
        year + day,
        day + year,
        year_century + month + day,
        year_century + day + month,
        month + day + year_century,
        day + month + year_century,
        year_century + year_short + month,
        year_century + year_short + day
    })

    return variants

def evaluate_pin(pin, demographics={}):
    reasons = []

    # Check if pin is commonly used
    if pin in COMMON_PINS:
        reasons.append("COMMONLY_USED")

    # Check if pin matches any date variant from demographics
    demo_fields = [
        ("dob", "DEMOGRAPHIC_DOB_SELF"),
        ("dob_spouse", "DEMOGRAPHIC_DOB_SPOUSE"),
        ("anniversary", "DEMOGRAPHIC_ANNIVERSARY")
    ]
    for field, reason_code in demo_fields:
        if field in demographics and demographics[field]:
            variants = get_date_variants(demographics[field])
            if pin in variants:
                reasons.append(reason_code)

    strength = "WEAK" if reasons else "STRONG"

    return {
        "strength": strength,
        "reasons": reasons
    }

def generate_random_mpin(length=4):
    return ''.join(random.choices('0123456789', k=length))

def is_secure_mpin(mpin, demographics, used_hashes):
    # Check common pins
    if mpin in COMMON_PINS:
        return False

    # Check if mpin hash already used
    if hash_mpin(mpin) in used_hashes:
        return False

    # Check demographics date variants
    for field in demographics.values():
        if not field:
            continue
        variants = get_date_variants(field)
        if mpin in variants:
            return False
    return True

def suggest_secure_mpin(demographics, length=4):
    used_hashes = load_used_hashes()
    attempts = 0
    while attempts < 10000:
        mpin = generate_random_mpin(length)
        if is_secure_mpin(mpin, demographics, used_hashes):
            return mpin
        attempts += 1
    return None

# === Colors based on OneBanc golden and silver theme ===
GOLDEN = "#D4AF37"       # Golden color
SILVER = "#C0C0C0"       # Silver color
DARK_BG = "#1C1C1C"      # Dark background for contrast
LIGHT_BG = "#F5F5F5"     # Light background for main window
TEXT_COLOR = "#333333"   # Dark text
BUTTON_BG = GOLDEN
BUTTON_FG = "black"
ENTRY_BG = "white"
ENTRY_FG = "#222222"
HIGHLIGHT_COLOR = GOLDEN

class MPINApp:
    def __init__(self, master):
        self.master = master
        master.title("MPIN Tester and Suggestor")

        # Set window background color
        master.configure(bg=LIGHT_BG)

        # Use a consistent font for the app
        self.default_font = ("Segoe UI", 10)
        self.header_font = ("Segoe UI", 12, "bold")

        # Container frame with padding and bg
        self.container = tk.Frame(master, bg=LIGHT_BG, padx=15, pady=15)
        self.container.grid(row=0, column=0, sticky="nsew")

        # Mode selection: Tester or Suggestor
        tk.Label(self.container, text="Choose Mode:", bg=LIGHT_BG, fg=TEXT_COLOR, font=self.header_font).grid(row=0, column=0, sticky="w", pady=(0,5))
        self.mode_var = tk.StringVar(value="tester")
        tk.Radiobutton(self.container, text="MPIN Tester", variable=self.mode_var, value="tester", command=self.mode_changed, 
                       bg=LIGHT_BG, fg=TEXT_COLOR, font=self.default_font, activebackground=LIGHT_BG).grid(row=0, column=1, sticky="w")
        tk.Radiobutton(self.container, text="MPIN Suggestor", variable=self.mode_var, value="suggestor", command=self.mode_changed, 
                       bg=LIGHT_BG, fg=TEXT_COLOR, font=self.default_font, activebackground=LIGHT_BG).grid(row=0, column=2, sticky="w")

        # MPIN length selection
        tk.Label(self.container, text="Select MPIN Length:", bg=LIGHT_BG, fg=TEXT_COLOR, font=self.header_font).grid(row=1, column=0, sticky="w", pady=(10,5))
        self.length_var = tk.IntVar(value=4)
        tk.Radiobutton(self.container, text="4 digits", variable=self.length_var, value=4,
                       bg=LIGHT_BG, fg=TEXT_COLOR, font=self.default_font, activebackground=LIGHT_BG).grid(row=1, column=1, sticky="w")
        tk.Radiobutton(self.container, text="6 digits", variable=self.length_var, value=6,
                       bg=LIGHT_BG, fg=TEXT_COLOR, font=self.default_font, activebackground=LIGHT_BG).grid(row=1, column=2, sticky="w")

        # User Demographics input
        tk.Label(self.container, text="Your DOB (YYYY-MM-DD):", bg=LIGHT_BG, fg=TEXT_COLOR, font=self.default_font).grid(row=2, column=0, sticky="w", pady=(10,2))
        self.dob_entry = tk.Entry(self.container, bg=ENTRY_BG, fg=ENTRY_FG, font=self.default_font, relief="solid", highlightthickness=1, highlightcolor=GOLDEN)
        self.dob_entry.grid(row=2, column=1, columnspan=2, sticky="we", pady=2)

        tk.Label(self.container, text="Spouse DOB (YYYY-MM-DD):", bg=LIGHT_BG, fg=TEXT_COLOR, font=self.default_font).grid(row=3, column=0, sticky="w", pady=2)
        self.spouse_dob_entry = tk.Entry(self.container, bg=ENTRY_BG, fg=ENTRY_FG, font=self.default_font, relief="solid", highlightthickness=1, highlightcolor=GOLDEN)
        self.spouse_dob_entry.grid(row=3, column=1, columnspan=2, sticky="we", pady=2)

        tk.Label(self.container, text="Anniversary (YYYY-MM-DD):", bg=LIGHT_BG, fg=TEXT_COLOR, font=self.default_font).grid(row=4, column=0, sticky="w", pady=2)
        self.anniv_entry = tk.Entry(self.container, bg=ENTRY_BG, fg=ENTRY_FG, font=self.default_font, relief="solid", highlightthickness=1, highlightcolor=GOLDEN)
        self.anniv_entry.grid(row=4, column=1, columnspan=2, sticky="we", pady=2)

        # MPIN input for tester mode
        tk.Label(self.container, text="Enter MPIN to Test:", bg=LIGHT_BG, fg=TEXT_COLOR, font=self.default_font).grid(row=5, column=0, sticky="w", pady=(10,2))
        self.mpin_test_entry = tk.Entry(self.container, bg=ENTRY_BG, fg=ENTRY_FG, font=self.default_font, relief="solid", highlightthickness=1, highlightcolor=GOLDEN)
        self.mpin_test_entry.grid(row=5, column=1, columnspan=2, sticky="we", pady=2)

        # Buttons with golden bg and black text
        self.action_button = tk.Button(self.container, text="Evaluate MPIN", bg=BUTTON_BG, fg=BUTTON_FG,
                                       font=self.default_font, activebackground="#B8860B", relief="raised", padx=10, pady=5, command=self.evaluate_or_suggest)
        self.action_button.grid(row=6, column=0, columnspan=3, pady=(15, 5), sticky="we")

        self.accept_button = tk.Button(self.container, text="Accept MPIN", bg=BUTTON_BG, fg=BUTTON_FG,
                                       font=self.default_font, activebackground="#B8860B", relief="raised", padx=10, pady=5, command=self.accept_mpin)
        self.accept_button.grid(row=7, column=0, columnspan=3, pady=(5, 15), sticky="we")

        # Output text box with silver background and golden border
        self.output_text = tk.Text(self.container, height=8, width=50, bg=SILVER, fg=TEXT_COLOR, font=self.default_font,
                                   relief="solid", borderwidth=2, highlightthickness=2, highlightbackground=GOLDEN)
        self.output_text.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky="we")
        self.output_text.config(state=tk.DISABLED)

        # Configure grid weights for responsive design
        for i in range(3):
            self.container.columnconfigure(i, weight=1)

        self.current_mpin = None
        self.mode_changed()  # To set initial UI state

    def get_demographics(self):
        return {
            "dob": self.dob_entry.get().strip(),
            "dob_spouse": self.spouse_dob_entry.get().strip(),
            "anniversary": self.anniv_entry.get().strip(),
        }

    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

    def append_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.config(state=tk.DISABLED)

    def mode_changed(self):
        mode = self.mode_var.get()
        if mode == "tester":
            self.mpin_test_entry.config(state="normal")
            self.action_button.config(text="Evaluate MPIN")
        else:
            self.mpin_test_entry.delete(0, tk.END)
            self.mpin_test_entry.config(state="disabled")
            self.action_button.config(text="Suggest MPIN")
        self.clear_output()

    def evaluate_or_suggest(self):
        self.clear_output()
        mode = self.mode_var.get()
        length = self.length_var.get()
        demographics = self.get_demographics()

        # Validate demographic date format (YYYY-MM-DD) or empty
        for key, val in demographics.items():
            if val != "" and len(val) != 10:
                messagebox.showerror("Input Error", f"{key.replace('_', ' ').title()} must be in YYYY-MM-DD format or left empty.")
                return

        if mode == "tester":
            # Show important alert about demographic combinations
            messagebox.showinfo(
                "Important Notice",
                "📌 NOTE: Your MPIN will be evaluated for potential weakness based on demographic date combinations.\n\n"
                "⚠️ Avoid using combinations derived from your DOB, spouse's DOB, or anniversary.\n\n"
                "We check for these patterns:\n"
                "- 4-digit patterns: DDMM, MMDD, YYMM, MMYY, YYDD, DDYY, YYYY (full year)\n"
                "- 6-digit patterns: DDMMYY, MMDDYY, YYMMDD, YYDDMM, YYYYMM, YYYYDD, MMYYYY, DDYYYY\n"
                "- Single components like: 2004, 2018 (full year), 02 (day), 10 (month), 04 (short year), etc.\n"
            )

            pin = self.mpin_test_entry.get().strip()
            if not pin.isdigit() or len(pin) != length:
                messagebox.showerror("Input Error", f"MPIN must be exactly {length} digits.")
                return

            result = evaluate_pin(pin, demographics)
            self.current_mpin = pin

            self.append_output(f"MPIN: {pin}")
            self.append_output(f"Strength: {result['strength']}")
            if result['reasons']:
                self.append_output("Reasons:")
                for r in result['reasons']:
                    if r == "COMMONLY_USED":
                        self.append_output(" - MPIN is commonly used and easy to guess.")
                    elif r == "DEMOGRAPHIC_DOB_SELF":
                        self.append_output(" - MPIN matches your Date of Birth related pattern.")
                    elif r == "DEMOGRAPHIC_DOB_SPOUSE":
                        self.append_output(" - MPIN matches your Spouse's Date of Birth related pattern.")
                    elif r == "DEMOGRAPHIC_ANNIVERSARY":
                        self.append_output(" - MPIN matches your Anniversary date related pattern.")
                    else:
                        self.append_output(f" - {r}")
            else:
                self.append_output("No known vulnerabilities found.")
        else:
            # Suggestor mode
            mpin = suggest_secure_mpin(demographics, length)
            if mpin is None:
                self.append_output("Unable to generate a secure MPIN after multiple attempts.")
                self.current_mpin = None
            else:
                self.current_mpin = mpin
                self.append_output(f"Suggested Secure MPIN: {mpin}")

    def accept_mpin(self):
        if self.current_mpin is None:
            messagebox.showwarning("No MPIN", "No MPIN available to accept. Please evaluate or suggest one first.")
            return
        mpin_hash = hash_mpin(self.current_mpin)
        used_hashes = load_used_hashes()
        if mpin_hash in used_hashes:
            messagebox.showinfo("Duplicate MPIN", "This MPIN has already been accepted before.")
            return
        save_mpin_hash(mpin_hash)
        messagebox.showinfo("MPIN Accepted", f"MPIN '{self.current_mpin}' has been accepted and saved.")
        self.current_mpin = None
        self.clear_output()
        self.mpin_test_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MPINApp(root)
    root.mainloop()
