"""
src/framework/__init__.py
-------------------------
Career-Readiness Framework Construction package.
Transforms empirical findings into an operational 4-Quadrant Talent Matrix,
4-Stage Career Progression Roadmap, and Four Stakeholder Action Blueprints.
"""

from src.framework.quadrant_matrix import build_four_quadrant_tables
from src.framework.blueprints import build_blueprint_tables

__all__ = ["build_four_quadrant_tables", "build_blueprint_tables"]
