"""
Main password strength evaluation engine.

Orchestrates pattern detection, entropy calculation, breach checking, and scoring
to provide a comprehensive password strength assessment with explainability.

This is the primary interface for password evaluation. It coordinates all
security modules to produce a unified, explainable result.
"""

from typing import Dict, List, Optional

from patterns import PatternDetector
from entropy import EntropyCalculator
from breach import BreachChecker
from scorer import PasswordScorer


class PasswordEvaluator:
    """Main password strength evaluation engine."""
    
    def __init__(self, dictionary_words: Optional[set] = None, blacklist_file: Optional[str] = None):
        """
        Initialize password evaluator.
        
        Args:
            dictionary_words: Set of dictionary words for pattern detection.
                             If None, dictionary checking is disabled.
            blacklist_file: Path to breach blacklist file. If None, uses default.
        """
        self.pattern_detector = PatternDetector(dictionary_words)
        self.entropy_calculator = EntropyCalculator()
        self.breach_checker = BreachChecker(blacklist_file)
        self.scorer = PasswordScorer()
    
    def evaluate(
        self,
        password: str,
        username: Optional[str] = None,
        email: Optional[str] = None
    ) -> Dict:
        """
        Evaluate password strength comprehensively.
        
        This is the main entry point for password evaluation. It:
        1. Detects weak patterns
        2. Calculates entropy
        3. Checks breach databases
        4. Computes score and classification
        5. Generates recommendations
        
        Args:
            password: Password to evaluate
            username: Optional username for similarity checks
            email: Optional email for similarity checks
        
        Returns:
            Dictionary with evaluation results:
            {
                "score": int (0-100),
                "strength": str ("Weak"|"Medium"|"Strong"|"Very Strong"),
                "entropy_bits": float,
                "issues": List[str],
                "recommendations": List[str],
                "is_breached": bool,
                "breach_reason": Optional[str]
            }
        """
        if not password:
            return {
                "score": 0,
                "strength": "Weak",
                "entropy_bits": 0.0,
                "issues": ["Password is empty"],
                "recommendations": ["Password cannot be empty"],
                "is_breached": False,
                "breach_reason": None,
            }
        
        # Step 1: Detect patterns
        pattern_issues = self.pattern_detector.detect_all(password, username, email)
        has_patterns = bool(pattern_issues)
        
        # Step 2: Calculate entropy
        entropy_bits, char_classes = self.entropy_calculator.calculate_entropy(
            password, has_patterns
        )
        
        # Step 3: Check breach databases
        is_breached, breach_reason = self.breach_checker.check_breach(password)
        
        # Step 4: Calculate score
        score = self.scorer.calculate_score(
            entropy_bits,
            pattern_issues,
            is_breached,
            len(password)
        )
        
        # Step 5: Classify strength
        strength = self.scorer.classify_strength(score)
        
        # Step 6: Generate recommendations
        recommendations = self.scorer.generate_recommendations(
            score,
            strength,
            entropy_bits,
            pattern_issues,
            is_breached,
            char_classes,
            len(password)
        )
        
        # Step 7: Format issues list
        issues = []
        for pattern_type, issue_list in pattern_issues.items():
            issues.extend(issue_list)
        
        if is_breached and breach_reason:
            issues.insert(0, breach_reason)
        
        if not issues:
            issues.append("No major issues detected")
        
        return {
            "score": score,
            "strength": strength,
            "entropy_bits": round(entropy_bits, 2),
            "issues": issues,
            "recommendations": recommendations,
            "is_breached": is_breached,
            "breach_reason": breach_reason,
        }

