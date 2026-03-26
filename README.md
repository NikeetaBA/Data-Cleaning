# 🚢 Supply Chain Demand Forecasting — Maritime Port Performance

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0.1-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange)
![Step](https://img.shields.io/badge/Step-1%20of%205%20Complete-brightgreen)

> A real-world supply chain analytics project built to demonstrate job-ready skills in data cleaning, time series forecasting, and business intelligence for logistics firms.

---

## 📌 Project Overview 

This project analyses **maritime port performance data** across 23 economies and 9 vessel market types to forecast port dwell time and vessel capacity trends — a core task for supply chain and logistics analysts.

| | |
|---|---|
| **Dataset** | Maritime Port Performance (UNCTAD / World Bank) |
| **Coverage** | 23 economies · 9 vessel types · 2022–2023 |
| **Key metric** | `median_port_time_days` (port dwell time) |
| **Goal** | Forecast port performance KPIs and surface actionable insights |

---

## 🗂️ Project Structure

```
supply-chain-forecasting/
│
├── data/
│   ├── raw/
│   │   └── Maritime Port Performance Project Dataset.csv
│   └── clean/
│       └── maritime_clean.csv                  ← generated after Step 1
│
├── 01_data_cleaning.py                         ← ✅ done
├── 02_eda.py                                   ← 🔜 coming next
├── 03_feature_engineering.py                   ← 🔜 upcoming
├── 04_forecasting_models.py                    ← 🔜 upcoming
├── 05_dashboard.py                             ← 🔜 upcoming
│
├── requirements.txt
└── README.md
```

---

## 🚀 Roadmap

| # | Step | Description | Status |
|---|---|---|---|
| 1 | Data Cleaning | Fix columns, parse dates, handle missing values, cap outliers | ✅ Done |
| 2 | EDA | Distributions, trends, correlations across economies & markets | 🔜 Next |
| 3 | Feature Engineering | Lag features, rolling averages, calendar encoding | 🔜 Upcoming |
| 4 | Forecasting Models | ARIMA → Prophet → XGBoost benchmark | 🔜 Upcoming |
| 5 | Dashboard & Report | Power BI dashboard + executive summary | 🔜 Upcoming |

---

## 🧹 Step 1 — Data Cleaning (`01_data_cleaning.py`)

### What it does

Takes the raw CSV (20 messy columns) and produces a clean, analysis-ready file (21 well-named columns).

### 8 cleaning steps applied

```
Raw CSV  (803 rows x 20 cols)
   |
   |-- 01  Drop junk index column (Unnamed: 0)
   |-- 02  Rename 19 verbose columns -> short snake_case names
   |-- 03  Parse "2022-S1" -> year = 2022, half = 1
   |-- 04  Convert 8 text flag columns -> True/False boolean
   |-- 05  Strip whitespace from category labels
   |-- 06  Cap outliers with 3xIQR (62 values clipped, 0 rows dropped)
   |-- 07  Reorder columns: IDs -> KPIs -> missing flags
   |-- 08  Sort by economy -> vessel_market -> year -> half
   |
Clean CSV  (803 rows x 21 cols)  ->  maritime_clean.csv
```

### Key columns after cleaning

| Column | Description |
|---|---|
| `economy` | Country / region (e.g. China, World) |
| `vessel_market` | Ship type (e.g. Container ships, Dry bulk carriers) |
| `year` / `half` | Parsed from period — e.g. 2022-S1 becomes 2022, 1 |
| `avg_vessel_age_yrs` | Average vessel age in years |
| `median_port_time_days` | Key forecast target — days a vessel spends in port |
| `avg_cargo_cap_dwt` | Average cargo capacity in Dead Weight Tonnes |
| `avg_container_cap_teu` | Container capacity in TEU (container ships only) |
| `missing_*` | Boolean flags — True means value was not available |

### Missing value summary

| Column | Missing | Note |
|---|---|---|
| `avg_vessel_age_yrs` | 0% | Fully complete |
| `median_port_time_days` | 22% | Some economies did not report |
| `avg_cargo_cap_dwt` | 23% | Some vessel types do not carry cargo |
| `avg_container_cap_teu` | 77% | Expected — TEU only applies to container ships |

---

## Setup & Run

### Requirements

- Python 3.8 or higher
- 2 packages for Step 1: `pandas` and `numpy`

### 1 — Clone the repo

```bash
git clone https://github.com/your-username/supply-chain-forecasting.git
cd supply-chain-forecasting
```

### 2 — Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3 — Install packages

```bash
pip install -r requirements.txt
```

### 4 — Run Step 1

```bash
python 01_data_cleaning.py
```

### Expected terminal output

```
Loaded: 803 rows x 20 columns
Outliers clipped (3xIQR):
  median_port_time_days: 14 values
  avg_vessel_size_gt: 48 values

Cleaned dataset: 803 rows x 21 columns
Economies: 23
Vessel markets: 9
Periods: ['2022-S1', '2022-S2', '2023-S1', '2023-S2']
Duplicates: 0

Saved: maritime_clean.csv
```

### Clean up pycache

```bash
# Remove existing pycache folders
find . -type d -name __pycache__ -exec rm -rf {} +

# Prevent creation going forward
export PYTHONDONTWRITEBYTECODE=1
```

---

## Common Errors

| Error | Fix |
|---|---|
| `FileNotFoundError: Maritime Port Performance...` | Make sure the CSV is inside `data/raw/` |
| `ModuleNotFoundError: No module named 'pandas'` | Run `pip install -r requirements.txt` |
| `(venv)` not visible in terminal | Re-run the activate command from Step 2 |

---

## Dependencies

Step 1 (cleaning) uses only:

```
pandas==3.0.1
numpy==2.4.2
```

Full project dependencies will be added to `requirements.txt` as each phase is built.

---

## About This Project

Built as a portfolio project to demonstrate supply chain analytics skills for logistics analyst roles. Covers the complete analyst workflow: raw data → cleaning → EDA → ML forecasting → executive dashboard.

**Skills demonstrated:** Python · Pandas · Time Series · ARIMA · Prophet · XGBoost · Power BI · Supply Chain KPIs

---

*Dataset: UNCTAD / World Bank Maritime Port Performance indicators*
