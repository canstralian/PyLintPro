---
license: apache-2.0
title: Mendicant AI - Repo Healer
sdk: gradio
emoji: 🏥
colorFrom: blue
colorTo: green
short_description: Self-healing repositories that automatically detect and fix broken window issues.
sdk_version: 5.14.0
---

# Mendicant AI - Self-Healing Repositories

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Status](https://img.shields.io/badge/Status-MVP-orange.svg)
![Issues](https://img.shields.io/github/issues/canstralian/PyLintPro)

---

## 🎯 Public Commitment: 12-Week Sprint to $10k MRR

**Mendicant AI** automates the detection and remediation of repository health issues that slow down engineering teams. We fix "broken window" problems like flaky tests, security misconfigurations, and code quality issues through automated Pull Requests.

### 📊 Weekly Scoreboard

| Metric | Target | Current | Progress |
|--------|--------|---------|----------|
| **Monthly Recurring Revenue** | $10,000 | $0 | 0% |
| **Pilot Commitments** | 10 | 0 | 0% |
| **Outreach Messages** | 500 | 50 | 10% |
| **Customer Interviews** | 50 | 4 | 8% |
| **Active Installations** | 25 | 0 | 0% |

---

## 🏥 The Problem We Solve

Engineering teams lose velocity due to "broken window" issues:
- **Flaky tests** that waste CI time and developer trust
- **Security misconfigurations** that create vulnerabilities  
- **Code quality drift** that accumulates technical debt
- **Outdated dependencies** with known security issues
- **Inconsistent formatting** that clutters code reviews

**Mendicant** acts as your repository's immune system, automatically detecting and fixing these issues before they impact your team's productivity.

---

## 📚 Table of Contents

- [Public Commitment](#-public-commitment-12-week-sprint-to-10k-mrr)
- [The Problem We Solve](#-the-problem-we-solve)
- [Solution Overview](#-solution-overview)
- [Pilot Program](#-pilot-program)
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
  - [GitHub App](#github-app)
  - [Web Interface](#web-interface)
  - [CLI Usage](#cli-usage)
- [Repository Health Checks](#-repository-health-checks)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 🔧 Solution Overview

Mendicant operates as a **GitHub App** that continuously monitors your repositories and automatically creates Pull Requests to fix detected issues:

1. **Detection Engine**: Scans for code quality, security, and reliability issues
2. **Automated Remediation**: Creates targeted fixes via Pull Requests
3. **Team Integration**: Fits seamlessly into existing code review workflows
4. **Continuous Monitoring**: Prevents regression of fixed issues

### Target Audience
- **Engineering Leaders** seeking to improve team velocity
- **Senior Developers** who want automated code quality enforcement
- **Startups** using Python/JavaScript/TypeScript stacks

---

## 💰 Pilot Program

**14-Day Pilot Program - $1,500**

Get started with Mendicant and see immediate results:
- Full repository health assessment
- Automated fixes for up to 50 issues
- Weekly progress reports
- Direct access to our engineering team
- 20% discount on annual contract if you convert

**Success Metrics:**
- Reduce CI build failures by 30%
- Decrease time-to-merge by 25%
- Improve code coverage by 15%

[**Book Your Pilot Call →**](https://calendly.com/mendicant-ai/pilot)

---

## ✨ Features

### Repository Health Monitoring
- **Automated Issue Detection**: Continuously scans for code quality, security, and reliability issues
- **Smart Remediation**: Creates targeted Pull Requests with fixes
- **Multi-Language Support**: Python, JavaScript, TypeScript, and more
- **Security Scanning**: Detects vulnerable dependencies and misconfigurations
- **Test Stability**: Identifies and fixes flaky tests
- **Performance Monitoring**: Spots performance regressions in CI

### GitHub Integration
- **Native GitHub App**: Seamless integration with your existing workflow
- **Pull Request Automation**: Automatically creates PRs with detailed explanations
- **Team Collaboration**: Integrates with code review processes
- **Custom Rules**: Configure checks based on your team's standards

### Developer Experience
- **Real-Time Feedback**: Instant notifications about repository health
- **Detailed Reports**: Comprehensive analysis with actionable recommendations
- **Minimal Noise**: Smart filtering to focus on high-impact issues
- **Learning System**: Adapts to your team's preferences over time

---

## 🚀 Demo

Try the core linting functionality on [Hugging Face Spaces](https://huggingface.co/spaces/Canstralian/PyLintPro).

Full GitHub App demo available during pilot program.

---

## ⚡ Installation

### Prerequisites

- Python 3.9 or higher
- `flake8`
- `autopep8`
- `gradio`

Install dependencies:

```bash
pip install -r requirements.txt



⸻

🛠️ Usage

Web Interface
	1.	Clone the repository:

git clone https://github.com/canstralian/PyLintPro.git
cd PyLintPro


	2.	Run the Gradio app:

python app.py


	3.	Access the application at:
http://127.0.0.1:7860
	4.	Upload a .py file or paste code to lint and auto-fix.

⸻

CLI Usage

You can run PyLintPro directly from the command line to lint a file:

python lint.py your_script.py

Example:

python lint.py main.py

The script will output:
   •   Linting issues detected
   •   Auto-fix suggestions
   •   Corrected output saved to a file (*_fixed.py).

⸻

⚙️ Advanced Options

Customize linting behavior via optional arguments:
   •   Ignore specific Flake8 rules:

python lint.py your_script.py --ignore=E501,W503


   •   Output corrected code to a custom path:

python lint.py your_script.py --output=formatted/main_fixed.py



⸻

☁️ Deployment

Hugging Face Spaces (Recommended)

Use the included README.md, requirements.txt, and app.py.
Set Space SDK to Gradio and Python version to 3.9 or higher.

Docker

(Coming soon)

docker build -t pylintpro .
docker run -p 7860:7860 pylintpro



⸻

🛤️ Roadmap
   •   Real-time web linting
   •   CLI support
   •   Multi-file upload support
   •   Custom linting profiles per project
   •   CI/CD integration (GitHub Actions plugin)
   •   Docker containerization

⸻

⚠️ Known Limitations
   •   Maximum upload size: 10 MB per .py file.
   •   Processing speed slows for extremely large scripts (>5,000 lines).
   •   Autopep8 fixes most but not all complex style violations.

⸻

🤝 Contributing

We welcome contributions!
	1.	Fork this repository
	2.	Create a new feature branch:

git checkout -b feature/my-new-feature


	3.	Follow coding standards:
      •   PEP 8 compliance
      •   No new lint warnings (flake8 .)
	4.	Test your changes.
	5.	Submit a Pull Request.

Please open an issue first if making large changes.

⸻

📄 License

This project is licensed under the MIT License.

⸻

🙏 Acknowledgements
   •   Gradio
   •   Flake8
   •   autopep8

⸻

📫 Contact
   •   Email: support@pylintpro.com
   •   GitHub Issues: Submit a Ticket

⸻

PyLintPro: Bring clarity, consistency, and confidence to your Python projects.

---