#!/usr/bin/env python3
"""
Start the password evaluation web server.
Run this script to start the server in the foreground.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print(" " * 15 + "🔒 Password Strength Evaluation Server")
    print("=" * 70)
    print("\n✓ Server is starting...")
    print("✓ Open your browser and navigate to: http://localhost:5000")
    print("✓ Press Ctrl+C to stop the server\n")
    print("=" * 70 + "\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")
        sys.exit(1)

