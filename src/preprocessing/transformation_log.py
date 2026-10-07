"""
transformation_log.py
---------------------
Reusable transformation logger for Phase 2.
Records every data cleaning and transformation operation to guarantee
traceability, auditability, and reproducibility.
Exports log to outputs/tables/phase2_transformation_log.csv.
"""

import os
from datetime import datetime, timezone
from typing import List, Optional, Union
import pandas as pd


class TransformationLogger:
    """Singleton/Instance logger for tracking DataFrame transformations."""

    def __init__(self, output_path: str = "outputs/tables/phase2_transformation_log.csv"):
        self.output_path = output_path
        self.records = []

    def log_transformation(
        self,
        dataset: str,
        operation: str,
        columns: Union[str, List[str]],
        rows_before: int,
        rows_after: int,
        rows_changed: int,
        values_changed: str,
        rationale: str,
        source_phase1_finding: str,
        output_dataset: str,
        timestamp: Optional[str] = None
    ):
        """Record a single atomic transformation step."""
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()
            
        col_str = ", ".join(columns) if isinstance(columns, list) else str(columns)
        
        record = {
            "timestamp": timestamp,
            "dataset": dataset,
            "operation": operation,
            "columns": col_str,
            "rows_before": rows_before,
            "rows_after": rows_after,
            "rows_changed": rows_changed,
            "values_changed": values_changed,
            "rationale": rationale,
            "source_phase1_finding": source_phase1_finding,
            "output_dataset": output_dataset
        }
        self.records.append(record)

    def to_dataframe(self) -> pd.DataFrame:
        """Return all logged transformations as a DataFrame."""
        return pd.DataFrame(self.records)

    def save(self) -> pd.DataFrame:
        """Save transformation records to CSV."""
        df = self.to_dataframe()
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        df.to_csv(self.output_path, index=False)
        return df


# Global default logger instance
global_logger = TransformationLogger()
