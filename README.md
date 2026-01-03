# 🥗 Gourmet Vault (Full-Stack & Serverless)

A comprehensive Recipe Management System featuring a dual-architecture design: a Serverless Frontend that runs entirely in the browser using LocalStorage, and a complete Python/Flask Backend for robust API development and testing.

## 🌟 Project Overview

This repository demonstrates a full software development lifecycle, including:

**Frontend:** A Serverless Single-Page Application (SPA) deployable to Netlify/GitHub Pages.

**Backend:** A RESTful Flask API with SQLAlchemy and SQLite.

**DevOps:** PowerShell automation for deployment and health checks.

**Quality:** Unit testing with Pytest and static analysis configs for SonarQube.

## 🚀 Key Features

### Frontend (Serverless Mode)

- **Zero Config:** Runs instantly in the browser using LocalStorage.
- **Smart Search:** Filter by cuisine, difficulty, or text.
- **Responsive:** Mobile-first design.
- **CRUD:** Create, read, update, delete recipes locally.

### Backend (Python/Flask)

- **REST API:** Fully functional endpoints for recipe management.
- **Database:** SQLite integration with SQLAlchemy ORM.
- **Validation:** Input sanitization and error handling.
- **Testing:** Comprehensive test suite with high code coverage.

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Backend:** Python 3.10+, Flask, SQLAlchemy
- **Automation:** PowerShell 5.1+
- **Testing & Quality:** Pytest, SonarQube, Pylint

## 📂 Project Structure

```
/
├── index.html                  # Serverless Frontend (Single File App)
├── app.py                      # Flask Backend API (REST endpoints & DB models)
├── test_app.py                 # Unit Test Suite (Pytest)
├── automation-scripts.ps1      # DevOps Automation (Setup, Backup, Health Checks)
├── requirements.txt            # Python Dependencies
├── sonar-project.properties    # SonarQube Configuration
├── README.md                   # Project Documentation
└── .gitignore                  # Git ignore rules
```

## 💻 How to Run

### 1. Run Frontend (Serverless)

Simply double-click `index.html` or deploy it to Netlify. It works independently of the backend using browser storage.

### 2. Run Backend (Optional)

To run the Python API locally:

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Start Server:**
```bash
python app.py
```

**Run Tests:**
```bash
pytest test_app.py
```

### 3. Run Automation

Use the included PowerShell script to manage the system:

```powershell
. .\automation-scripts.ps1
Test-RecipeSystemHealth  # Check system status
Backup-RecipeDatabase    # Create DB backup
```

## 🌐 Deployment

- **Frontend:** Drag `index.html` to Netlify Drop for instant hosting.
- **Backend:** Docker-ready (configurable via `requirements.txt` and `app.py`).

## 👤 Author

Deblina Mandal

## 📄 License

This project is licensed under the MIT License.
