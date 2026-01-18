"""
Unit tests for password strength evaluation system.

Tests cover:
- Pattern detection
- Entropy calculation
- Breach detection
- Scoring and classification
- Integration tests
"""

import unittest
from unittest.mock import Mock, patch

from evaluator import PasswordEvaluator
from patterns import PatternDetector
from entropy import EntropyCalculator
from breach import BreachChecker
from scorer import PasswordScorer


class TestPatternDetector(unittest.TestCase):
    """Test pattern detection functionality."""
    
    def setUp(self):
        self.detector = PatternDetector()
    
    def test_repeated_chars(self):
        """Test detection of repeated characters."""
        issues = self.detector.detect_all("aaaa")
        self.assertIn("repeated_chars", issues)
    
    def test_sequential_chars(self):
        """Test detection of sequential patterns."""
        issues = self.detector.detect_all("abcd1234")
        self.assertIn("sequential_chars", issues)
    
    def test_keyboard_pattern(self):
        """Test detection of keyboard patterns."""
        issues = self.detector.detect_all("qwerty")
        self.assertIn("keyboard_pattern", issues)
    
    def test_dictionary_word(self):
        """Test detection of dictionary words."""
        detector = PatternDetector({"password", "admin", "test"})
        issues = detector.detect_all("password123")
        self.assertIn("dictionary_word", issues)
    
    def test_year_pattern(self):
        """Test detection of year patterns."""
        issues = self.detector.detect_all("password2020")
        self.assertIn("year_pattern", issues)
    
    def test_username_similarity(self):
        """Test detection of username similarity."""
        issues = self.detector.detect_all("john123", username="john")
        self.assertIn("username_similarity", issues)
    
    def test_low_variety(self):
        """Test detection of low character variety."""
        issues = self.detector.detect_all("aaaaaaa")
        self.assertIn("low_variety", issues)


class TestEntropyCalculator(unittest.TestCase):
    """Test entropy calculation."""
    
    def test_empty_password(self):
        """Test entropy for empty password."""
        entropy, _ = EntropyCalculator.calculate_entropy("")
        self.assertEqual(entropy, 0.0)
    
    def test_simple_password(self):
        """Test entropy for simple password."""
        entropy, char_classes = EntropyCalculator.calculate_entropy("password")
        self.assertGreater(entropy, 0)
        self.assertTrue(char_classes["has_lower"])
    
    def test_complex_password(self):
        """Test entropy for complex password."""
        entropy, char_classes = EntropyCalculator.calculate_entropy("P@ssw0rd!")
        self.assertGreater(entropy, 0)
        self.assertTrue(char_classes["has_lower"])
        self.assertTrue(char_classes["has_upper"])
        self.assertTrue(char_classes["has_digit"])
        self.assertTrue(char_classes["has_special"])
    
    def test_pattern_penalty(self):
        """Test that patterns reduce entropy."""
        entropy_no_pattern, _ = EntropyCalculator.calculate_entropy("Random123!@#", False)
        entropy_with_pattern, _ = EntropyCalculator.calculate_entropy("Random123!@#", True)
        self.assertGreater(entropy_no_pattern, entropy_with_pattern)


class TestBreachChecker(unittest.TestCase):
    """Test breach detection."""
    
    def setUp(self):
        self.checker = BreachChecker()
    
    def test_empty_blacklist(self):
        """Test with empty blacklist."""
        is_breached, reason = self.checker.check_breach("randompassword123")
        # Should not be breached if not in blacklist
        self.assertFalse(is_breached)
    
    def test_blacklist_addition(self):
        """Test adding to blacklist."""
        self.checker.add_to_blacklist("testpassword")
        is_breached, reason = self.checker.check_breach("testpassword")
        self.assertTrue(is_breached)


class TestPasswordScorer(unittest.TestCase):
    """Test scoring functionality."""
    
    def test_breached_password(self):
        """Test that breached passwords get score 0."""
        score = PasswordScorer.calculate_score(
            entropy_bits=50.0,
            pattern_issues={},
            is_breached=True,
            length=12
        )
        self.assertEqual(score, 0)
    
    def test_strength_classification(self):
        """Test strength classification."""
        self.assertEqual(PasswordScorer.classify_strength(30), "Weak")
        self.assertEqual(PasswordScorer.classify_strength(50), "Medium")
        self.assertEqual(PasswordScorer.classify_strength(70), "Strong")
        self.assertEqual(PasswordScorer.classify_strength(90), "Very Strong")
    
    def test_recommendations(self):
        """Test recommendation generation."""
        recommendations = PasswordScorer.generate_recommendations(
            score=30,
            strength="Weak",
            entropy_bits=15.0,
            pattern_issues={"repeated_chars": ["test"]},
            is_breached=False,
            char_classes={"has_lower": True, "has_upper": False, "has_digit": False, "has_special": False},
            length=6
        )
        self.assertGreater(len(recommendations), 0)


class TestPasswordEvaluator(unittest.TestCase):
    """Integration tests for password evaluator."""
    
    def setUp(self):
        self.evaluator = PasswordEvaluator()
    
    def test_empty_password(self):
        """Test evaluation of empty password."""
        result = self.evaluator.evaluate("")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["strength"], "Weak")
    
    def test_weak_password(self):
        """Test evaluation of weak password."""
        result = self.evaluator.evaluate("password")
        self.assertLess(result["score"], 40)
        self.assertEqual(result["strength"], "Weak")
    
    def test_medium_password(self):
        """Test evaluation of medium password."""
        result = self.evaluator.evaluate("Password123")
        # Score may vary, but should be classified
        self.assertIn(result["strength"], ["Weak", "Medium", "Strong"])
    
    def test_strong_password(self):
        """Test evaluation of strong password."""
        result = self.evaluator.evaluate("Tr0ub4dor&3")
        # Should have reasonable score
        self.assertGreater(result["score"], 0)
    
    def test_very_strong_password(self):
        """Test evaluation of very strong password."""
        result = self.evaluator.evaluate("Xk9#mP2$vL7@nQ4&wR8!")
        # Long, complex password should score well
        self.assertGreaterEqual(result["score"], 60)
    
    def test_username_similarity(self):
        """Test username similarity detection."""
        result = self.evaluator.evaluate("john123", username="john")
        self.assertGreater(len(result["issues"]), 0)
    
    def test_email_similarity(self):
        """Test email similarity detection."""
        result = self.evaluator.evaluate("user123", email="user@example.com")
        self.assertGreater(len(result["issues"]), 0)
    
    def test_result_structure(self):
        """Test that result has all required fields."""
        result = self.evaluator.evaluate("testpassword")
        required_fields = ["score", "strength", "entropy_bits", "issues", "recommendations"]
        for field in required_fields:
            self.assertIn(field, result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def setUp(self):
        self.evaluator = PasswordEvaluator()
    
    def test_very_short_password(self):
        """Test very short password."""
        result = self.evaluator.evaluate("ab")
        self.assertEqual(result["strength"], "Weak")
    
    def test_very_long_password(self):
        """Test very long password."""
        long_pass = "a" * 100
        result = self.evaluator.evaluate(long_pass)
        # Should still detect patterns (repeated chars)
        self.assertGreater(len(result["issues"]), 0)
    
    def test_unicode_password(self):
        """Test password with unicode characters."""
        result = self.evaluator.evaluate("pässwörd123")
        # Should handle unicode gracefully
        self.assertIsInstance(result["score"], int)
    
    def test_special_characters_only(self):
        """Test password with only special characters."""
        result = self.evaluator.evaluate("!@#$%^&*()")
        # Should calculate entropy based on special char pool
        self.assertGreater(result["entropy_bits"], 0)


if __name__ == "__main__":
    unittest.main()

