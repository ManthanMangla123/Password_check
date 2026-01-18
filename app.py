#!/usr/bin/env python3
"""
Flask web application for password strength evaluation.

Provides a web interface and REST API for password strength evaluation.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

from evaluator import PasswordEvaluator
from cli import load_dictionary_words
from config import WORDLIST_FILE, BLACKLIST_FILE

app = Flask(__name__)
CORS(app)  # Enable CORS for API access

# Initialize evaluator
dictionary_words = load_dictionary_words(WORDLIST_FILE)
evaluator = PasswordEvaluator(
    dictionary_words=dictionary_words,
    blacklist_file=BLACKLIST_FILE
)


@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')


@app.route('/api/evaluate', methods=['POST'])
def evaluate_password():
    """
    API endpoint for password evaluation.
    
    Accepts JSON:
    {
        "password": "string",
        "username": "string (optional)",
        "email": "string (optional)"
    }
    
    Returns JSON with evaluation results.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        password = data.get('password', '')
        username = data.get('username')
        email = data.get('email')
        
        if not password:
            return jsonify({"error": "Password is required"}), 400
        
        # Evaluate password
        result = evaluator.evaluate(
            password=password,
            username=username,
            email=email
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "password-evaluator"}), 200


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("=" * 60)
    print("Password Strength Evaluation Server")
    print("=" * 60)
    print("Server starting on http://localhost:5001")
    print("Open your browser and navigate to: http://localhost:5001")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)

