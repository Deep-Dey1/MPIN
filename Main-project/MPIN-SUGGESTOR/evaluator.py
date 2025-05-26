import os
from itertools import permutations

# Load common PINs (this runs once)
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

def get_date_variants(date_str):
    parts = date_str.split('-')
    if len(parts) != 3:
        return set()

    year, month, day = parts
    year_short = year[-2:]

    components_all = [day, month, year_short, year]  # includes full year

    variants = set()

    # Include standalone components of valid lengths
    for comp in components_all:
        if len(comp) in [4, 6]:
            variants.add(comp)

    # --- 4-digit combinations (2 parts) ---
    for combo in permutations(components_all, 2):
        candidate = ''.join(combo)
        if len(candidate) == 4:
            variants.add(candidate)

    # --- 6-digit combinations (2 parts and 3 parts) ---
    for combo in permutations(components_all, 2):
        candidate = ''.join(combo)
        if len(candidate) == 6:
            variants.add(candidate)

    for combo in permutations(components_all, 3):
        candidate = ''.join(combo)
        if len(candidate) == 6:
            variants.add(candidate)

    return variants

def evaluate_pin(pin, demographics={}):
    reasons = []

    # Part A: Check for commonly used
    if pin in COMMON_PINS:
        reasons.append("COMMONLY_USED")

    # Part B & C: Check against demographics
    demo_fields = [
        ("dob", "DEMOGRAPHIC_DOB_SELF"),
        ("dob_spouse", "DEMOGRAPHIC_DOB_SPOUSE"),
        ("anniversary", "DEMOGRAPHIC_ANNIVERSARY")
    ]

    for field, reason_code in demo_fields:
        if field in demographics:
            variants = get_date_variants(demographics[field])
            if pin in variants:
                reasons.append(reason_code)

    strength = "WEAK" if reasons else "STRONG"

    return {
        "strength": strength,
        "reasons": reasons
    }
