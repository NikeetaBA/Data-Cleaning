"""
Supply Chain Forecasting Project
Step 1: Data Cleaning — Maritime Port Performance Dataset
=========================================================
Input:  Maritime Port Performance Project Dataset.csv
Output: maritime_clean.csv

Cleaning steps applied:
  1. Drop unnamed index column
  2. Rename columns to clean snake_case
  3. Parse period (2022-S1) → year + half integer columns
  4. Convert text MissingValue flag columns → boolean missing_* indicators
  5. Strip whitespace from categorical labels
  6. Cap outliers using 3×IQR method on numeric KPI columns
  7. Reorder columns logically (IDs → KPIs → flags)
  8. Sort rows by economy → vessel_market → year → half
"""

import pandas as pd
import numpy as np

# ── Load raw data ─────────────────────────────────────────────────────────────
df = pd.read_csv("Maritime Port Performance Project Dataset.csv")
print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# ── Step 1: Drop unnamed index column ─────────────────────────────────────────
def new_func(df):
    df = df.drop(columns=["Unnamed: 0"])
    return df

df = new_func(df)

# ── Step 2: Rename columns ────────────────────────────────────────────────────
rename_map = {
    "Economy_Label":                                                                  "economy",
    "CommercialMarket_Label":                                                         "vessel_market",
    "Average_age_of_vessels_years_Value":                                             "avg_vessel_age_yrs",
    "Average_age_of_vessels_years_MissingValue":                                      "_flag_vessel_age",
    "Median_time_in_port_days_Value":                                                 "median_port_time_days",
    "Median_time_in_port_days_MissingValue":                                          "_flag_port_time",
    "Average_size_GT_of_vessels_Value":                                               "avg_vessel_size_gt",
    "Average_size_GT_of_vessels_MissingValue":                                        "_flag_vessel_size",
    "Average_cargo_carrying_capacity_dwt_per_vessel_Value":                           "avg_cargo_cap_dwt",
    "Average_cargo_carrying_capacity_dwt_per_vessel_MissingValue":                    "_flag_cargo_cap",
    "Average_container_carrying_capacity_TEU_per_container_ship_Value":               "avg_container_cap_teu",
    "Average_container_carrying_capacity_TEU_per_container_ship_MissingValue":        "_flag_container_cap",
    "Maximum_size_GT_of_vessels_Value":                                               "max_vessel_size_gt",
    "Maximum_size_GT_of_vessels_MissingValue":                                        "_flag_max_vessel_size",
    "Maximum_cargo_carrying_capacity_dwt_of_vessels_Value":                           "max_cargo_cap_dwt",
    "Maximum_cargo_carrying_capacity_dwt_of_vessels_MissingValue":                    "_flag_max_cargo",
    "Maximum_container_carrying_capacity_TEU_of_container_ships_Value":               "max_container_cap_teu",
    "Maximum_container_carrying_capacity_TEU_of_container_ships_MissingValue":        "_flag_max_container",
    "period":                                                                         "period",
}
df = df.rename(columns=rename_map)

# ── Step 3: Parse period → year + half ────────────────────────────────────────
# Format is "2022-S1" → year=2022, half=1 (S1=H1, S2=H2)
df["year"] = df["period"].str[:4].astype(int)
df["half"] = df["period"].str[-1].astype(int)

# ── Step 4: Flag columns → boolean missing indicators ─────────────────────────
# Some flag cols are float64 (all NaN = never flagged), others are str dtype
flag_cols = [c for c in df.columns if c.startswith("_flag_")]
for fc in flag_cols:
    bool_col = fc.replace("_flag_", "missing_")
    col = df[fc]
    if col.dtype == object or str(col.dtype) == "str":
        # Text: "Not available or not separately reported" → True
        df[bool_col] = col.str.startswith("Not", na=False)
    else:
        # Float64 all-NaN: data was always present → False
        df[bool_col] = False
df = df.drop(columns=flag_cols)

# ── Step 5: Strip whitespace from categorical labels ──────────────────────────
df["economy"]      = df["economy"].str.strip()
df["vessel_market"] = df["vessel_market"].str.strip()

# ── Step 6: Cap outliers with 3×IQR ──────────────────────────────────────────
# Preserves the row but brings extreme values to a defensible bound.
# 3×IQR is used (vs 1.5×IQR) to avoid over-clipping legitimate port extremes.
numeric_kpi = [
    "avg_vessel_age_yrs",
    "median_port_time_days",
    "avg_vessel_size_gt",
    "avg_cargo_cap_dwt",
    "avg_container_cap_teu",
    "max_vessel_size_gt",
    "max_cargo_cap_dwt",
    "max_container_cap_teu",
]
outlier_report = {}
for col in numeric_kpi:
    series = df[col].dropna()
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 3 * iqr, q3 + 3 * iqr
    n_clipped = int(((df[col] < lo) | (df[col] > hi)).sum())
    df[col] = df[col].clip(lower=lo, upper=hi)
    outlier_report[col] = n_clipped

print("Outliers clipped (3×IQR):")
for col, n in outlier_report.items():
    if n > 0:
        print(f"  {col}: {n} values")

# ── Step 7: Reorder columns ───────────────────────────────────────────────────
id_cols      = ["economy", "vessel_market", "period", "year", "half"]
missing_cols = [c for c in df.columns if c.startswith("missing_")]
df = df[id_cols + numeric_kpi + missing_cols]

# ── Step 8: Sort ──────────────────────────────────────────────────────────────
df = df.sort_values(["economy", "vessel_market", "year", "half"]).reset_index(drop=True)

# ── Summary ───────────────────────────────────────────────────────────────────
print(f"\nCleaned dataset: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Economies: {df['economy'].nunique()}")
print(f"Vessel markets: {df['vessel_market'].nunique()}")
print(f"Periods: {sorted(df['period'].unique())}")
print(f"Duplicates: {df.duplicated(subset=['economy','vessel_market','period']).sum()}")
print("\nMissing values per KPI:")
for col in numeric_kpi:
    n   = df[col].isnull().sum()
    pct = 100 * n / len(df)
    print(f"  {col}: {n} ({pct:.1f}%)")

# ── Save ──────────────────────────────────────────────────────────────────────
df.to_csv("maritime_clean.csv", index=False)
print("\n✓ Saved: maritime_clean.csv")
