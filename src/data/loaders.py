"""
loaders.py
----------
Reusable and robust data ingestion functions for CSV and XLSX files.
Ensures raw source files are loaded without modification.
Includes a standard-library XLSX reader to ensure independence from third-party binary libraries.
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple
import pandas as pd


def load_csv_dataset(file_path: str, **kwargs) -> pd.DataFrame:
    """Load a CSV dataset in read-only mode returning a pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    return pd.read_csv(file_path, **kwargs)


def load_excel_dataset(file_path: str, sheet_name: Optional[str] = None) -> Tuple[List[str], pd.DataFrame]:
    """
    Load an Excel (.xlsx) file using standard library zipfile/XML parsing.
    Guarantees zero mutation of the raw file and independence from openpyxl.
    
    Returns:
        Tuple of (list_of_sheet_names, DataFrame_of_first_or_specified_sheet)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel file not found: {file_path}")
        
    with zipfile.ZipFile(file_path, "r") as z:
        # Extract workbook sheet names
        wb_tree = ET.fromstring(z.read("xl/workbook.xml"))
        sheet_elems = wb_tree.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet")
        sheets = [s.get("name") for s in sheet_elems]
        
        # Load shared strings table if present
        strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            ss_tree = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in ss_tree.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si"):
                text = "".join([
                    t.text for t in si.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")
                    if t.text is not None
                ])
                strings.append(text)
        
        # Determine target sheet XML path
        target_idx = 1
        if sheet_name and sheet_name in sheets:
            target_idx = sheets.index(sheet_name) + 1
        sheet_path = f"xl/worksheets/sheet{target_idx}.xml"
        if sheet_path not in z.namelist():
            # Fallback to first available sheet in namelist
            sheet_files = sorted([f for f in z.namelist() if f.startswith("xl/worksheets/sheet") and f.endswith(".xml")])
            sheet_path = sheet_files[0]
            
        sheet_tree = ET.fromstring(z.read(sheet_path))
        rows = []
        for row in sheet_tree.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row"):
            cols = {}
            for c in row.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c"):
                r = c.get("r", "")
                col_letter = "".join([ch for ch in r if ch.isalpha()])
                col_idx = 0
                for ch in col_letter:
                    col_idx = col_idx * 26 + (ord(ch.upper()) - ord("A") + 1)
                col_idx -= 1
                
                t = c.get("t")
                val_node = c.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")
                v_text = val_node.text if val_node is not None else None
                
                if t == "s" and v_text is not None:
                    cols[col_idx] = strings[int(v_text)]
                else:
                    cols[col_idx] = v_text
                    
            if cols:
                max_c = max(cols.keys()) + 1
                row_data = [cols.get(i, None) for i in range(max_c)]
                rows.append(row_data)
                
        if not rows:
            return sheets, pd.DataFrame()
            
        max_cols = max(len(r) for r in rows)
        norm_rows = [r + [None] * (max_cols - len(r)) for r in rows]
        df = pd.DataFrame(norm_rows[1:], columns=norm_rows[0])
        return sheets, df


def load_all_raw_datasets(base_dir: str = "data/raw") -> Dict[str, pd.DataFrame]:
    """
    Load all four raw hackathon datasets into memory as DataFrames.
    Does NOT modify the raw files.
    """
    datasets = {}
    
    # 1. Data Science Jobs
    ds_path = os.path.join(base_dir, "DataScience Jobs.csv")
    datasets["DataScience Jobs"] = load_csv_dataset(ds_path)
    
    # 2. Analytics Jobs
    aj_path = os.path.join(base_dir, "Analytics Jobs.csv")
    datasets["Analytics Jobs"] = load_csv_dataset(aj_path)
    
    # 3. JDS Skill Traits
    jds_path = os.path.join(base_dir, "JDS Skill Traits.xlsx")
    _, df_jds = load_excel_dataset(jds_path)
    datasets["JDS Skill Traits"] = df_jds
    
    # 4. SDS Personality Traits
    sds_path = os.path.join(base_dir, "SDS Personality Traits.xlsx")
    _, df_sds = load_excel_dataset(sds_path)
    datasets["SDS Personality Traits"] = df_sds
    
    return datasets
