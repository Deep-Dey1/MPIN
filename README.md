# MPIN
This repository contains a basic project to find Weak MPINs by predicting the MPIN as guessable or commonly used one. To fix the Weak MPINS this project suggest the users more secure and unique MPINs for their use using GUI and web application.

# 🔐 MPIN Security Assessment

## 📘 Introduction: What is MPIN?

**MPIN (Mobile Personal Identification Number)** is a numeric password used for authentication in mobile banking applications. It generally consists of 4 or 6 digits and serves as a second factor for verifying user identity.

### 🏦 Common Use Cases
- Accessing mobile banking apps (e.g., SBI YONO, HDFC Bank, OneBanc).
- Performing transactions.
- Changing sensitive settings.

---

## ⚠️ Vulnerabilities of MPINs

### 1. **Commonly Used PINs**
Users often choose predictable MPINs like:
- `1234`, `0000`, `1111`, `1212`, etc.

These are easily guessable and widely targeted by brute-force attacks.

### 2. **Demographic-based PINs**
MPINs are frequently derived from personal events, such as:
- **User's Date of Birth**
- **Spouse's Date of Birth**
- **Wedding Anniversary**

Attackers with access to basic personal information may easily guess these MPINs.

### 🔐 Real-World Countermeasures
- Enforce MPIN complexity rules.
- Prevent use of demographic data in PIN.
- Integrate biometric authentication.
- Implement rate-limiting and lockout mechanisms.

---

## 📌 Problem Statement

This project aims to:
1. Detect if the entered MPIN is commonly used.
2. Evaluate if it's related to user demographics (DOB, Spouse DOB, Anniversary).
3. Return `WEAK` or `STRONG` classification.
4. Provide reasons if the MPIN is weak.
5. Support both 4-digit and 6-digit MPINs.
6. Offer a user-friendly GUI and test coverage.

---

## ✅ My Solution

### 🧩 Part A: Detect Commonly Used PINs
Checks the entered MPIN against a list of known common MPINs.

#### 🔍 Logic
```python
if mpin in commonly_used_pin_list:
    mark_as_weak("COMMONLY_USED")
`````

### 🧩 Part B: Demographic-Based Check

This part checks if the MPIN is derived from any known demographic information that users often use out of convenience. These combinations are predictable and weaken the MPIN's security.

#### 🧠 Inputs

- **User DOB**
- **Spouse DOB**
- **Wedding Anniversary**

#### 🔍 Logic

For each of the above dates, we generate multiple combinations using formats like `DDMM`, `MMDD`, `YYMMDD`, `YYYYMM`, etc., and check whether the given MPIN matches any of these combinations.

```python
if mpin in get_date_variants(user_dob):
    mark_as_weak("DEMOGRAPHIC_DOB_SELF")

if mpin in get_date_variants(spouse_dob):
    mark_as_weak("DEMOGRAPHIC_DOB_SPOUSE")

if mpin in get_date_variants(anniversary):
    mark_as_weak("DEMOGRAPHIC_ANNIVERSARY")
`````
#### ✅ Output
- **Strength: WEAK or STRONG**
### 🧩 Part C: Full Weakness Reasoning System

This part builds upon Part A and Part B by not only determining the **strength** of the MPIN but also clearly **explaining the reasons** behind a weak classification.

#### 🧠 Inputs

- **MPIN** (4-digit)
- **User DOB**
- **Spouse DOB**
- **Wedding Anniversary**

#### 🔍 Logic

We check the MPIN for two types of weaknesses:

1. **Commonly Used MPINs**  
   Compared against a predefined list of the most frequently used PINs (e.g., `1234`, `0000`, `1111`, etc.)

2. **Demographic Matches**  
   Using the `get_date_variants()` function to generate all meaningful combinations from each date input and checking if the MPIN matches any of those.

Each reason is appended to a list of weakness reasons:

```python
weak_reasons = []

if mpin in commonly_used_mpin_list:
    weak_reasons.append("COMMONLY_USED")

if mpin in get_date_variants(user_dob):
    weak_reasons.append("DEMOGRAPHIC_DOB_SELF")

if mpin in get_date_variants(spouse_dob):
    weak_reasons.append("DEMOGRAPHIC_DOB_SPOUSE")

if mpin in get_date_variants(anniversary):
    weak_reasons.append("DEMOGRAPHIC_ANNIVERSARY")

if weak_reasons:
    strength = "WEAK"
else:
    strength = "STRONG"
`````
#### ✅ Output
- **Strength: WEAK or STRONG**

- **Reasons (if WEAK):** An array containing any of the following:

- **COMMONLY_USED**

- **DEMOGRAPHIC_DOB_SELF**

- **DEMOGRAPHIC_DOB_SPOUSE**

- **DEMOGRAPHIC_ANNIVERSARY**

**If no weaknesses are found, the array will be empty, and the strength will be marked as STRONG.**
