from evaluator import evaluate_pin

def run_tests():
    test_cases = [
        {
            "pin": "1234",
            "demographics": {},
            "expected_strength": "WEAK",
            "expected_reasons": ["COMMONLY_USED"]
        },
        {
            "pin": "1998",
            "demographics": {"dob": "1998-01-02"},
            "expected_strength": "WEAK",
            "expected_reasons": ["DEMOGRAPHIC_DOB_SELF"]
        },
        {
            "pin": "0201",
            "demographics": {"dob": "1998-01-02"},
            "expected_strength": "WEAK",
            "expected_reasons": ["DEMOGRAPHIC_DOB_SELF"]
        },
        {
            "pin": "9802",
            "demographics": {"dob": "1998-01-02"},
            "expected_strength": "WEAK",
            "expected_reasons": ["DEMOGRAPHIC_DOB_SELF"]
        },
        {
            "pin": "0202",
            "demographics": {"dob_spouse": "1997-02-02"},
            "expected_strength": "WEAK",
            "expected_reasons": ["DEMOGRAPHIC_DOB_SPOUSE"]
        },
        {
            "pin": "0708",
            "demographics": {"anniversary": "2018-08-07"},
            "expected_strength": "WEAK",
            "expected_reasons": ["DEMOGRAPHIC_ANNIVERSARY"]
        },
        {
            "pin": "9374",
            "demographics": {"dob": "1995-07-14"},
            "expected_strength": "STRONG",
            "expected_reasons": []
        },
        {
            "pin": "0000",
            "demographics": {"dob": "2000-01-01"},
            "expected_strength": "WEAK",
            "expected_reasons": ["COMMONLY_USED"]
        },
        {
            "pin": "123456",
            "demographics": {},
            "expected_strength": "WEAK",
            "expected_reasons": ["COMMONLY_USED"]
        },
        {
            "pin": "0101",
            "demographics": {},
            "expected_strength": "WEAK",
            "expected_reasons": ["COMMONLY_USED"]
        },
        {
            "pin": "741852",
            "demographics": {},
            "expected_strength": "WEAK",
            "expected_reasons": ["COMMONLY_USED"]
        },
        {
            "pin": "1412",
            "demographics": {"dob": "2012-12-14"},
            "expected_strength": "WEAK",
            "expected_reasons": ["DEMOGRAPHIC_DOB_SELF"]
        },
        {
            "pin": "7878",
            "demographics": {},
            "expected_strength": "STRONG",
            "expected_reasons": []
        },
        {
            "pin": "147258",
            "demographics": {},
            "expected_strength": "WEAK",
            "expected_reasons": ["COMMONLY_USED"]
        },
        {
            "pin": "0987",
            "demographics": {"dob_spouse": "1987-09-21"},
            "expected_strength": "WEAK",
            "expected_reasons": ["DEMOGRAPHIC_DOB_SPOUSE"]
        },
        {
            "pin": "0304",
            "demographics": {"anniversary": "2015-04-03"},
            "expected_strength": "WEAK",
            "expected_reasons": ["DEMOGRAPHIC_ANNIVERSARY"]
        },
        {
            "pin": "3141",
            "demographics": {},
            "expected_strength": "STRONG",
            "expected_reasons": []
        },
        {
            "pin": "9999",
            "demographics": {},
            "expected_strength": "WEAK",
            "expected_reasons": ["COMMONLY_USED"]
        },
        {
            "pin": "2020",
            "demographics": {},
            "expected_strength": "WEAK",
            "expected_reasons": ["COMMONLY_USED"]
        },
        {
            "pin": "8585",
            "demographics": {},
            "expected_strength": "STRONG",
            "expected_reasons": []
        }
    ]

    passed = 0

    for i, case in enumerate(test_cases, 1):
        result = evaluate_pin(case["pin"], case["demographics"])
        status = "✅ PASS" if result["strength"] == case["expected_strength"] and set(result["reasons"]) == set(case["expected_reasons"]) else "❌ FAIL"
        
        print(f"Test Case {i}: {status}")
        print(f"Input PIN: {case['pin']}")
        print(f"Demographics: {case['demographics']}")
        print(f"Expected: {case['expected_strength']} - {case['expected_reasons']}")
        print(f"Got: {result['strength']} - {result['reasons']}")
        print("-" * 40)

        if status.startswith("✅"):
            passed += 1

    print(f"\n✅ Total Passed: {passed}/{len(test_cases)}")

if __name__ == "__main__":
    run_tests()
