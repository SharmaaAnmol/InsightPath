# Raw Data Inventory & Integrity Verification (Phase 1)

## 1. Executive Summary & Verification Environment

This document establishes the physical inventory and integrity verification of all raw datasets provided for the SAS CU Hackathon analytics project. The audit was conducted in `/Users/anmolsharma/Desktop/DataScienceTool` using SHA-256 cryptographic hashing to confirm that the source datasets remain 100% byte-for-byte identical between the workspace root and the read-only storage directory `data/raw/`.

* **Audit Timestamp**: `2026-10-07T15:05:00+05:30`
* **Audit Runtime**: Python 3.13 (macOS Darwin)
* **Integrity Status**: **100% Byte-for-Byte Preservation Verified**

---

## 2. Raw Dataset Physical Inventory Table

| Dataset | Workspace Root Path | Preserved Raw Path | Format | Size (Bytes) | SHA-256 Digest (First 16 chars) | Sheet Count | Sheet Names | Row Count | Col Count | Read Status |
|---|---|---|---|---|---|---|---|---|---|---|
| **Data Science Jobs** | `DataScience Jobs.csv` | `data/raw/DataScience Jobs.csv` | CSV (UTF-8) | 96,390 | `24658523ee3e2959` | N/A | N/A | 1,602 | 8 | PASS |
| **Analytics Jobs** | `Analytics Jobs.csv` | `data/raw/Analytics Jobs.csv` | CSV (UTF-8) | 3,610,518 | `c0bfd52e0685e6c8` | N/A | N/A | 15,841 | 8 | PASS |
| **JDS Skill Traits** | `JDS Skill Traits.xlsx` | `data/raw/JDS Skill Traits.xlsx` | XLSX (XML) | 16,190 | `2dc0a3f0702bf175` | 1 | `['JDS']` | 171 | 7 | PASS |
| **SDS Personality Traits**| `SDS Personality Traits.xlsx`| `data/raw/SDS Personality Traits.xlsx`| XLSX (XML) | 14,839 | `112a08e50c655e57` | 1 | `['SDS']` | 161 | 7 | PASS |
| **Data Description Doc** | `Data Description Doc.pdf` | N/A | PDF | — | N/A | — | — | — | — | **ABSENT (NOT VERIFIED FROM SOURCE DATA)** |
| **Problem Context Brief...**| `Problem Context Brief...pdf` | N/A | PDF | — | N/A | — | — | — | — | **ABSENT (NOT VERIFIED FROM SOURCE DATA)** |

---

## 3. Detailed Dataset Specifications

### 3.1. Dataset 1: Data Science Jobs (`DataScience Jobs.csv`)
* **Physical Path**: `/Users/anmolsharma/Desktop/DataScienceTool/data/raw/DataScience Jobs.csv`
* **Encoding**: Standard ASCII / UTF-8 text.
* **Row Dimensions**: Exactly 1,602 rows (1 header row + 1,602 data rows).
* **Column Dimensions**: 8 columns.
* **Column Names**: `reference_no`, `company_name`, `job_title`, `min_experience`, `avg_salary`, `min_salary`, `max_salary`, `num_of_jobs`.
* **Duplicate Columns**: 0 duplicate column names.
* **Integrity Status**: Identical between root and `data/raw/` (`SHA256: 24658523ee3e2959...`).

### 3.2. Dataset 2: Analytics Jobs (`Analytics Jobs.csv`)
* **Physical Path**: `/Users/anmolsharma/Desktop/DataScienceTool/data/raw/Analytics Jobs.csv`
* **Encoding**: UTF-8 with standard comma separation.
* **Row Dimensions**: Exactly 15,841 rows (1 header row + 15,841 data rows).
* **Column Dimensions**: 8 columns.
* **Column Names**: `s_no`, `experience`, `job_description`, `job_desig`, `job_type`, `key_skills`, `location`, `salary`.
* **Duplicate Columns**: 0 duplicate column names.
* **Integrity Status**: Identical between root and `data/raw/` (`SHA256: c0bfd52e0685e6c8...`).

### 3.3. Dataset 3: Junior Data Scientist Skill Traits (`JDS Skill Traits.xlsx`)
* **Physical Path**: `/Users/anmolsharma/Desktop/DataScienceTool/data/raw/JDS Skill Traits.xlsx`
* **Workbook Structure**: Exactly 1 worksheet named `JDS`.
* **Raw Table Dimensions**: 171 rows, 7 columns.
* **Valid Records**: Exactly 139 records (Rows 140–171 are 100% empty trailing cells).
* **Column Names**: `id`, `big_data_skills`, `maths-stats_skills`, `coding_skills`, `ai_and_ml_skills`, `dashboard_and_storytelling_skills`, `salary_hike_high_or_low`.
* **Duplicate Columns**: 0 duplicate column names.
* **Integrity Status**: Identical between root and `data/raw/` (`SHA256: 2dc0a3f0702bf175...`).

### 3.4. Dataset 4: Senior Data Scientist Personality Traits (`SDS Personality Traits.xlsx`)
* **Physical Path**: `/Users/anmolsharma/Desktop/DataScienceTool/data/raw/SDS Personality Traits.xlsx`
* **Workbook Structure**: Exactly 1 worksheet named `SDS`.
* **Raw Table Dimensions**: Exactly 161 rows, 7 columns.
* **Valid Records**: Exactly 161 records (0 null rows).
* **Column Names (Raw String Values)**: `'id'`, `'neuroticism'`, `' extraversion'` *(leading space)*, `'openness_to_experience'`, `'agreeableness'`, `'conscientiousness'`, `'success_ classification_ high_low'` *(internal spaces)*.
* **Duplicate Columns**: 0 duplicate column names.
* **Integrity Status**: Identical between root and `data/raw/` (`SHA256: 112a08e50c655e57...`).

---

## 4. Discrepancy & Verification Findings

1. **Root vs Raw Synchronicity**: Every source dataset in the workspace root matches its corresponding backup in `data/raw/` byte-for-byte.
2. **Missing PDF Documentation**: Neither `Data Description Doc.pdf` nor `Problem Context Brief, SAS VFL Demos, Guidelines Dos and Donts.pdf` exists in the workspace. Their context is known through the hackathon prompt brief, but the physical PDF files could not be inspected.
3. **Non-Destructive Guarantee**: In strict compliance with Rule 1, no raw dataset file has been modified, overwritten, or renamed.
