"""
Pattern detection module for password strength evaluation.

Detects common weak patterns that reduce password security:
- Repeated characters
- Sequential patterns (alphabetical, numerical, descending)
- Keyboard patterns (qwerty, asdf, etc.)
- Leetspeak substitutions
- Dictionary words
- Year patterns
- Username/email similarity
- Low character variety

Security rationale: Pattern detection is crucial because entropy alone doesn't
capture predictability. A password with high entropy but obvious patterns is
vulnerable to pattern-based attacks.
"""

import re
import string
from typing import Dict, List, Set, Tuple, Optional
from difflib import SequenceMatcher

from config import (
    PATTERN_THRESHOLDS,
    PATTERN_PENALTIES,
    SIMILARITY_THRESHOLD,
    MIN_CHAR_VARIETY_RATIO,
)


class PatternDetector:
    """Detects weak patterns in passwords."""
    
    # Keyboard layout patterns (common rows and columns)
    KEYBOARD_ROWS = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
        "1234567890",
    ]
    
    # Leetspeak common substitutions
    LEETSPEAK_MAP = {
        'a': ['4', '@'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['7'],
        'l': ['1'],
        'z': ['2'],
    }
    
    def __init__(self, dictionary_words: Optional[Set[str]] = None):
        """
        Initialize pattern detector.
        
        Args:
            dictionary_words: Set of common dictionary words to check against.
                             If None, will use empty set (dictionary check disabled).
        """
        self.dictionary_words = dictionary_words or set()
        self._build_keyboard_patterns()
    
    def _build_keyboard_patterns(self):
        """Build forward and reverse keyboard patterns for detection."""
        self.keyboard_patterns = set()
        
        # Forward patterns
        for row in self.KEYBOARD_ROWS:
            for i in range(len(row) - PATTERN_THRESHOLDS["min_keyboard_pattern_length"] + 1):
                pattern = row[i:i + PATTERN_THRESHOLDS["min_keyboard_pattern_length"]]
                self.keyboard_patterns.add(pattern)
                self.keyboard_patterns.add(pattern.upper())
        
        # Reverse patterns
        for row in self.KEYBOARD_ROWS:
            reversed_row = row[::-1]
            for i in range(len(reversed_row) - PATTERN_THRESHOLDS["min_keyboard_pattern_length"] + 1):
                pattern = reversed_row[i:i + PATTERN_THRESHOLDS["min_keyboard_pattern_length"]]
                self.keyboard_patterns.add(pattern)
                self.keyboard_patterns.add(pattern.upper())
        
        # Column patterns (less common but still weak)
        for col_idx in range(10):
            col_pattern = ""
            for row in self.KEYBOARD_ROWS[:3]:  # Only letter rows
                if col_idx < len(row):
                    col_pattern += row[col_idx]
            if len(col_pattern) >= PATTERN_THRESHOLDS["min_keyboard_pattern_length"]:
                self.keyboard_patterns.add(col_pattern)
                self.keyboard_patterns.add(col_pattern.upper())
    
    def detect_all(self, password: str, username: Optional[str] = None, 
                   email: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Detect all patterns in password.
        
        Args:
            password: Password to analyze
            username: Optional username for similarity check
            email: Optional email for similarity check
        
        Returns:
            Dictionary mapping pattern type to list of detected issues
        """
        issues = {
            "repeated_chars": [],
            "sequential_chars": [],
            "keyboard_pattern": [],
            "leetspeak": [],
            "dictionary_word": [],
            "year_pattern": [],
            "username_similarity": [],
            "low_variety": [],
        }
        
        password_lower = password.lower()
        
        # Detect all pattern types
        issues["repeated_chars"] = self._detect_repeated_chars(password)
        issues["sequential_chars"] = self._detect_sequential_chars(password)
        issues["keyboard_pattern"] = self._detect_keyboard_patterns(password_lower)
        issues["leetspeak"] = self._detect_leetspeak(password_lower)
        issues["dictionary_word"] = self._detect_dictionary_words(password_lower)
        issues["year_pattern"] = self._detect_year_patterns(password)
        issues["username_similarity"] = self._detect_username_similarity(
            password, username, email
        )
        issues["low_variety"] = self._detect_low_variety(password)
        
        # Remove empty lists
        return {k: v for k, v in issues.items() if v}
    
    def _detect_repeated_chars(self, password: str) -> List[str]:
        """Detect consecutive repeated characters."""
        issues = []
        min_repeat = PATTERN_THRESHOLDS["min_repeat_length"]
        
        i = 0
        while i < len(password):
            char = password[i]
            count = 1
            j = i + 1
            while j < len(password) and password[j] == char:
                count += 1
                j += 1
            
            if count >= min_repeat:
                issues.append(f"Repeated character '{char}' {count} times")
            
            i = j
        
        return issues
    
    def _detect_sequential_chars(self, password: str) -> List[str]:
        """Detect sequential character patterns (alphabetical, numerical, descending)."""
        issues = []
        min_seq = PATTERN_THRESHOLDS["min_sequence_length"]
        
        # Check for sequences in sliding windows
        for i in range(len(password) - min_seq + 1):
            window = password[i:i + min_seq]
            
            # Check ascending alphabetical
            if self._is_ascending_alpha(window):
                issues.append(f"Sequential pattern: '{window}' (ascending)")
                continue
            
            # Check descending alphabetical
            if self._is_descending_alpha(window):
                issues.append(f"Sequential pattern: '{window}' (descending)")
                continue
            
            # Check ascending numerical
            if self._is_ascending_numeric(window):
                issues.append(f"Sequential pattern: '{window}' (numerical)")
                continue
            
            # Check descending numerical
            if self._is_descending_numeric(window):
                issues.append(f"Sequential pattern: '{window}' (numerical descending)")
        
        return issues
    
    def _is_ascending_alpha(self, s: str) -> bool:
        """Check if string is ascending alphabetical sequence."""
        if not s.isalpha():
            return False
        s_lower = s.lower()
        for i in range(len(s_lower) - 1):
            if ord(s_lower[i + 1]) != ord(s_lower[i]) + 1:
                return False
        return True
    
    def _is_descending_alpha(self, s: str) -> bool:
        """Check if string is descending alphabetical sequence."""
        if not s.isalpha():
            return False
        s_lower = s.lower()
        for i in range(len(s_lower) - 1):
            if ord(s_lower[i + 1]) != ord(s_lower[i]) - 1:
                return False
        return True
    
    def _is_ascending_numeric(self, s: str) -> bool:
        """Check if string is ascending numerical sequence."""
        if not s.isdigit():
            return False
        for i in range(len(s) - 1):
            if int(s[i + 1]) != (int(s[i]) + 1) % 10:  # Handle wrap-around (9->0)
                return False
        return True
    
    def _is_descending_numeric(self, s: str) -> bool:
        """Check if string is descending numerical sequence."""
        if not s.isdigit():
            return False
        for i in range(len(s) - 1):
            if int(s[i + 1]) != (int(s[i]) - 1) % 10:  # Handle wrap-around (0->9)
                return False
        return True
    
    def _detect_keyboard_patterns(self, password_lower: str) -> List[str]:
        """Detect keyboard layout patterns."""
        issues = []
        min_len = PATTERN_THRESHOLDS["min_keyboard_pattern_length"]
        
        for i in range(len(password_lower) - min_len + 1):
            window = password_lower[i:i + min_len]
            if window in self.keyboard_patterns:
                issues.append(f"Keyboard pattern detected: '{window}'")
        
        return issues
    
    def _detect_leetspeak(self, password_lower: str) -> List[str]:
        """Detect leetspeak substitutions."""
        issues = []
        
        # Check for common leetspeak patterns
        leet_patterns = [
            (r'[a@]dm[i1]n', 'admin'),
            (r'p[@a]ssw[o0]rd', 'password'),
            (r'[l1]0v3', 'love'),
            (r'[h4]ack', 'hack'),
            (r'[t7]est', 'test'),
        ]
        
        for pattern, word in leet_patterns:
            if re.search(pattern, password_lower):
                issues.append(f"Leetspeak substitution detected (resembles '{word}')")
        
        # General leetspeak detection: check if password has high ratio of digit/special
        # substitutions that match common leetspeak patterns
        leet_count = 0
        for char in password_lower:
            for original, substitutions in self.LEETSPEAK_MAP.items():
                if char in substitutions:
                    leet_count += 1
                    break
        
        if len(password_lower) > 0 and leet_count / len(password_lower) > 0.3:
            issues.append("High leetspeak substitution ratio detected")
        
        return issues
    
    def _detect_dictionary_words(self, password_lower: str) -> List[str]:
        """Detect dictionary words in password."""
        issues = []
        
        if not self.dictionary_words:
            return issues
        
        min_word_len = PATTERN_THRESHOLDS["min_dictionary_word_length"]
        
        # Check if entire password is a dictionary word
        if len(password_lower) >= min_word_len and password_lower in self.dictionary_words:
            issues.append(f"Password is a common dictionary word: '{password_lower}'")
        
        # Check for dictionary words as substrings
        for word in self.dictionary_words:
            if len(word) >= min_word_len and word in password_lower:
                # Avoid duplicate issues
                if word not in [issue.split("'")[1] for issue in issues if "'" in issue]:
                    issues.append(f"Contains dictionary word: '{word}'")
        
        return issues
    
    def _detect_year_patterns(self, password: str) -> List[str]:
        """Detect year patterns (1900-2099)."""
        issues = []
        min_year, max_year = PATTERN_THRESHOLDS["max_year_range"]
        
        # Match 4-digit years
        year_pattern = r'\d{4}'
        matches = re.finditer(year_pattern, password)
        
        for match in matches:
            year_str = match.group()
            try:
                year = int(year_str)
                if min_year <= year <= max_year:
                    issues.append(f"Year pattern detected: '{year_str}'")
            except ValueError:
                continue
        
        return issues
    
    def _detect_username_similarity(self, password: str, username: Optional[str], 
                                   email: Optional[str]) -> List[str]:
        """Detect similarity to username or email."""
        issues = []
        
        if not username and not email:
            return issues
        
        password_lower = password.lower()
        
        # Check username similarity
        if username:
            username_lower = username.lower()
            
            # Check if username is substring of password
            if username_lower in password_lower:
                issues.append(f"Password contains username: '{username}'")
            
            # Check similarity ratio
            similarity = SequenceMatcher(None, password_lower, username_lower).ratio()
            if similarity >= SIMILARITY_THRESHOLD:
                issues.append(f"Password too similar to username (similarity: {similarity:.2f})")
        
        # Check email similarity
        if email:
            email_lower = email.lower()
            # Extract local part (before @)
            email_local = email_lower.split('@')[0] if '@' in email_lower else email_lower
            
            # Check if email local part is substring of password
            if email_local in password_lower:
                issues.append(f"Password contains email username: '{email_local}'")
            
            # Check similarity ratio
            similarity = SequenceMatcher(None, password_lower, email_local).ratio()
            if similarity >= SIMILARITY_THRESHOLD:
                issues.append(f"Password too similar to email (similarity: {similarity:.2f})")
        
        return issues
    
    def _detect_low_variety(self, password: str) -> List[str]:
        """Detect low character variety (too many repeated unique characters)."""
        issues = []
        
        if len(password) == 0:
            return issues
        
        unique_chars = len(set(password))
        variety_ratio = unique_chars / len(password)
        
        if variety_ratio < MIN_CHAR_VARIETY_RATIO:
            issues.append(
                f"Low character variety: {unique_chars} unique characters "
                f"out of {len(password)} (ratio: {variety_ratio:.2f})"
            )
        
        return issues

