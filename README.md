<div align="center">

```text
                                     ███                                               ████ 
                                    ░░░                                               ░░███ 
 █████ ███ █████  ██████  ████████  ████   ██████  ████████  █████ ███ █████  ██████   ░███ 
░░███ ░███░░███  ███░░███░░███░░███░░███  ███░░███░░███░░███░░███ ░███░░███  ░░░░░███  ░███ 
 ░███ ░███ ░███ ░███████  ░███ ░███ ░███ ░███ ░░░  ░███ ░░░  ░███ ░███ ░███   ███████  ░███ 
 ░░███████████  ░███░░░   ░███ ░███ ░███ ░███  ███ ░███      ░░███████████   ███░░███  ░███ 
  ░░████░████   ░░██████  ░███████  █████░░██████  █████      ░░████░████   ░░████████ █████
   ░░░░ ░░░░     ░░░░░░   ░███░░░  ░░░░░  ░░░░░░  ░░░░░        ░░░░ ░░░░     ░░░░░░░░ ░░░░░ 
                          ░███                                                              
                          █████       wepicrwal — Web Vuln Scanner               
                         ░░░░░        
```

# 🛡️ WEPICRWAL

### ⚡ Advanced Web Port & Vulnerability Scanner ⚡

**Fast. Lightweight. Ruthlessly thorough.**

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](#-legal-disclaimer)
[![Security](https://img.shields.io/badge/Security-Authorized%20Use%20Only-red.svg?style=for-the-badge)](#-legal-disclaimer)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg?style=for-the-badge)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-orange.svg?style=for-the-badge)](#-contributing)

*Developed with ❤️ by **Md Zishan Raza***

[Features](#-key-features) • [Installation](#️-manual-step-by-step-installation--setup) • [Usage](#-usage--examples) • [Screenshots](#-screenshots--workflow) • [Disclaimer](#-legal-disclaimer)

</div>

---

## 🚀 Overview

**Wepicrwal** is a powerful, lightweight, and fast **Python-based security tool** designed to test the security posture of web applications and servers.

It combines all of the following into a single tool:
- 🔌 Automated **TCP/UDP port scanning**
- 🕷️ Detection of common **web vulnerabilities** (XSS, SQL Injection, CSRF)
- 📊 A **stunning, executive-ready HTML report** that you can share directly with a client or team

Whether you're a pentester, a bug bounty hunter, or just want to check the security of your own web app — **Wepicrwal** gives you a clean, fast, and readable report without any complicated setup.

> ⚠️ **Note:** This tool is intended for **authorized security testing only**. Please make sure to read the [Legal Disclaimer](#-legal-disclaimer) below.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Comprehensive Port Scanning** | Performs deep scanning of TCP and UDP ports to identify open services and reports their risk levels (`Safe`, `Moderate`, `Unsafe`, `Critical`) |
| ⚡ **Web Vulnerability Checks** | Reflected XSS, error-based SQL Injection detection, and CSRF token validation — all in one place |
| 🔒 **Mandatory Authorization Gate** | Built-in confirmation prompt that prevents accidental / unauthorized scanning |
| 📊 **Stunning HTML Reports** | Generates dark-themed, modern, mobile-responsive reports with summary cards and detailed findings |
| 🧵 **Multithreaded Performance** | Uses threading for fast and efficient scanning |
| 🕒 **Timestamped Reports** | Every scan produces its own unique, timestamped report file — making it easy to keep a history |
| 🧩 **Modular Scan Modes** | Scan ports only, vulnerabilities only, or both — your choice |
| 🖥️ **Cross-Platform** | Works on Linux, macOS, and Windows (with Python 3) |

### 🔥 Detailed Breakdown

- 🌐 **Port Intelligence**
  - Fast detection of open/closed/filtered ports
  - Risk classification for each port so you can prioritize what to fix first

- 🕸️ **Vulnerability Engine**
  - **Reflected XSS** — via URL parameters & form inputs
  - **SQL Injection (SQLi)** — error-based signature detection
  - **CSRF** — protection token analysis on POST forms

- 📈 **Reporting Engine**
  - Executive summary cards (total ports scanned, vulnerabilities found, risk score)
  - Clean, shareable, dark-mode HTML output — ready to hand to a client

---

## 🛠️ Manual Step-by-Step Installation & Setup

Follow these steps to set up the tool on your local machine:

### Step 1️⃣ — Clone the Repository

```bash
git clone https://github.com/zishanofficial17-eng/wepicrwal.git
cd wepicrwal
```

### Step 2️⃣ — Verify Python Installation

Check whether Python 3 is installed on your system:

```bash
python3 --version
```

If Python 3 isn't installed, download it from the [official website](https://www.python.org/downloads/).

### Step 3️⃣ — (Recommended) Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### Step 4️⃣ — Install Required Dependencies

```bash
pip install requests beautifulsoup4
```

> 💡 If you run into a permission error, you can use the `--user` flag:
> ```bash
> pip install --user requests beautifulsoup4
> ```

### Step 5️⃣ — Make the Script Executable (Linux/macOS)

```bash
chmod +x Wepicrwal.py
```

✅ **Setup complete!** You're now ready to run the tool.

---

## 💻 Usage & Examples

Pass a target URL or domain to run the tool:

```bash
python3 Wepicrwal.py http://example.com
```

### 🎛️ Advanced Options

| Command | Purpose |
|---|---|
| `python3 Wepicrwal.py target.com --ports-only` | Runs **port scan only** |
| `python3 Wepicrwal.py http://target.com --vuln-only` | Runs **vulnerability scan only** |
| `python3 Wepicrwal.py http://target.com -o my_custom_report.html` | Sets a **custom HTML report name** |
| `python3 Wepicrwal.py --help` | Shows all available options |

---

## 📸 Screenshots & Workflow

> 📌 *Don't forget to add your tool's actual screenshots here — it'll make the README even more attractive!*

```markdown
![Banner Preview](assets/banner-preview.png)
![Scan In Progress](assets/scan-progress.png)
![HTML Report Sample](assets/report-sample.png)
```

**The workflow looks something like this:**

1. 🏁 **Banner & Authorization** — The tool displays its ASCII banner on startup and asks for a legal disclaimer/authorization confirmation for the target
2. 🔎 **Scanning** — TCP/UDP ports and web forms are tested (with live progress shown)
3. 📄 **Report Generation** — A unique, timestamped HTML file is generated

   ```
   wepicrwal_target_com_20260328.html
   ```

4. 🎉 **Done!** — Open the report in your browser to review the findings

---

## 🧭 Roadmap

- [ ] 🌍 Subdomain enumeration module
- [ ] 🧪 Blind SQLi & time-based detection
- [ ] 📑 PDF export for reports
- [ ] 🔔 Slack/Discord webhook notifications
- [ ] 🐳 Docker support

*(Feel free to suggest more via Issues!)*

---

## 🤝 Contributing

Contributions are genuinely welcome! 🎉

1. **Fork** the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add some amazing feature'`)
4. **Push** the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

---

## ⚠️ Legal Disclaimer

> **Wepicrwal** is built **strictly for educational purposes** and **authorized penetration testing / security audits**.
>
> Performing port scanning or vulnerability testing on any system without explicit written permission is **illegal** and can lead to serious legal consequences.
>
> The developers are **not responsible** for any misuse of this tool. Please use it responsibly. 🙏

---

## 📜 License

This project is distributed under the **MIT License** — see the [`LICENSE`](LICENSE) file for more details.

---

## 👤 Author

<div align="center">

**Md Zishan Raza**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/zishanofficial17-eng)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/md-zishan-rz)

⭐ **If you liked this project, please consider giving it a Star!** ⭐

</div>
