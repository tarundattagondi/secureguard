# 🛡️ SecureGuard — Security Compliance Dashboard

[![CI/CD Pipeline](https://github.com/tarundattagondi/secureguard/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/tarundattagondi/secureguard/actions)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-green.svg)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Test Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen.svg)]()

A full-stack **Governance, Risk, and Compliance (GRC)** dashboard that maps security controls to **NIST CSF** and **ISO 27001** frameworks, tracks organizational risks, monitors automated security scan results, and manages vendor security reviews. Built with a complete **DevOps pipeline** including CI/CD, automated security scanning (SAST, dependency scanning, container scanning), Docker containerization, and AWS deployment.

---

## 📸 Screenshots

### Dashboard
Real-time compliance score, open risk count, vulnerability findings, vendor review status, control breakdown chart, and recent risk activity feed.

![Dashboard](docs/screenshots/dashboard.png)

### Compliance Controls
33 NIST CSF controls across Identify, Protect, Detect, Respond, and Recover categories with inline status updates and filtering.

![Controls](docs/screenshots/controls.png)

### Risk Register
Add, track, and manage security risks with auto-calculated risk scores (Likelihood × Impact), color-coded severity, status filtering, and NIST control mapping.

![Risk Register](docs/screenshots/risk-register.png)

### Security Scan Results
Vulnerability trend charts, severity breakdown (Critical/High/Medium/Low), and historical scan data from Bandit, Safety, and Trivy pipeline scans.

![Scan Results](docs/screenshots/scan-results.png)

### CI/CD Pipeline
Automated 6-stage pipeline running on every push — lint, tests, SAST, dependency scan, Docker build + Trivy container scan, and pipeline summary.

![CI/CD Pipeline](docs/screenshots/ci-cd-pipeline.png)

### AWS Deployment
Deployed to AWS EC2 with Docker Compose (Flask + PostgreSQL + Nginx) and security group configuration.

![AWS Deployment](docs/screenshots/aws-deployment.png)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   GitHub Repository                  │
│   Push code → Triggers GitHub Actions CI/CD Pipeline │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│            GitHub Actions CI/CD Pipeline              │
│                                                       │
│  Stage 1: Lint (flake8)                               │
│  Stage 2: Unit Tests (pytest, 45 tests, 95% coverage)│
│  Stage 3: SAST Scan (Bandit - Python security issues) │
│  Stage 4: Dependency Scan (pip-audit - known CVEs)    │
│  Stage 5: Docker Build + Container Scan (Trivy)       │
│  Stage 6: Pipeline Summary                            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Production (AWS EC2)                     │
│                                                       │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────┐ │
│  │  Nginx   │──▶│  Flask App   │──▶│  PostgreSQL  │ │
│  │ (Reverse │   │  (Gunicorn)  │   │  (Database)  │ │
│  │  Proxy)  │   │  Port 5001   │   │  Port 5432   │ │
│  │ Port 80  │   └──────────────┘   └──────────────┘ │
│  └──────────┘                                        │
│          All running in Docker Compose                │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python, Flask, SQLAlchemy | REST API and server-side rendering |
| **Frontend** | Jinja2, Chart.js, CSS | Dashboard UI with interactive charts |
| **Database** | PostgreSQL | Persistent storage for controls, risks, scans, vendors |
| **Containerization** | Docker, Docker Compose | Multi-container deployment (Flask + Postgres + Nginx) |
| **Reverse Proxy** | Nginx | Production-grade HTTP server and load balancing |
| **WSGI Server** | Gunicorn | Production Python application server |
| **CI/CD** | GitHub Actions | Automated testing and deployment pipeline |
| **SAST** | Bandit | Static Application Security Testing for Python |
| **Dependency Scan** | pip-audit | Checks installed packages for known CVEs |
| **Container Scan** | Trivy | Scans Docker images for OS and library vulnerabilities |
| **Linting** | flake8 | Python code style and syntax checking |
| **Testing** | pytest, pytest-cov | Unit tests with 95% code coverage |
| **Cloud** | AWS EC2 | Production deployment with security groups and IAM |

---

## 🚀 Features

### Compliance Control Tracker
- 33 pre-seeded **NIST CSF** controls across all 5 functions (Identify, Protect, Detect, Respond, Recover)
- Inline status updates: Implemented, Partially Implemented, Not Implemented, Not Applicable
- Filter by status, framework, and category
- Track control owner and evidence links

### Risk Register
- Create and manage security risks with title, description, likelihood (1-5), and impact (1-5)
- **Auto-calculated risk score** (Likelihood × Impact) with color-coded severity:
  - 🔴 Critical (20-25) | 🟠 High (12-19) | 🟡 Medium (6-11) | 🟢 Low (1-5)
- Map risks to specific NIST controls
- Filter by status: Open, In Progress, Mitigated, Accepted

### Automated Security Scan Results
- Stores results from **Bandit** (SAST), **pip-audit** (dependency), and **Trivy** (container) scans
- **Vulnerability trend chart** showing Critical/High/Medium/Low findings over last 10 pipeline runs
- Severity breakdown summary cards
- Full scan history with pipeline run IDs

### Vendor Security Tracker
- Track third-party vendors with risk ratings and questionnaire status
- Monitor SOC 2 report dates and expiry
- Vendor statuses: Not Sent, Sent, In Review, Approved, Rejected

### CI/CD Pipeline (6 Stages)
- **Lint** — flake8 code style checking
- **Unit Tests** — 45 tests with 95% coverage via pytest
- **SAST** — Bandit scans Python code for security vulnerabilities
- **Dependency Scan** — pip-audit checks for known CVEs in packages
- **Docker Build + Trivy** — Builds container and scans for image vulnerabilities
- **Pipeline Summary** — Reports pass/fail for all stages

---

## 📁 Project Structure

```
secureguard/
├── .github/workflows/
│   └── ci-cd.yml                  # GitHub Actions 6-stage pipeline
├── app/
│   ├── __init__.py                # Flask app factory with extensions
│   ├── models.py                  # SQLAlchemy models (Controls, Risks, Scans, Vendors)
│   ├── routes/
│   │   ├── dashboard.py           # Dashboard with real-time metrics
│   │   ├── controls.py            # NIST/ISO control CRUD + filtering
│   │   ├── risks.py               # Risk register with score calculation
│   │   └── scans.py               # Scan results with trend data
│   ├── templates/                 # Jinja2 HTML templates
│   └── static/css/                # Styled dark theme CSS
├── scripts/
│   └── seed_controls.py           # Seeds 33 NIST controls + sample data
├── tests/
│   ├── conftest.py                # pytest fixtures (in-memory SQLite)
│   ├── test_models.py             # Model creation and validation tests
│   ├── test_routes.py             # Route and endpoint tests
│   └── test_risk_calculator.py    # Risk score calculation tests
├── Dockerfile                     # Python 3.11 slim container
├── docker-compose.yml             # Flask + PostgreSQL + Nginx stack
├── docker-entrypoint.sh           # Auto-migrate and seed on startup
├── nginx.conf                     # Reverse proxy configuration
├── config.py                      # App configuration with env vars
├── .flake8                        # Linter configuration
├── .bandit.yml                    # SAST scan configuration
├── pytest.ini                     # Test runner configuration
└── requirements.txt               # Python dependencies
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (or use Docker)

### Option 1: Run with Docker (Recommended)

```bash
git clone https://github.com/tarundattagondi/secureguard.git
cd secureguard
docker compose up --build -d
```

Open `http://localhost` (Nginx) or `http://localhost:5001` (direct Flask).

### Option 2: Run Locally

```bash
git clone https://github.com/tarundattagondi/secureguard.git
cd secureguard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set up database
export FLASK_APP=run.py
export DATABASE_URL=postgresql://user:password@localhost:5432/secureguard_db
flask db upgrade
python scripts/seed_controls.py

# Run
python run.py
```

Open `http://127.0.0.1:5001`.

### Run Tests

```bash
pytest                                    # Run all 45 tests
pytest --cov=app --cov-report=term-missing  # With coverage report
```

---

## 🔒 Security Scanning

Every push triggers automated security scans in the CI/CD pipeline:

| Scanner | Type | What It Finds |
|---------|------|--------------|
| **Bandit** | SAST | Hardcoded passwords, SQL injection, insecure functions, weak crypto |
| **pip-audit** | Dependency | Known CVEs in installed Python packages (checks PyPI advisory DB) |
| **Trivy** | Container | OS vulnerabilities, library CVEs, misconfigurations in Docker image |
| **flake8** | Linting | Code style violations, syntax errors, unused imports |

Scan reports are uploaded as **GitHub Actions artifacts** after each pipeline run.

---

## 🗄️ Database Schema

### ComplianceControl
| Field | Type | Description |
|-------|------|-------------|
| control_id | String(20) | NIST CSF ID (e.g., "PR.AC-4") |
| framework | String(20) | "NIST CSF" or "ISO 27001" |
| category | String(100) | Identify, Protect, Detect, Respond, Recover |
| status | String(30) | Implemented / Partially / Not Implemented / N/A |
| owner | String(100) | Responsible team or individual |

### Risk
| Field | Type | Description |
|-------|------|-------------|
| title | String(200) | Risk title |
| likelihood | Integer | 1-5 scale |
| impact | Integer | 1-5 scale |
| risk_score | Integer | Auto-calculated (likelihood × impact) |
| status | String(30) | Open / In Progress / Mitigated / Accepted |
| related_control | String(20) | Maps to NIST control ID |

### ScanResult
| Field | Type | Description |
|-------|------|-------------|
| scan_type | String(50) | Bandit, Safety, or Trivy |
| critical/high/medium/low_count | Integer | Findings by severity |
| pipeline_run_id | String(100) | Links to CI/CD run |

### Vendor
| Field | Type | Description |
|-------|------|-------------|
| name | String(200) | Vendor company name |
| risk_rating | String(20) | Critical / High / Medium / Low / Not Assessed |
| questionnaire_status | String(30) | Not Sent / Sent / In Review / Approved / Rejected |
| soc2_expiry_date | DateTime | SOC 2 report expiration |

---

## 🌐 AWS Deployment

Deployed to **AWS EC2** (t2.micro, Ubuntu 24.04) with:
- **Docker Compose** running Flask + PostgreSQL + Nginx containers
- **Security Groups** configured with:
  - SSH (port 22) restricted to admin IP only
  - HTTP (port 80) open for web access
  - Custom TCP (port 5001) for direct Flask access
- **Gunicorn** WSGI server with 3 workers for production performance
- **Nginx** reverse proxy handling HTTP traffic and static files

---

## 🧪 Test Coverage

```
Name                          Stmts   Miss  Cover
--------------------------------------------------
app/__init__.py                  20      0   100%
app/models.py                    63      3    95%
app/routes/__init__.py            0      0   100%
app/routes/controls.py           23      0   100%
app/routes/dashboard.py          15      0   100%
app/routes/risks.py              27      5    81%
app/routes/scans.py               8      0   100%
--------------------------------------------------
TOTAL                           156      8    95%

45 tests passed
```

---

## 📊 CI/CD Pipeline Stages

```
Code Linting (9s)
    │
    ├── Unit Tests (20s)
    ├── SAST - Bandit Scan (9s)
    └── Dependency Vulnerability Scan (20s)
            │
            └── Build & Scan Docker Image (51s)
                    │
                    └── Pipeline Summary (2s)
```

All stages must pass before the Docker image is built. Security scan reports are saved as pipeline artifacts.

---

## 🔧 Configuration

Environment variables (set in `.env` or Docker Compose):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `sqlite:///secureguard.db` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `FLASK_APP` | Flask application entry point | `run.py` |

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Tarun Datta Gondi**
- MS Computer Science, George Mason University
