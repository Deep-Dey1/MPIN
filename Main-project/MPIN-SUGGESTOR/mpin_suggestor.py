import random
import os
from evaluator import evaluate_pin, get_date_variants, load_common_pins

COMMON_PINS = load_common_pins()
USED_MPINS_FILE = "used_mpins.txt"

def load_used_mpins():
    if not os.path.exists(USED_MPINS_FILE):
        return set()
    with open(USED_MPINS_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip().isdigit())

def save_mpin(mpin):
    with open(USED_MPINS_FILE, "a") as f:
        f.write(mpin + "\n")

def generate_random_mpin(length=4):
    return ''.join(random.choices('0123456789', k=length))

def is_secure_mpin(mpin, demographics, used_mpins):
    if mpin in COMMON_PINS or mpin in used_mpins:
        return False

    for field in demographics.values():
        variants = get_date_variants(field)
        if mpin in variants:
            return False

    return True

def suggest_secure_mpin(demographics, length=4):
    used_mpins = load_used_mpins()
    attempts = 0
    while attempts < 10000:
        mpin = generate_random_mpin(length)
        if is_secure_mpin(mpin, demographics, used_mpins):
            return mpin
        attempts += 1
    return None

def get_valid_date(prompt):
    while True:
        date_str = input(prompt).strip()
        if len(date_str) == 10 and all(part.isdigit() for part in date_str.split("-")):
            return date_str
        print("Please enter a valid date in YYYY-MM-DD format.")

def main():
    print("Secure MPIN Suggestor")

    # Collect user demographics
    dob = get_valid_date("Enter your Date of Birth (YYYY-MM-DD): ")
    dob_spouse = get_valid_date("Enter your Spouse's DOB (YYYY-MM-DD): ")
    anniversary = get_valid_date("Enter your Anniversary Date (YYYY-MM-DD): ")
    demographics = {
        "dob": dob,
        "dob_spouse": dob_spouse,
        "anniversary": anniversary
    }

    while True:
        mpin = suggest_secure_mpin(demographics)
        if mpin:
            print(f"\n Suggested Secure MPIN: {mpin}")
            choice = input("Do you want to accept this MPIN? (yes/no): ").strip().lower()
            if choice == 'yes':
                save_mpin(mpin)
                print("MPIN registered successfully and won't be reused.")
                break
        else:
            print("Couldn't find a secure MPIN. Please try again later.")
            break

if __name__ == "__main__":
    main()
