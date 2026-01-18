#!/usr/bin/env python3
"""
Example usage of the password strength evaluation system.

Demonstrates various use cases and password evaluation scenarios.
"""

from evaluator import PasswordEvaluator


def print_evaluation(password: str, username: str = None, email: str = None):
    """Print formatted evaluation results."""
    evaluator = PasswordEvaluator()
    result = evaluator.evaluate(password, username, email)
    
    print(f"\n{'=' * 60}")
    print(f"Password: {'*' * len(password)}")
    if username:
        print(f"Username: {username}")
    if email:
        print(f"Email: {email}")
    print(f"{'=' * 60}")
    print(f"Score: {result['score']}/100")
    print(f"Strength: {result['strength']}")
    print(f"Entropy: {result['entropy_bits']} bits")
    print(f"Breached: {'Yes' if result['is_breached'] else 'No'}")
    if result['is_breached'] and result['breach_reason']:
        print(f"Breach Reason: {result['breach_reason']}")
    print(f"\nIssues:")
    for issue in result['issues']:
        print(f"  • {issue}")
    print(f"\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec}")
    print()


def main():
    """Run example evaluations."""
    print("Password Strength Evaluation System - Example Usage")
    print("=" * 60)
    
    # Example 1: Weak password
    print("\n[Example 1] Weak Password")
    print_evaluation("password123")
    
    # Example 2: Medium password
    print("\n[Example 2] Medium Password")
    print_evaluation("Password123")
    
    # Example 3: Strong password
    print("\n[Example 3] Strong Password")
    print_evaluation("Tr0ub4dor&3")
    
    # Example 4: Very strong password
    print("\n[Example 4] Very Strong Password")
    print_evaluation("Xk9#mP2$vL7@nQ4&wR8!")
    
    # Example 5: Password with patterns
    print("\n[Example 5] Password with Multiple Patterns")
    print_evaluation("qwerty1234")
    
    # Example 6: Username similarity
    print("\n[Example 6] Username Similarity Check")
    print_evaluation("johnsmith123", username="johnsmith")
    
    # Example 7: Email similarity
    print("\n[Example 7] Email Similarity Check")
    print_evaluation("user123", email="user@example.com")
    
    # Example 8: Dictionary word
    print("\n[Example 8] Dictionary Word")
    print_evaluation("welcome2024")
    
    # Example 9: Year pattern
    print("\n[Example 9] Year Pattern")
    print_evaluation("MyPassword2020")
    
    # Example 10: Leetspeak
    print("\n[Example 10] Leetspeak Substitution")
    print_evaluation("P@ssw0rd!")
    
    # Example 11: Repeated characters
    print("\n[Example 11] Repeated Characters")
    print_evaluation("aaaa1111")
    
    # Example 12: Sequential pattern
    print("\n[Example 12] Sequential Pattern")
    print_evaluation("abcdef123")
    
    # Example 13: Good password
    print("\n[Example 13] Good Password")
    print_evaluation("K7#mP9$vL2@nQ4&wR6!")
    
    print("\n" + "=" * 60)
    print("Examples complete!")


if __name__ == "__main__":
    main()

