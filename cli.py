#!/usr/bin/env python3
"""
Command-line interface for password strength evaluation.

Provides a simple CLI for testing and using the password evaluator.
"""

import argparse
import json
import sys
from pathlib import Path

from evaluator import PasswordEvaluator


def load_dictionary_words(wordlist_file: str) -> set:
    """Load dictionary words from file."""
    wordlist_path = Path(wordlist_file)
    if wordlist_path.exists():
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                return {line.strip().lower() for line in f if line.strip()}
        except Exception as e:
            print(f"Warning: Could not load wordlist: {e}", file=sys.stderr)
    return set()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Evaluate password strength using entropy, pattern detection, and breach intelligence"
    )
    parser.add_argument(
        "password",
        nargs="?",
        help="Password to evaluate (if not provided, will prompt)"
    )
    parser.add_argument(
        "--username",
        help="Username for similarity checking"
    )
    parser.add_argument(
        "--email",
        help="Email for similarity checking"
    )
    parser.add_argument(
        "--wordlist",
        default="data/common_words.txt",
        help="Path to dictionary wordlist file"
    )
    parser.add_argument(
        "--blacklist",
        default="data/top_10k_passwords.txt",
        help="Path to breach blacklist file"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    # Get password
    password = args.password
    if not password:
        import getpass
        password = getpass.getpass("Enter password to evaluate: ")
    
    if not password:
        print("Error: Password cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    # Load dictionary words
    dictionary_words = load_dictionary_words(args.wordlist)
    
    # Initialize evaluator
    evaluator = PasswordEvaluator(
        dictionary_words=dictionary_words,
        blacklist_file=args.blacklist
    )
    
    # Evaluate password
    result = evaluator.evaluate(
        password=password,
        username=args.username,
        email=args.email
    )
    
    # Output results
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\nPassword Strength Evaluation")
        print(f"{'=' * 50}")
        print(f"Score: {result['score']}/100")
        print(f"Strength: {result['strength']}")
        print(f"Entropy: {result['entropy_bits']} bits")
        print(f"\nIssues Detected:")
        for issue in result['issues']:
            print(f"  • {issue}")
        print(f"\nRecommendations:")
        for rec in result['recommendations']:
            print(f"  • {rec}")
        if result['is_breached']:
            print(f"\n⚠️  WARNING: This password has been compromised!")
        print()


if __name__ == "__main__":
    main()

