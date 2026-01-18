Password Strength Evaluation System

A production-ready password strength evaluation system that classifies passwords as Weak / Medium / Strong / Very Strong using entropy calculation, human pattern detection, and breach intelligence — not naive rule-based checks.

Why This Project Exists

Most password strength checkers rely on fixed rules (minimum length, special characters, etc.) that are easily gamed and provide false confidence.

This project demonstrates how real-world password security should be evaluated: by combining entropy, predictability analysis, and breach intelligence, while remaining explainable, configurable, and suitable for production use.

Security Philosophy

This system is built around the following principles:

Entropy Over Rules
Security is measured by search space, not checkbox rules.

Human Pattern Awareness
Predictable human behaviors drastically reduce effective password strength.

Breach Intelligence First
A password is insecure if attackers already know it — regardless of complexity.

Explainability
Users must understand why a password is weak and how to improve it.

Configurability
No hard-coded magic numbers. All thresholds and penalties are adjustable.

Intended Use Cases

Backend password validation for authentication systems

Security tooling and internal audits

Developer education and training

Interview and portfolio demonstration of security engineering skills

Architecture

Modular, testable, and production-oriented design:

password_check/
├── config.py          # Centralized configuration and thresholds
├── patterns.py        # Pattern detection (repeats, sequences, keyboard, etc.)
├── entropy.py         # Shannon entropy calculation
├── breach.py          # Breach checking (local + optional HIBP)
├── scorer.py          # Scoring and strength classification
├── evaluator.py       # Main evaluation engine
├── cli.py             # Command-line interface
├── test_evaluator.py  # Unit tests
├── setup_data.py      # Data setup script
└── data/              # Wordlists and blacklists

Installation

Clone the repository

Set up data files

python setup_data.py


This creates:

data/common_words.txt — dictionary wordlist

data/top_10k_passwords.txt — breached password blacklist

Optional: Enable Have I Been Pwned (HIBP)

Install dependency: pip install requests

In config.py, enable:

BREACH_CONFIG["hibp_enabled"] = True


HIBP uses k-anonymity — only hash prefixes are transmitted.

Usage
Command-Line Interface
python cli.py "your_password_here"

python cli.py "password123" --username "john" --email "john@example.com"

python cli.py "password123" --json

Python API
from evaluator import PasswordEvaluator

evaluator = PasswordEvaluator()

result = evaluator.evaluate(
    password="your_password_here",
    username="optional_username",
    email="optional@email.com"
)


Returned structure:

{
  "score": 0-100,
  "strength": "Weak | Medium | Strong | Very Strong",
  "entropy_bits": 0.0,
  "issues": [],
  "recommendations": [],
  "is_breached": false,
  "breach_reason": null
}

How It Works
1. Pattern Detection

Identifies predictable structures that reduce effective security:

Repeated characters (aaaa, 1111)

Sequential patterns (abcd, 1234, descending included)

Keyboard patterns (qwerty, asdf, zxcv)

Leetspeak substitutions (p@ssw0rd)

Dictionary words

Year patterns (1900–2099)

Username/email similarity

Low character diversity

2. Entropy Calculation

Shannon entropy is computed as:

H = length × log₂(character_pool_size)


Character pool size is dynamic, based on actual character classes used:

Lowercase: 26

Uppercase: 26

Digits: 10

Special characters: 33

When predictable patterns are detected, entropy is penalized to reflect reduced effective strength.

3. Breach Detection

Local blacklist of commonly compromised passwords

Optional Have I Been Pwned API using privacy-preserving k-anonymity

If a password is breached → automatic Weak classification, regardless of entropy.

4. Scoring & Classification

Base score derived from entropy

Significant penalties applied for detected patterns

Minor bonuses for increased length

Final score clamped to 0–100

Strength mapping:

< 40 → Weak

40–60 → Medium

60–80 → Strong

≥ 80 → Very Strong

All thresholds are configurable.

Security Trade-offs and Design Decisions
Why Not Simple Rules?

Rule-based systems are predictable and easily bypassed. They do not model real attack costs.

Why Combine Entropy and Patterns?

Entropy measures theoretical strength; pattern detection models human predictability. Both are required for realistic evaluation.

Why Breach Checks Override Everything?

A password known to attackers is insecure by definition, regardless of complexity.

Why k-Anonymity?

It enables breach checking without exposing passwords or full hashes, preserving user privacy.

Why Explainability?

Security systems must guide users toward better behavior, not just reject input.

Configuration

All security behavior is defined in config.py:

Score thresholds

Pattern sensitivity

Penalty weights

Entropy multipliers

Breach detection settings

This allows adaptation to different threat models and environments.

Testing

Run all tests:

python -m unittest test_evaluator.py


Coverage includes:

Pattern detection logic

Entropy calculation

Breach handling

Scoring and classification

Edge cases and integration paths

Limitations and Future Enhancements
Current Limitations

English-focused dictionary

Rule-based pattern detection

Optional internet dependency for HIBP

Planned Enhancements

Multi-language dictionaries

Advanced pattern recognition

Password history checks

Context-aware policies (user vs admin)

Real-time feedback integration

License

MIT License — free for educational, personal, and commercial use.

Security Note

Passwords are never stored or transmitted.
All evaluation is local. When HIBP is enabled, only hash prefixes are sent using k-anonymity.
