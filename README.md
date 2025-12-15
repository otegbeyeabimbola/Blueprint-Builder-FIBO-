# 🏗️ Blueprint Builder

> **Where AI Meets Compliance, Automatically.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](#-copyright--license)
[![Hackathon](https://img.shields.io/badge/Bria_FIBO-Hackathon_2025-orange)](https://github.com/)

**Blueprint Builder** is a JSON-Native Compliance Engine that transforms messy AI outputs into validated, auditable financial assets. It combines rigorous schema validation with deterministic patching to ensure your data isn't just generated—it's certified.

---

## 🚨 The Problem

In the age of AI, Large Language Models (LLMs) can generate financial data in seconds. But **AI doesn't understand compliance.**

* One missing field.
* One wrong format.
* One violated business rule.

Any of these can cause an entire dataset to be rejected. Manual fixes take hours or days. Blueprint Builder solves this by automating the "Last Mile" of AI content generation.

## ✨ Key Features

### 🛡️ Bulletproof Validation
Powered by **Pydantic**, we enforce strict schema validation to catch structural errors immediately.

### 🔧 Deterministic Patching & Auto-Fix
We don't just flag errors; we fix them. Our engine uses deterministic algorithms to auto-correct violations (e.g., formatting dates, inferring missing required fields based on context).

### 🔐 Cryptographic Integrity
Every validated asset receives a **SHA-256 trace ID**. Think of it as a fingerprint; if a single byte changes, the hash breaks, ensuring total data integrity.

### 📜 Persistent Ledger & Replay
* **Audit Trails:** Every validation attempt is logged with timestamps, violations, and corrections.
* **Time Travel:** Use the **Undo/Redo** buttons to step through data states.
* **Replay:** Re-verify old assets against current rules to ensure ongoing compliance.

---

## 🚀 How It Works

```mermaid
graph TD
    A[Raw AI Output] -->|Input| B{Schema Validation}
    B -->|Error Found| C[Deterministic Patcher]
    C -->|Auto-Fix| B
    B -->|Valid| D[FIBO Semantic Rules]
    D -->|Verified| E[SHA-256 Hashing]
    E -->|Log| F[(Immutable Ledger)]
    F -->|Output| G[Certified Asset]
````

## 🛠️ Installation

1.  **Clone the repository**

    ```bash
    git clone [https://github.com/your-username/blueprint-builder.git](https://github.com/your-username/blueprint-builder.git)
    cd blueprint-builder
    ```

2.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**

    ```bash
    python main.py
    ```

## 💻 Usage Example

Blueprint Builder is designed to integrate anywhere via CLI.

**Input (Broken AI Output):**

```json
{
  "asset_type": "Bond",
  "maturity": "2025/12/01",  // Wrong format
  "face_value": "1M"         // String instead of Float
}
```

**Command:**

```bash
blueprint build --input bond_data.json --fix
```

**Output (Validated & Patched):**

```json
{
  "trace_id": "a1b2c3d4...",
  "status": "VALIDATED",
  "data": {
    "asset_type": "Bond",
    "maturity": "2025-12-01T00:00:00Z",
    "face_value": 1000000.00
  },
  "log": "Fixed date format; Converted currency string to float."
}
```

-----

## 👥 Contributors

This project was built by:

  * **Mohammed B. Kemal** - [Email](mailto:mickymicky718@gmail.com)
  * **Abimbola A. Otegbeye** - [Email](mailto:otegbeyeabimbola2017@gmail.com)

*Built with ❤️ for the **Bria FIBO Hackathon 2025**.*

-----

## ⚖️ Copyright & License

Copyright © 2025 **Mohammed B. Kemal** and **Abimbola A. Otegbeye**. All Rights Reserved.

This project is submitted for the **FIBO Hackathon 2025**. Unauthorized copying of this file, via any medium, is strictly prohibited unless authorized by the copyright holders.
