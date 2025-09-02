
---
license: apache-2.0
title: Mendicant AI
sdk: gradio
emoji: 🤖
colorFrom: indigo
colorTo: purple
short_description: An AI-powered development assistant for code analysis, project management, and GitHub integration.
sdk_version: 5.14.0
---

# 🤖 Mendicant AI

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-%F0%9F%9A%80-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%E2%9C%94-blue.svg)
![GitHub Integration](https://img.shields.io/badge/GitHub-OAuth-black?logo=github)
[![Hugging Face Space](https://img.shields.io/badge/Space-Status-green)](https://huggingface.co/spaces/Canstralian/MendicantAI)

---

**Mendicant AI** is an **AI-powered development assistant** designed to streamline the way developers and teams build software.  
It combines **intelligent repository analysis, project management tools, and seamless GitHub integration** into a single platform.  

Think of it as your **Swiss Army Knife for modern development** — balancing **speed**, **security**, and **clarity**.  

---

## 📚 Table of Contents

- [✨ Features](#-features)
- [🚀 Demo](#-demo)
- [⚡ Installation](#-installation)
- [🛠️ Usage](#-usage)
  - [Web Interface](#web-interface)
  - [CLI Usage](#cli-usage)
- [⚙️ Tech Stack](#-tech-stack)
- [☁️ Deployment](#-deployment)
- [🛤️ Roadmap](#-roadmap)
- [⚠️ Known Limitations](#-known-limitations)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgements](#-acknowledgements)
- [📫 Contact](#-contact)

---

## ✨ Features

- 🔐 **Authentication & Security**
  - Email/password auth with JWT tokens
  - GitHub OAuth support
  - Secure password hashing (`bcrypt`)
  - Session management and user profiles

- 📊 **Project Management**
  - Create, update, and delete projects
  - Link projects to GitHub repositories
  - Organize and track project progress
  - Isolated user-specific project spaces

- 🔍 **Repository Analysis**
  - Automated GitHub repo scanning
  - Code quality assessments
  - Language distribution insights
  - Commit activity metrics

- 🛠️ **GitHub Integration**
  - OAuth-based authentication
  - Repo browsing and API data fetching
  - Secure token handling
  - AI-assisted insights for repos

---

## 🚀 Demo

Try the live demo on [Hugging Face Spaces](https://huggingface.co/spaces/Canstralian/MendicantAI).

---

## ⚡ Installation

### Prerequisites
- Python 3.9 or higher  
- Node.js (for frontend)  
- PostgreSQL database  

### Setup

```bash
# Clone repository
git clone https://github.com/canstralian/MendicantAI.git
cd MendicantAI

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install


⸻

🛠️ Usage

Web Interface

# Run backend
cd backend
uvicorn main:app --reload

# Run frontend
cd frontend
npm run dev

	•	Visit: http://127.0.0.1:3000 (frontend)
	•	API available at: http://127.0.0.1:8000

CLI Usage

Run repository analysis from the terminal:

python scripts/analyze_repo.py --url https://github.com/user/repo


⸻

⚙️ Tech Stack
	•	Backend: FastAPI · SQLAlchemy · PyJWT · PostgreSQL
	•	Frontend: React · TailwindCSS · TypeScript · Vite
	•	Dev & Testing: Pytest · Asyncio · HTTPX · Docker
	•	Integrations: GitHub API · OAuth 2.0

⸻

☁️ Deployment

Hugging Face Spaces

Deploy with Gradio for quick demos and prototypes.

Replit
	1.	Import the repo
	2.	Install dependencies (pip install -r requirements.txt)
	3.	Run the backend + frontend directly in Replit

Docker

docker-compose up --build


⸻

🛤️ Roadmap
	•	AI-driven code reviews
	•	PR linting & auto-fix suggestions
	•	Team collaboration dashboards
	•	CI/CD GitHub Actions integration
	•	VS Code plugin

⸻

⚠️ Known Limitations
	•	Repo analysis may be slow for very large projects (>1GB).
	•	Only GitHub repos supported in this release (GitLab/Bitbucket planned).
	•	Hugging Face demo runs with limited resources (use Docker for production).

⸻

🤝 Contributing

We welcome contributions!
	1.	Fork this repo
	2.	Create a feature branch:

git checkout -b feature/my-feature


	3.	Follow standards (PEP 8, ESLint, Prettier)
	4.	Submit a Pull Request

⸻

📄 License

This project is licensed under the Apache 2.0 License.
See LICENSE for details.

⸻

🙏 Acknowledgements
	•	FastAPI
	•	React
	•	PostgreSQL
	•	Hugging Face Spaces

⸻

📫 Contact
	•	GitHub Issues: Submit a Ticket
	•	Hugging Face: Discussion Board
	•	Email: support@mendicantai.dev

⸻

🚀 Mendicant AI — your intelligent partner for secure, scalable, and insightful software development.

---
