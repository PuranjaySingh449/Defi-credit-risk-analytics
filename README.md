# DeFi Credit Risk Analytics

An end-to-end data science and analytics project focused on **credit risk assessment in decentralized finance (DeFi)** using **on-chain blockchain data**.

This project demonstrates how borrower behavior alone — without traditional financial history — can be used to derive **credit scores, risk tiers, and actionable insights**.

---

## 📌 Project Overview

Traditional credit scoring relies on centralized financial records.  
In DeFi, borrower behavior is fully transparent on-chain.

This project explores how **on-chain borrowing and repayment activity** can be transformed into a **credit risk analytics system**.

### Key objectives:
- Extract raw borrower activity from the blockchain
- Engineer behavioral features from transactions
- Design a rule-based credit scoring system
- Segment borrowers into risk tiers
- Validate insights using business intelligence dashboards

---

## 🔍 Data Source

- **Protocol:** Aave (DeFi lending protocol)
- **Data Access:** The Graph (GraphQL API)
- **Events Used:** Borrow and Repay events
- **Scale:** ~70,000 unique borrowers

A custom extraction script handles:
- GraphQL pagination
- Timestamp ordering
- Large-scale event collection

---

## 🧠 Methodology

### 1️⃣ Data Extraction
- Implemented a Python script (`timedata.py`) to query the Aave subgraph
- Extracted large-scale borrow and repay events with timestamps
- Stored raw activity as structured CSV datasets

### 2️⃣ Feature Engineering
Derived behavioral features such as:
- Borrow frequency
- Repayment behavior
- Activity duration
- Aggregate borrowing patterns

### 3️⃣ Credit Scoring
- Designed a **rule-based credit score (0–100)**
- Score reflects repayment consistency and borrowing behavior
- No machine learning used in the base scoring logic (for interpretability)

### 4️⃣ Risk Segmentation
Borrowers classified into:
- **Low Risk**
- **Medium Risk**
- **High Risk**

Based on score thresholds and behavioral consistency.

### 5️⃣ Validation & Visualization
- Built an interactive **Power BI dashboard**
- Validated that:
  - Low-risk borrowers have higher average scores
  - High-risk borrowers cluster at low scores
- Used BI for explainability and monitoring

---

## 📊 Power BI Dashboard

The dashboard includes:
- Total borrowers KPI
- Average credit score KPI
- Risk tier distribution (donut chart)
- Average credit score by risk tier (bar chart)

📁 Screenshots are available in the `powerbi/screenshots/` folder.  
📁 The full `.pbix` file is included for interactive exploration.

---

## 🛠 Tech Stack

- **Python**
- **Pandas**
- **GraphQL**
- **Blockchain / DeFi data**
- **Feature Engineering**
- **Power BI**

---

## 📂 Repository Structure

