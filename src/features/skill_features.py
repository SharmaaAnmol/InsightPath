"""
skill_features.py
-----------------
Reusable feature engineering module for skill tokenization and multi-hot encoding.
Derives skill frequency profile across all postings without external web lists.
Provides configurable top-K binary indicator feature generation.
"""

import re
from collections import Counter
from typing import List, Tuple, Set
import pandas as pd


def tokenize_skills(skill_text: str) -> List[str]:
    """
    Deterministic skill tokenizer:
    1. Splits on commas
    2. Strips leading/trailing whitespace
    3. Lowercases tokens
    4. Filters out pure punctuation tokens (e.g. '...', '-')
    5. Preserves meaningful multi-word phrases (e.g. 'machine learning', 'business analysis')
    """
    if not isinstance(skill_text, str) or not skill_text.strip():
        return []
        
    raw_tokens = skill_text.split(",")
    valid_tokens = []
    
    for tok in raw_tokens:
        clean_tok = tok.strip().lower()
        # Filter empty or pure punctuation tokens
        if clean_tok and re.search(r"[a-zA-Z0-9]", clean_tok) and clean_tok not in ["...", "..", ".", "-", "--"]:
            valid_tokens.append(clean_tok)
            
    return valid_tokens


def build_skill_frequency_profile(
    series: pd.Series,
    total_postings: int,
    output_path: str = "outputs/tables/skill_frequency_profile.csv"
) -> pd.DataFrame:
    """
    Build vocabulary frequency ranking across all postings.
    Counts unique postings mentioning each skill (document frequency).
    Exports frequency profile table.
    """
    posting_token_sets = []
    all_tokens = []
    
    for item in series.dropna():
        tokens = tokenize_skills(str(item))
        token_set = set(tokens)
        posting_token_sets.append(token_set)
        all_tokens.extend(token_set)
        
    counts = Counter(all_tokens)
    records = []
    for rank, (skill, freq) in enumerate(counts.most_common(), start=1):
        pct = round((freq / total_postings) * 100, 2)
        records.append({
            "skill": skill,
            "frequency": freq,
            "percentage_of_postings": pct,
            "rank": rank
        })
        
    df_profile = pd.DataFrame(records)
    if output_path:
        df_profile.to_csv(output_path, index=False)
    return df_profile


def skill_to_column_name(skill: str) -> str:
    """Convert raw skill token to valid snake_case column identifier."""
    cleaned = skill.strip().lower()
    cleaned = cleaned.replace("c++", "cpp").replace("c#", "csharp").replace(".net", "dotnet")
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned).strip("_")
    return f"skill_{cleaned}"


def generate_top_k_skill_indicators(
    series: pd.Series,
    top_k_skills: List[str]
) -> pd.DataFrame:
    """
    Generate binary indicator features (0/1) for a configured list of top-K skills.
    Column names are prefixed with 'skill_'.
    """
    skill_lookup = [(s, skill_to_column_name(s)) for s in top_k_skills]
    indicators = {col_name: [] for _, col_name in skill_lookup}
    
    for item in series:
        tokens = set(tokenize_skills(str(item)))
        for raw_skill, col_name in skill_lookup:
            indicators[col_name].append(1 if raw_skill in tokens else 0)
            
    return pd.DataFrame(indicators, index=series.index)

