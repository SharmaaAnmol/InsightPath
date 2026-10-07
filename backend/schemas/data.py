"""
backend/schemas/data.py
-----------------------
Pydantic schemas for data-table endpoints serving validated CSV outputs.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TableResponse(BaseModel):
    table_name: str = Field(..., description="Logical identifier of the table")
    source_path: str = Field(..., description="Relative path of source CSV in repository")
    row_count: int = Field(..., description="Number of records returned")
    columns: List[str] = Field(..., description="List of column names")
    records: List[Dict[str, Any]] = Field(..., description="List of row dictionaries")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional context or summary metrics")
