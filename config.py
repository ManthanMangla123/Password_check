"""
Configuration module for password strength evaluation system.

Centralizes all security thresholds, scoring parameters, and system constants.
This ensures maintainability and allows security policies to be adjusted without
modifying core logic.
"""

from typing import Dict, List

# Scoring thresholds
SCORE_THRESHOLDS = {
    "WEAK": 40,
    "MEDIUM": 60,
    "STRONG": 80,
    "VERY_STRONG": 100
}

# Entropy calculation parameters
MIN_ENTROPY_BITS = 20  # Minimum acceptable entropy for any password
ENTROPY_PENALTY_MULTIPLIER = 0.3  # Reduce entropy by 30% when patterns detected

# Character pool sizes for entropy calculation
CHAR_POOL_SIZES = {
    "lowercase": 26,
    "uppercase": 26,
    "digits": 10,
    "special": 33  # Common special characters: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
}

# Pattern detection thresholds
PATTERN_THRESHOLDS = {
    "min_repeat_length": 3,  # Minimum consecutive repeated characters to flag
    "min_sequence_length": 4,  # Minimum sequential characters to flag
    "min_keyboard_pattern_length": 4,  # Minimum keyboard pattern length
    "max_year_range": (1900, 2099),  # Year pattern detection range
    "min_dictionary_word_length": 4,  # Minimum word length to check in dictionary
}

# Penalty weights for different pattern types
PATTERN_PENALTIES = {
    "repeated_chars": 15,  # Score penalty for repeated characters
    "sequential_chars": 20,  # Score penalty for sequential patterns
    "keyboard_pattern": 25,  # Score penalty for keyboard patterns
    "leetspeak": 10,  # Score penalty for leetspeak substitutions
    "dictionary_word": 30,  # Score penalty for dictionary words
    "year_pattern": 15,  # Score penalty for year patterns
    "username_similarity": 25,  # Score penalty for username/email similarity
    "low_variety": 20,  # Score penalty for low character variety
}

# Breach detection configuration
BREACH_CONFIG = {
    "local_blacklist_file": "data/top_10k_passwords.txt",
    "hibp_api_url": "https://api.pwnedpasswords.com/range/",
    "hibp_enabled": False,  # Set to True to enable HIBP API (requires internet)
    "breach_force_weak": True,  # Force WEAK classification if breached
}

# File paths
DATA_DIR = "data"
WORDLIST_FILE = f"{DATA_DIR}/common_words.txt"
BLACKLIST_FILE = f"{DATA_DIR}/top_10k_passwords.txt"

# Similarity check configuration
SIMILARITY_THRESHOLD = 0.5  # Minimum similarity ratio to flag username/email match

# Character variety thresholds
MIN_CHAR_VARIETY_RATIO = 0.3  # Minimum unique chars / total length ratio

def get_char_pool_size(has_lower: bool, has_upper: bool, has_digit: bool, has_special: bool) -> int:
    """
    Calculate character pool size based on detected character classes.
    
    This is critical for accurate entropy calculation. The pool size directly
    affects entropy, which is the foundation of password strength assessment.
    
    Args:
        has_lower: Whether password contains lowercase letters
        has_upper: Whether password contains uppercase letters
        has_digit: Whether password contains digits
        has_special: Whether password contains special characters
    
    Returns:
        Total character pool size available for password generation
    """
    pool_size = 0
    if has_lower:
        pool_size += CHAR_POOL_SIZES["lowercase"]
    if has_upper:
        pool_size += CHAR_POOL_SIZES["uppercase"]
    if has_digit:
        pool_size += CHAR_POOL_SIZES["digits"]
    if has_special:
        pool_size += CHAR_POOL_SIZES["special"]
    
    # Minimum pool size to prevent division by zero
    return max(pool_size, 1)

