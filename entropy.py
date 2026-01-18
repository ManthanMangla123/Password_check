"""
Entropy calculation module for password strength evaluation.

Computes Shannon entropy to measure password unpredictability. Entropy is the
foundation of password strength assessment, representing the number of bits
needed to encode the password.

Security rationale: Entropy quantifies the search space an attacker must explore.
Higher entropy = larger search space = more secure password. However, entropy
alone is insufficient - patterns reduce effective entropy even if theoretical
entropy is high.
"""

import math
from typing import Dict, Tuple

from config import get_char_pool_size, ENTROPY_PENALTY_MULTIPLIER


class EntropyCalculator:
    """Calculates Shannon entropy for passwords."""
    
    @staticmethod
    def calculate_entropy(password: str, has_patterns: bool = False) -> Tuple[float, Dict[str, bool]]:
        """
        Calculate Shannon entropy for password.
        
        Entropy formula: H = L * log2(N)
        where L = password length, N = character pool size
        
        Args:
            password: Password to analyze
            has_patterns: Whether patterns were detected (applies penalty)
        
        Returns:
            Tuple of (entropy_bits, character_class_flags)
            character_class_flags: Dict indicating which character classes are present
        """
        if not password:
            return 0.0, {
                "has_lower": False,
                "has_upper": False,
                "has_digit": False,
                "has_special": False,
            }
        
        # Detect character classes
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" for c in password)
        
        # Calculate character pool size
        pool_size = get_char_pool_size(has_lower, has_upper, has_digit, has_special)
        
        # Calculate base entropy: H = L * log2(N)
        length = len(password)
        base_entropy = length * math.log2(pool_size)
        
        # Apply penalty if patterns detected
        # Patterns reduce effective entropy because they make passwords predictable
        if has_patterns:
            # Reduce entropy by penalty multiplier
            # This reflects that patterns make brute-force attacks more efficient
            effective_entropy = base_entropy * (1 - ENTROPY_PENALTY_MULTIPLIER)
        else:
            effective_entropy = base_entropy
        
        # Ensure non-negative entropy
        effective_entropy = max(0.0, effective_entropy)
        
        return effective_entropy, {
            "has_lower": has_lower,
            "has_upper": has_upper,
            "has_digit": has_digit,
            "has_special": has_special,
            "pool_size": pool_size,
        }
    
    @staticmethod
    def calculate_positional_entropy(password: str) -> float:
        """
        Calculate entropy considering character frequency at each position.
        
        This is a more sophisticated entropy calculation that accounts for
        non-uniform character distribution, but is computationally expensive.
        For production use, we use the simpler pool-based calculation.
        
        Args:
            password: Password to analyze
        
        Returns:
            Positional entropy in bits
        """
        if not password:
            return 0.0
        
        # Character frequency analysis
        char_counts = {}
        for char in password:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        # Calculate entropy using frequency distribution
        length = len(password)
        entropy = 0.0
        
        for char, count in char_counts.items():
            probability = count / length
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        # Multiply by length to get total entropy
        return entropy * length

