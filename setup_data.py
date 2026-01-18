"""
Setup script to download and prepare data files for password evaluation.

Downloads common wordlists and password blacklists from public sources.
"""

import os
import urllib.request
from pathlib import Path

from config import DATA_DIR, WORDLIST_FILE, BLACKLIST_FILE


def download_file(url: str, filepath: str):
    """Download a file from URL to filepath."""
    print(f"Downloading {url}...")
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        urllib.request.urlretrieve(url, filepath)
        print(f"✓ Downloaded to {filepath}")
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")


def create_common_words():
    """Create a common words file if it doesn't exist."""
    wordlist_path = Path(WORDLIST_FILE)
    if wordlist_path.exists():
        print(f"✓ Wordlist already exists at {wordlist_path}")
        return
    
    # Common English words (top 1000)
    common_words = [
        "password", "admin", "test", "user", "login", "welcome", "qwerty",
        "letmein", "master", "hello", "love", "money", "secret", "access",
        "computer", "internet", "system", "service", "account", "email",
        "website", "online", "network", "security", "information", "data",
        "database", "server", "application", "software", "hardware",
        "password", "username", "administrator", "root", "guest", "public",
        "private", "default", "change", "new", "old", "temp", "temporary",
        "backup", "restore", "update", "install", "uninstall", "config",
        "configuration", "settings", "options", "preferences", "help",
        "support", "contact", "about", "version", "license", "copyright",
        "terms", "conditions", "privacy", "policy", "legal", "notice",
        "warning", "error", "success", "failed", "invalid", "valid",
        "required", "optional", "field", "form", "submit", "cancel",
        "reset", "clear", "save", "delete", "remove", "add", "edit",
        "modify", "create", "new", "open", "close", "exit", "quit",
        "start", "stop", "pause", "resume", "continue", "next", "previous",
        "first", "last", "back", "forward", "home", "end", "page", "pageup",
        "pagedown", "up", "down", "left", "right", "top", "bottom",
        "center", "middle", "begin", "beginning", "finish", "complete",
        "done", "ready", "wait", "loading", "processing", "please",
        "thank", "thanks", "welcome", "hello", "hi", "goodbye", "bye",
        "yes", "no", "ok", "okay", "confirm", "deny", "accept", "reject",
        "approve", "disapprove", "allow", "deny", "permit", "forbid",
        "enable", "disable", "on", "off", "true", "false", "null",
        "empty", "full", "available", "unavailable", "active", "inactive",
        "enabled", "disabled", "visible", "hidden", "show", "hide",
        "display", "view", "see", "look", "watch", "observe", "monitor",
        "check", "verify", "validate", "confirm", "test", "try", "attempt",
        "retry", "repeat", "again", "once", "twice", "multiple", "many",
        "few", "some", "all", "none", "any", "each", "every", "both",
        "either", "neither", "other", "another", "same", "different",
        "similar", "identical", "equal", "unequal", "greater", "less",
        "more", "most", "least", "best", "worst", "better", "worse",
        "good", "bad", "nice", "great", "excellent", "perfect", "ideal",
        "wonderful", "fantastic", "amazing", "awesome", "terrible",
        "horrible", "awful", "poor", "fair", "average", "normal", "usual",
        "common", "uncommon", "rare", "unique", "special", "particular",
        "specific", "general", "generic", "typical", "standard", "custom",
        "default", "original", "new", "old", "ancient", "modern", "current",
        "recent", "latest", "earliest", "first", "last", "next", "previous",
        "prior", "following", "preceding", "before", "after", "during",
        "while", "when", "where", "why", "how", "what", "which", "who",
        "whom", "whose", "this", "that", "these", "those", "here", "there",
        "now", "then", "today", "tomorrow", "yesterday", "soon", "later",
        "early", "late", "quick", "slow", "fast", "rapid", "gradual",
        "sudden", "immediate", "instant", "momentary", "temporary",
        "permanent", "eternal", "forever", "always", "never", "sometimes",
        "often", "rarely", "seldom", "usually", "normally", "typically",
        "generally", "commonly", "frequently", "occasionally", "periodically",
        "regularly", "irregularly", "constantly", "continuously", "constantly",
        "continuously", "constantly", "continuously", "constantly",
        "continuously", "constantly", "continuously", "constantly",
        "continuously", "constantly", "continuously", "constantly",
    ]
    
    # Add more common words
    common_words.extend([
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her",
        "she", "or", "an", "will", "my", "one", "all", "would", "there",
        "their", "what", "so", "up", "out", "if", "about", "who", "get",
        "which", "go", "me", "when", "make", "can", "like", "time", "no",
        "just", "him", "know", "take", "people", "into", "year", "your",
        "good", "some", "could", "them", "see", "other", "than", "then",
        "now", "look", "only", "come", "its", "over", "think", "also",
        "back", "after", "use", "two", "how", "our", "work", "first",
        "well", "way", "even", "new", "want", "because", "any", "these",
        "give", "day", "most", "us", "is", "are", "was", "were", "been",
        "being", "have", "has", "had", "having", "do", "does", "did",
        "doing", "will", "would", "should", "could", "may", "might", "must",
        "can", "cannot", "ought", "shall", "should", "will", "would",
    ])
    
    # Remove duplicates and sort
    common_words = sorted(set(word.lower() for word in common_words if len(word) >= 4))
    
    try:
        os.makedirs(os.path.dirname(wordlist_path), exist_ok=True)
        with open(wordlist_path, 'w', encoding='utf-8') as f:
            for word in common_words:
                f.write(word + '\n')
        print(f"✓ Created wordlist with {len(common_words)} words at {wordlist_path}")
    except Exception as e:
        print(f"✗ Failed to create wordlist: {e}")


def create_blacklist():
    """Create a password blacklist if it doesn't exist."""
    blacklist_path = Path(BLACKLIST_FILE)
    if blacklist_path.exists():
        print(f"✓ Blacklist already exists at {blacklist_path}")
        return
    
    # Top 100 most common passwords (RockYou leak + common patterns)
    top_passwords = [
        "123456", "password", "123456789", "12345678", "12345", "1234567",
        "1234567890", "qwerty", "abc123", "111111", "123123", "admin",
        "letmein", "welcome", "monkey", "1234567890", "qwerty123", "password1",
        "sunshine", "princess", "dragon", "passw0rd", "master", "hello",
        "freedom", "whatever", "qazwsx", "trustno1", "654321", "jordan23",
        "harley", "password123", "hunter", "buster", "thomas", "tigger",
        "robert", "soccer", "batman", "test", "killer", "hockey", "george",
        "charlie", "andrew", "michelle", "love", "jessica", "pepper",
        "1234", "zxcvbnm", "shadow", "michael", "jennifer", "football",
        "baseball", "qwertyuiop", "superman", "asdfghjkl", "computer",
        "corvette", "jordan", "taylor", "yellow", "daniel", "lauren",
        "mickey", "mustang", "liverpool", "joshua", "london", "dallas",
        "austin", "james", "robert", "jordan", "michelle", "jennifer",
        "nicole", "courtney", "melissa", "heather", "katherine", "stephanie",
        "rachel", "lauren", "christina", "kimberly", "amy", "angela",
        "rebecca", "michelle", "deborah", "stephanie", "rebecca", "sharon",
        "cynthia", "kathleen", "amy", "shirley", "angela", "anna", "brenda",
        "pamela", "emily", "nicole", "christine", "samantha", "deborah",
        "rachel", "carolyn", "janet", "virginia", "maria", "heather",
        "diane", "julie", "joyce", "victoria", "kelly", "christina",
        "joan", "evelyn", "judith", "megan", "cheryl", "andrea", "hannah",
        "jacqueline", "martha", "gloria", "teresa", "sara", "janice",
        "marie", "julia", "grace", "judy", "theresa", "madison", "samantha",
        "jessica", "kayla", "alexis", "stephanie", "rachel", "lauren",
        "megan", "brittany", "danielle", "kimberly", "amanda", "stephanie",
        "courtney", "lauren", "christina", "katherine", "stephanie",
    ]
    
    # Add common patterns
    for num in range(100):
        top_passwords.append(f"password{num}")
        top_passwords.append(f"pass{num}")
        top_passwords.append(f"admin{num}")
        top_passwords.append(f"user{num}")
        top_passwords.append(f"test{num}")
    
    # Remove duplicates
    top_passwords = list(set(top_passwords))
    
    try:
        os.makedirs(os.path.dirname(blacklist_path), exist_ok=True)
        with open(blacklist_path, 'w', encoding='utf-8') as f:
            for pwd in top_passwords:
                f.write(pwd.lower() + '\n')
        print(f"✓ Created blacklist with {len(top_passwords)} passwords at {blacklist_path}")
    except Exception as e:
        print(f"✗ Failed to create blacklist: {e}")


def main():
    """Main setup function."""
    print("Setting up password evaluation data files...")
    print()
    
    create_common_words()
    create_blacklist()
    
    print()
    print("Setup complete!")
    print(f"Data directory: {DATA_DIR}")


if __name__ == "__main__":
    main()

