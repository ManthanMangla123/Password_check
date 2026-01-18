# Quick Start Guide

## Web Server is Running! 🚀

The password evaluation web server has been started.

### Access the Web Interface

**Open your browser and navigate to:**
```
http://localhost:5001
```

**Note:** Port 5000 is often used by macOS AirPlay Receiver, so we use port 5001 instead.

### Features

- **Beautiful Web UI**: Modern, responsive interface
- **Real-time Evaluation**: Instant password strength analysis
- **Detailed Results**: Score, entropy, issues, and recommendations
- **Username/Email Checks**: Optional similarity detection
- **Breach Detection**: Checks against compromised password databases

### API Endpoint

You can also use the REST API directly:

```bash
curl -X POST http://localhost:5001/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"password": "your_password_here", "username": "optional", "email": "optional"}'
```

### Stop the Server

Press `Ctrl+C` in the terminal where the server is running, or:

```bash
pkill -f "python3 app.py"
```

### Restart the Server

```bash
python3 app.py
```

Or use the convenience script:
```bash
./run_server.sh
```

---

**Note**: The server runs on `http://localhost:5001` (port 5000 is often used by macOS AirPlay Receiver).

