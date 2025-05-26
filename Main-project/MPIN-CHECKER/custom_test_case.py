from evaluator import evaluate_pin

def is_valid_mpin(pin, length):
    return pin.isdigit() and len(pin) == length

def is_valid_date(date_str):
    if len(date_str) != 10:
        return False
    parts = date_str.split("-")
    return len(parts) == 3 and all(part.isdigit() for part in parts)

def get_valid_input(prompt, length=None, is_date=False):
    while True:
        value = input(prompt).strip()
        if is_date:
            if is_valid_date(value):
                return value
            else:
                print("❌ Please enter a valid date in YYYY-MM-DD format.")
        elif length:
            if is_valid_mpin(value, length):
                return value
            else:
                print(f"❌ MPIN must be exactly {length} digits.")
        else:
            return value

def part_a(pin):
    print("\n=== Part A: Check if MPIN is commonly used (without demographics) ===")
    result = evaluate_pin(pin)
    if "COMMONLY_USED" in result["reasons"]:
        print(f"Entered MPIN: {pin}")
        print("Output: MPIN is COMMONLY USED ❌")
    else:
        print(f"Entered MPIN: {pin}")
        print("Output: MPIN is NOT commonly used ✅")

def part_b(pin, demographics):
    print("\n=== Part B: Evaluate MPIN Strength based on demographics ===")
    result = evaluate_pin(pin, demographics)
    print(f"Entered MPIN: {pin}")
    print("Output: Strength =", result["strength"])

def part_c(pin, demographics):
    print("\n=== Part C: Full Evaluation with Reasons for Weak MPIN ===")
    result = evaluate_pin(pin, demographics)
    print(f"Entered MPIN: {pin}")
    print("Output: Strength =", result["strength"])
    if result["strength"] == "WEAK":
        print("Reasons:", result["reasons"])
    else:
        print("Reasons: None ✅")

def part_d(pin_6_digit, demographics):
    print("\n=== Part D: Same as C but with a 6-digit MPIN ===")
    result = evaluate_pin(pin_6_digit, demographics)
    print(f"Entered MPIN: {pin_6_digit}")
    print("Output: Strength =", result["strength"])
    if result["strength"] == "WEAK":
        print("Reasons:", result["reasons"])
    else:
        print("Reasons: None ✅")

def main():
    print("🔐 MPIN Evaluation (All Parts A to D)\n")

    print("📌 NOTE: Your MPIN will be evaluated for potential weakness based on demographic date combinations.")
    print("⚠️ Avoid using combinations derived from your DOB, spouse's DOB, or anniversary.")
    print("We check for these patterns:")
    print("- 4-digit patterns: DDMM, MMDD, YYMM, MMYY, YYDD, DDYY, YYYY (full year)")
    print("- 6-digit patterns: DDMMYY, MMDDYY, YYMMDD, YYDDMM, YYYYMM, YYYYDD, MMYYYY, DDYYYY")
    print("- Single components like: 2004, 2018 (full year), 02 (day), 10 (month), 04 (short year), etc.\n")

    # Input for 4-digit MPIN
    pin_4 = get_valid_input("Enter your 4-digit MPIN: ", length=4)

    # Input for demographics
    dob = get_valid_input("Enter your Date of Birth (YYYY-MM-DD): ", is_date=True)
    dob_spouse = get_valid_input("Enter your Spouse's DOB (YYYY-MM-DD): ", is_date=True)
    anniversary = get_valid_input("Enter your Anniversary Date (YYYY-MM-DD): ", is_date=True)

    demographics = {
        "dob": dob,
        "dob_spouse": dob_spouse,
        "anniversary": anniversary
    }

    # Input for 6-digit MPIN
    pin_6 = get_valid_input("\nEnter your 6-digit MPIN: ", length=6)

    # Run all parts
    part_a(pin_4)
    part_b(pin_4, demographics)
    part_c(pin_4, demographics)
    part_d(pin_6, demographics)

if __name__ == "__main__":
    main()
