"""
Breach detection module for password strength evaluation.

Checks passwords against known breach databases to identify compromised passwords.
Uses local blacklist and optional Have I Been Pwned (HIBP) API with k-anonymity.

Security rationale: A password with high entropy is still weak if it's been
compromised in a breach. Attackers use breached password lists in credential
stuffing attacks. Breach detection is critical for production security.
"""

import hashlib
import os
from typing import Optional, Set, Tuple

from config import BREACH_CONFIG, DATA_DIR


class BreachChecker:
    """Checks passwords against breach databases."""
    
    def __init__(self, blacklist_file: Optional[str] = None):
        """
        Initialize breach checker.
        
        Args:
            blacklist_file: Path to local blacklist file. If None, uses default from config.
        """
        self.blacklist_file = blacklist_file or BREACH_CONFIG["local_blacklist_file"]
        self.blacklist: Set[str] = set()
        self._load_blacklist()
    
    def _load_blacklist(self):
        """Load local blacklist from file."""
        blacklist_path = os.path.join(DATA_DIR, os.path.basename(self.blacklist_file))
        
        # Try to load blacklist, but don't fail if file doesn't exist
        if os.path.exists(blacklist_path):
            try:
                with open(blacklist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    # Read all lines, strip whitespace, convert to lowercase
                    self.blacklist = {
                        line.strip().lower() 
                        for line in f 
                        if line.strip()
                    }
            except Exception as e:
                # Log error but continue without blacklist
                print(f"Warning: Could not load blacklist: {e}")
                self.blacklist = set()
        else:
            # File doesn't exist - will be created by setup script
            self.blacklist = set()
    
    def check_breach(self, password: str) -> Tuple[bool, Optional[str]]:
        """
        Check if password appears in breach databases.
        
        Args:
            password: Password to check
        
        Returns:
            Tuple of (is_breached, reason)
            is_breached: True if password is found in breaches
            reason: Human-readable reason for breach status
        """
        password_lower = password.lower()
        
        # Check local blacklist first (fastest)
        if password_lower in self.blacklist:
            return True, "Password found in common breach database (top 10k)"
        
        # Check HIBP API if enabled
        if BREACH_CONFIG["hibp_enabled"]:
            hibp_breached, hibp_reason = self._check_hibp(password)
            if hibp_breached:
                return True, hibp_reason
        
        return False, None
    
    def _check_hibp(self, password: str) -> Tuple[bool, Optional[str]]:
        """
        Check password against Have I Been Pwned API using k-anonymity.
        
        k-anonymity: Only send first 5 characters of SHA-1 hash to HIBP,
        then check full hash locally. This protects password privacy.
        
        Args:
            password: Password to check
        
        Returns:
            Tuple of (is_breached, reason)
        """
        try:
            import requests
            
            # Compute SHA-1 hash
            password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            hash_prefix = password_hash[:5]
            hash_suffix = password_hash[5:]
            
            # Query HIBP API with prefix only (k-anonymity)
            api_url = f"{BREACH_CONFIG['hibp_api_url']}{hash_prefix}"
            response = requests.get(api_url, timeout=5)
            
            if response.status_code == 200:
                # Check if our hash suffix appears in the response
                # Response format: SUFFIX:COUNT (one per line)
                for line in response.text.splitlines():
                    if ':' in line:
                        suffix, count = line.split(':', 1)
                        if suffix == hash_suffix:
                            return True, f"Password found in HIBP database ({count} breaches)"
            
            return False, None
            
        except ImportError:
            return False, "HIBP check requires 'requests' library"
        except Exception as e:
            # Network errors, API errors, etc. - fail open (don't block password)
            return False, f"HIBP check failed: {str(e)}"
    
    def add_to_blacklist(self, password: str):
        """
        Add password to local blacklist (for testing or custom blacklists).
        
        Args:
            password: Password to add
        """
        self.blacklist.add(password.lower())

