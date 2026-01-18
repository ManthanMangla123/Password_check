"""
Scoring module for password strength evaluation.

Converts entropy, pattern detection, and breach status into a unified score (0-100)
and strength classification (Weak/Medium/Strong/Very Strong).

Security rationale: Scoring provides a single metric for password strength while
preserving explainability. The score balances multiple factors:
- Base entropy (foundation of security)
- Pattern penalties (reduces score for predictability)
- Breach status (forces weak classification if compromised)
"""

from typing import Dict, List

from config import (
    SCORE_THRESHOLDS,
    PATTERN_PENALTIES,
    MIN_ENTROPY_BITS,
)


class PasswordScorer:
    """Scores passwords based on entropy, patterns, and breach status."""
    
    @staticmethod
    def calculate_score(
        entropy_bits: float,
        pattern_issues: Dict[str, List[str]],
        is_breached: bool,
        length: int
    ) -> int:
        """
        Calculate password strength score (0-100).
        
        Scoring algorithm:
        1. Start with entropy-based score (0-80 points)
        2. Apply pattern penalties (reduce score)
        3. Apply breach penalty (force to 0 if breached)
        4. Apply length bonus (small bonus for longer passwords)
        
        Args:
            entropy_bits: Calculated entropy in bits
            pattern_issues: Dictionary of detected pattern issues
            is_breached: Whether password is in breach database
            length: Password length
        
        Returns:
            Score from 0-100
        """
        # If breached, force weak score
        if is_breached:
            return 0
        
        # Base score from entropy (0-80 points)
        # Normalize entropy to 0-80 scale
        # Good entropy is 40+ bits, excellent is 60+ bits
        if entropy_bits <= 0:
            base_score = 0
        elif entropy_bits < 20:
            base_score = int((entropy_bits / 20) * 20)  # 0-20 points
        elif entropy_bits < 40:
            base_score = int(20 + ((entropy_bits - 20) / 20) * 30)  # 20-50 points
        elif entropy_bits < 60:
            base_score = int(50 + ((entropy_bits - 40) / 20) * 20)  # 50-70 points
        else:
            base_score = int(70 + min((entropy_bits - 60) / 20 * 10, 10))  # 70-80 points
        
        score = base_score
        
        # Apply pattern penalties
        for pattern_type, issues in pattern_issues.items():
            if issues:  # If any issues of this type detected
                penalty = PATTERN_PENALTIES.get(pattern_type, 0)
                # Apply penalty once per pattern type (not per issue)
                score -= penalty
        
        # Length bonus (small bonus for longer passwords, max +5 points)
        if length >= 16:
            score += 5
        elif length >= 12:
            score += 3
        elif length >= 8:
            score += 1
        
        # Ensure score is in valid range
        score = max(0, min(100, score))
        
        return int(score)
    
    @staticmethod
    def classify_strength(score: int) -> str:
        """
        Classify password strength based on score.
        
        Args:
            score: Password strength score (0-100)
        
        Returns:
            Strength classification: "Weak", "Medium", "Strong", or "Very Strong"
        """
        if score < SCORE_THRESHOLDS["WEAK"]:
            return "Weak"
        elif score < SCORE_THRESHOLDS["MEDIUM"]:
            return "Medium"
        elif score < SCORE_THRESHOLDS["STRONG"]:
            return "Strong"
        else:
            return "Very Strong"
    
    @staticmethod
    def generate_recommendations(
        score: int,
        strength: str,
        entropy_bits: float,
        pattern_issues: Dict[str, List[str]],
        is_breached: bool,
        char_classes: Dict[str, bool],
        length: int
    ) -> List[str]:
        """
        Generate actionable recommendations to improve password strength.
        
        Args:
            score: Current password score
            strength: Current strength classification
            entropy_bits: Calculated entropy
            pattern_issues: Detected pattern issues
            is_breached: Whether password is breached
            char_classes: Character class flags
            length: Password length
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if is_breached:
            recommendations.append("This password has been compromised in a data breach. Use a completely different password.")
            return recommendations
        
        if strength == "Weak":
            recommendations.append("Password is weak. Consider using a longer, more complex password.")
        
        if entropy_bits < MIN_ENTROPY_BITS:
            recommendations.append(f"Entropy is low ({entropy_bits:.1f} bits). Increase password complexity.")
        
        if length < 8:
            recommendations.append("Password is too short. Use at least 8 characters.")
        elif length < 12:
            recommendations.append("Consider using a longer password (12+ characters) for better security.")
        
        if not char_classes.get("has_lower"):
            recommendations.append("Add lowercase letters to increase character variety.")
        if not char_classes.get("has_upper"):
            recommendations.append("Add uppercase letters to increase character variety.")
        if not char_classes.get("has_digit"):
            recommendations.append("Add numbers to increase character variety.")
        if not char_classes.get("has_special"):
            recommendations.append("Add special characters to increase character variety.")
        
        # Pattern-specific recommendations
        if "repeated_chars" in pattern_issues:
            recommendations.append("Avoid repeating the same character multiple times.")
        if "sequential_chars" in pattern_issues:
            recommendations.append("Avoid sequential patterns (abc, 123, etc.).")
        if "keyboard_pattern" in pattern_issues:
            recommendations.append("Avoid keyboard patterns (qwerty, asdf, etc.).")
        if "dictionary_word" in pattern_issues:
            recommendations.append("Avoid common dictionary words. Use random or uncommon words.")
        if "year_pattern" in pattern_issues:
            recommendations.append("Avoid year patterns. Don't use birth years or common years.")
        if "username_similarity" in pattern_issues:
            recommendations.append("Don't use your username or email in your password.")
        if "leetspeak" in pattern_issues:
            recommendations.append("Leetspeak substitutions (p@ssw0rd) are predictable. Use truly random characters.")
        
        if not recommendations:
            recommendations.append("Password meets good security practices. Keep it secure and don't reuse it.")
        
        return recommendations

