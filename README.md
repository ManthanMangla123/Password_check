# 🔒 Password Strength Evaluation System

> A production-ready password strength evaluation system that classifies passwords as **Weak / Medium / Strong / Very Strong** using entropy calculation, human pattern detection, and breach intelligence — not naive rule-based checks.

---

## 📋 Table of Contents

- [Why This Project Exists](#why-this-project-exists)
- [Security Philosophy](#security-philosophy)
- [Intended Use Cases](#intended-use-cases)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Security Trade-offs](#security-trade-offs-and-design-decisions)
- [Configuration](#configuration)
- [Testing](#testing)
- [Limitations & Future Enhancements](#limitations-and-future-enhancements)

---

## 🎯 Why This Project Exists

Most password strength checkers rely on fixed rules (minimum length, special characters, etc.) that are easily gamed and provide false confidence.

This project demonstrates how real-world password security should be evaluated: by combining entropy, predictability analysis, and breach intelligence, while remaining explainable, configurable, and suitable for production use.

---

## 🛡️ Security Philosophy

This system is built around the following principles:

### **Entropy Over Rules**
Security is measured by search space, not checkbox rules.

### **Human Pattern Awareness**
Predictable human behaviors drastically reduce effective password strength.

### **Breach Intelligence First**
A password is insecure if attackers already know it — regardless of complexity.

### **Explainability**
Users must understand why a password is weak and how to improve it.

### **Configurability**
No hard-coded magic numbers. All thresholds and penalties are adjustable.

---

## 💼 Intended Use Cases

- **Backend password validation** for authentication systems
- **Security tooling** and internal audits
- **Developer education** and training
- **Interview and portfolio** demonstration of security engineering skills

---

## 🏗️ Architecture

Modular, testable, and production-oriented design:

```
password_check/
├── config.py          # Centralized configuration and thresholds
├── patterns.py        # Pattern detection (repeats, sequences, keyboard, etc.)
├── entropy.py         # Shannon entropy calculation
├── breach.py          # Breach checking (local + optional HIBP)
├── scorer.py          # Scoring and strength classification
├── evaluator.py       # Main evaluation engine
├── cli.py             # Command-line interface
├── app.py             # Flask web application
├── test_evaluator.py  # Unit tests
├── setup_data.py      # Data setup script
└── data/              # Wordlists and blacklists
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ManthanMangla123/Password_check.git
cd Password_check
```

### 2. Ensure Python Version

Python 3.8+ is recommended.

```bash
python --version
```

### 3. Set Up Required Data Files

Run the setup script once:

```bash
python setup_data.py
```

This creates:
- `data/common_words.txt` — dictionary wordlist for pattern detection
- `data/top_10k_passwords.txt` — breached password blacklist

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Optional: Enable Breach Intelligence via Have I Been Pwned

Install dependency:

```bash
pip install requests
```

Edit `config.py`:

```python
BREACH_CONFIG["hibp_enabled"] = True
```

> **Privacy Note:** HIBP uses k-anonymity — only hash prefixes are transmitted. Passwords and full hashes are never sent.

### 6. Run the Web Server

```bash
python app.py
```

Open your browser and navigate to: `http://localhost:5001`

---

## 📖 Usage

### Command-Line Interface

**Basic usage:**

```bash
python cli.py "your_password_here"
```

**With username and email similarity checks:**

```bash
python cli.py "password123" --username "john" --email "john@example.com"
```

**JSON output:**

```bash
python cli.py "password123" --json
```

### Python API Usage

```python
from evaluator import PasswordEvaluator

evaluator = PasswordEvaluator()

result = evaluator.evaluate(
    password="your_password_here",
    username="optional_username",
    email="optional@email.com"
)
```

**Returned structure:**

```json
{
  "score": 0-100,
  "strength": "Weak | Medium | Strong | Very Strong",
  "entropy_bits": 0.0,
  "issues": [],
  "recommendations": [],
  "is_breached": false,
  "breach_reason": null
}
```

### Web Interface

Start the Flask server:

```bash
python app.py
```

Access the web interface at `http://localhost:5001` for an interactive password evaluation experience.

---

## ⚙️ How It Works

### 1. Pattern Detection

Identifies predictable structures that reduce effective security:

- **Repeated characters** (aaaa, 1111)
- **Sequential patterns** (abcd, 1234, descending included)
- **Keyboard patterns** (qwerty, asdf, zxcv)
- **Leetspeak substitutions** (p@ssw0rd)
- **Dictionary words**
- **Year patterns** (1900–2099)
- **Username/email similarity**
- **Low character diversity**

### 2. Entropy Calculation

**Shannon entropy:**

```
H = length × log₂(character_pool_size)
```

**Character pool size is dynamic:**

- Lowercase: 26
- Uppercase: 26
- Digits: 10
- Special characters: 33

Detected patterns reduce effective entropy.

### 3. Breach Detection

- **Local blacklist** of commonly compromised passwords
- **Optional Have I Been Pwned API** using privacy-preserving k-anonymity

> If a password is breached → automatic **Weak** classification.

### 4. Scoring & Classification

- Base score derived from entropy
- Significant penalties for detected patterns
- Minor bonuses for increased length
- Final score clamped to 0–100

**Strength mapping:**

| Score Range | Classification |
|-------------|----------------|
| < 40        | Weak           |
| 40–60       | Medium         |
| 60–80       | Strong         |
| ≥ 80        | Very Strong    |

All thresholds are configurable.

---

## 🔐 Security Trade-offs and Design Decisions

### **Why Not Simple Rules?**
Rule-based systems are predictable and easily bypassed.

### **Why Combine Entropy and Patterns?**
Entropy measures theoretical strength; pattern detection models human predictability.

### **Why Breach Checks Override Everything?**
A password known to attackers is insecure by definition.

### **Why k-Anonymity?**
It enables breach checking without exposing passwords or hashes.

### **Why Explainability?**
Security systems should guide users toward better behavior.

---

## ⚙️ Configuration

All security behavior is defined in `config.py`:

- Score thresholds
- Pattern sensitivity
- Penalty weights
- Entropy multipliers
- Breach detection settings

---

## 🧪 Testing

Run all tests:

```bash
python -m unittest test_evaluator.py
```

**Coverage includes:**

- Pattern detection logic
- Entropy calculation
- Breach handling
- Scoring and classification
- Edge cases and integration paths

---

## 🔮 Limitations and Future Enhancements

### Current Limitations

- English-focused dictionary
- Rule-based pattern detection
- Optional internet dependency for HIBP

### Planned Enhancements

- Multi-language dictionaries
- Advanced pattern recognition
- Password history checks
- Context-aware policies (user vs admin)
- Real-time feedback integration

---

## 📄 License

MIT License — free for educational, personal, and commercial use.

---

## 🔒 Security Note

> **Important:** Passwords are never stored or transmitted.  
> All evaluation is local.  
> When HIBP is enabled, only hash prefixes are sent using k-anonymity.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ for better password security**
