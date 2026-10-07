"""
src/synthesis/__init__.py
-------------------------
Cross-dataset analytical synthesis and methodological triangulation package.
Integrates findings across macro job demand, micro skill postings, junior skill velocity,
and senior consulting behavioral profiles without row-level joins.
"""

from src.synthesis.triangulation import build_all_phase7_synthesis_tables

__all__ = ["build_all_phase7_synthesis_tables"]
