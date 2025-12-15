# 🏗️ Blueprint Builder FIBO Compliance Engine

> **Where FIBO Standards Meet Frontend Velocity.**

[![React 18](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg)](https://www.typescriptlang.org/)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](#-copyright--license)
[![Hackathon](https://img.shields.io/badge/Bria_FIBO-Hackathon_2025-orange)](https://github.com/)

**Blueprint Compliance Engine** is a robust validation suite that visualizes and enforces financial data integrity. It provides a seamless interface for validating raw asset data against strict FIBO (Financial Industry Business Ontology) schemas and semantic business rules, ensuring every asset is audit-ready before it hits the ledger.

---

## 🚨 The Problem

Managing financial asset data is error-prone. JSON syntax errors, missing fields, or subtle business rule violations (like a Bond priced too low) often go unnoticed until they break downstream systems.

* **Schema failures:** Incorrect data types or formatting.
* **Semantic gaps:** Logical inconsistencies that pass code validation but fail business compliance.
* **Opaque history:** No record of *who* validated *what* and *when*.

Blueprint Compliance Engine solves this by providing immediate visual feedback, auto-conversion tools, and an immutable validation history.

## ✨ Key Features

### 🛡️ Dual-Layer Validation
We go beyond simple syntax checking.
* **Schema Layer:** Enforces structure (e.g., Asset ID length, data types, required arrays).
* **Semantic Layer:** Enforces business logic (e.g., flagging suspicious pricing or generic issuer names).

### 🔧 Intelligent Data Ingestion
Stop wrestling with formatting.
* **Smart Convert:** Automatically transforms raw key-value text pairs into valid JSON.
* **URL Fetch:** Pulls live data from remote endpoints directly into the validator.
* **File Import:** seamless `.json` file loading.

### 📊 Immutable History Ledger
Every action is recorded. The engine maintains a local ledger of every validation attempt, complete with:
* **Trace IDs:** Unique identifiers for every transaction.
* **Iteration Counts:** Tracking validation cycles.
* **Result Badges:** Clear visual indicators (Valid, Semantic Fail, Schema Fail).

### 📤 Export & Audit
Generate proof of compliance instantly. Export your entire validation history ledger as a standardized JSON file for external auditing and reporting.

---

## 🚀 How It Works

```mermaid
graph TD
    A[Raw Input / URL / File] -->|Ingest| B{Format Check}
    B -->|Smart Convert| C[JSON Object]
    C -->|Validate| D{Compliance Engine}
    D -->|Check 1| E[Schema Rules]
    D -->|Check 2| F[Semantic Logic]
    E & F -->|Result| G[Validation Status]
    G -->|Log| H[(History Ledger)]
    H -->|Export| I[Audit Report]
````

## 🛠️ Installation

1.  **Clone the repository**

    ```bash
    git clone [https://github.com/your-username/blueprint-compliance-engine.git](https://github.com/your-username/blueprint-compliance-engine.git)
    cd blueprint-compliance-engine
    ```

2.  **Install dependencies**

    ```bash
    npm install
    # or
    yarn install
    ```

3.  **Run the application**

    ```bash
    npm run dev
    ```

## 💻 Usage Example

The Engine is designed for real-time interaction.

**Input (Raw Text):**

```text
asset_id: BOND456
asset_type: Bond
issuer_name: Government Corp
price: 1000
```

**Action:**
Click **"🔄 Convert to JSON"** then **"🔍 Validate Asset"**.

**Output (Validation Result Panel):**

> **⚠️ SEMANTIC FAIL**
>
> **Semantic Validation Failed**
> • Issuer name appears too short or generic for regulatory compliance
> • Insufficient documentation for regulatory standards (minimum 2 required)

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
