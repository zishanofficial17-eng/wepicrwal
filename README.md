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

**Wepicrwal** ek powerful, lightweight aur fast **Python-based security tool** hai jo web applications aur servers ki security posture ko test karne ke liye design kiya gaya hai.

Ye ek hi tool me combine karta hai:
- 🔌 Automated **TCP/UDP port scanning**
- 🕷️ Common **web vulnerability detection** (XSS, SQL Injection, CSRF)
- 📊 Ek **stunning, executive-ready HTML report** jo aap client ya team ke saath directly share kar sakein

Chahe aap ek pentester ho, bug bounty hunter ho, ya apni khud ki web app ki security check karna chahte ho — **Wepicrwal** aapko ek clean, fast aur readable report deta hai, bina kisi complex setup ke.

> ⚠️ **Note:** Yeh tool sirf **authorized security testing** ke liye hai. Neeche diya gaya [Legal Disclaimer](#-legal-disclaimer) zaroor padhein.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Comprehensive Port Scanning** | TCP aur UDP ports ki deep scanning karke open services identify karta hai aur unke risk levels (`Safe`, `Moderate`, `Unsafe`, `Critical`) batata hai |
| ⚡ **Web Vulnerability Checks** | Reflected XSS, error-based SQL Injection, aur CSRF token validation — sab ek jagah |
| 🔒 **Mandatory Authorization Gate** | Built-in confirmation prompt jo accidental / unauthorized scanning ko rokta hai |
| 📊 **Stunning HTML Reports** | Dark-themed, modern, mobile-responsive reports — summary cards + detailed findings |
| 🧵 **Multithreaded Performance** | Threading ke through fast aur efficient scanning |
| 🕒 **Timestamped Reports** | Har scan ki apni unique, timestamped report file — history maintain karna easy |
| 🧩 **Modular Scan Modes** | Sirf ports, sirf vulnerabilities, ya dono — aapki marzi |
| 🖥️ **Cross-Platform** | Linux, macOS aur Windows — sab par chalta hai (Python 3 ke saath) |

### 🔥 Detailed Breakdown

- 🌐 **Port Intelligence**
  - Open/closed/filtered ports ka fast detection
  - Har port ke liye risk classification, taaki aap priority decide kar sako

- 🕸️ **Vulnerability Engine**
  - **Reflected XSS** — URL parameters & form inputs ke through
  - **SQL Injection (SQLi)** — error-based signature detection
  - **CSRF** — POST forms me protection token analysis

- 📈 **Reporting Engine**
  - Executive summary cards (total ports scanned, vulnerabilities found, risk score)
  - Clean, shareable, dark-mode HTML output — client-ready

---

## 🛠️ Manual Step-by-Step Installation & Setup

Apne local machine par is tool ko setup karne ke liye yeh steps follow karein:

### Step 1️⃣ — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/wepicrwal.git
cd wepicrwal
```

### Step 2️⃣ — Verify Python Installation

Check karein ki aapke system me Python 3 installed hai ya nahi:

```bash
python3 --version
```

Agar Python 3 install nahi hai, toh [official website](https://www.python.org/downloads/) se download kar lein.

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

> 💡 Agar permission error aaye, toh `--user` flag use kar sakte hain:
> ```bash
> pip install --user requests beautifulsoup4
> ```

### Step 5️⃣ — Make the Script Executable (Linux/macOS)

```bash
chmod +x Wepicrwal.py
```

✅ **Setup complete!** Ab aap tool run karne ke liye ready hain.

---

## 💻 Usage & Examples

Tool ko run karne ke liye target URL ya domain pass karein:

```bash
python3 Wepicrwal.py http://example.com
```

### 🎛️ Advanced Options

| Command | Purpose |
|---|---|
| `python3 Wepicrwal.py target.com --ports-only` | Sirf **Port Scan** karta hai |
| `python3 Wepicrwal.py http://target.com --vuln-only` | Sirf **Vulnerability Scan** karta hai |
| `python3 Wepicrwal.py http://target.com -o my_custom_report.html` | Custom **HTML report name** deta hai |
| `python3 Wepicrwal.py --help` | Saare available options dikhata hai |

---

## 📸 Screenshots & Workflow

> 📌 *Yahan par apne tool ke actual screenshots add karna na bhoolein — README aur bhi zyada attractive lagegi!*

```markdown
![Banner Preview](assets/banner-preview.png)
![Scan In Progress](assets/scan-progress.png)
![HTML Report Sample](assets/report-sample.png)
```

**Workflow kuch is tarah dikhta hai:**

1. 🏁 **Banner & Authorization** — Tool start hote hi ASCII banner dikhayega aur target confirm karne ke liye legal disclaimer/authorization maangega
2. 🔎 **Scanning** — TCP/UDP ports aur web forms test honge (progress live dikhega)
3. 📄 **Report Generation** — Ek unique, timestamped HTML file generate hogi

   ```
   wepicrwal_target_com_20260328.html
   ```

4. 🎉 **Done!** — Report ko browser me open karke findings review karein

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

Contributions dil se welcome hain! 🎉

1. Repository ko **Fork** karein
2. Ek naya branch banayein (`git checkout -b feature/amazing-feature`)
3. Apne changes **Commit** karein (`git commit -m 'Add some amazing feature'`)
4. Branch ko **Push** karein (`git push origin feature/amazing-feature`)
5. Ek **Pull Request** open karein

---

## ⚠️ Legal Disclaimer

> **Wepicrwal** ko sirf **educational purposes** aur **authorized penetration testing / security audits** ke liye banaya gaya hai.
>
> Bina explicit written permission ke kisi bhi system par port scanning ya vulnerability testing karna **illegal** hai aur isse severe legal consequences ho sakte hain.
>
> Developers is tool ke kisi bhi misuse ke zimmedaar **nahi** hain. Use responsibly. 🙏

---

## 📜 License

Is project ko **MIT License** ke andar distribute kiya gaya hai — dekhein [`LICENSE`](LICENSE) file for more details.

---

## 👤 Author

<div align="center">

**Md Zishan Raza**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](#)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](#)

⭐ **Agar yeh project pasand aaya, toh ek Star zaroor dedein!** ⭐

</div>
