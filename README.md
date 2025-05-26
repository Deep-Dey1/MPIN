# MPIN
This repository contains a basic project to find Weak MPINs by predicting the MPIN as guessable or commonly used one. To fix the Weak MPINS this project suggest the users more secure and unique MPINs for their use using GUI and web application.

# 🔐 MPIN Security Assessment – OneBanc Assignment

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

