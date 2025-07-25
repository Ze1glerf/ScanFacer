# 🕷️ ScanFacer

**ScanFacer** is a powerful yet simple Python-based website crawler that scans and logs all discovered pages of a domain into a timestamped `.txt` file. It is interactive, customizable, and designed with ethical usage in mind — making it ideal for SEO analysts, penetration testers, digital archivers, and web researchers.

---

### ✨ Features

- 🔍 Recursively scans internal pages of a website
- 🕒 Prompts delay time between each request (recommended: 20s)
- 🌐 Asks user whether to use HTTP or HTTPS
- 📄 Outputs results into a nicely formatted `.txt` file
- ⛔ Skips non-HTML content
- 🔁 Depth-limited recursion (default: 3 levels)
- 🤖 CLI-based and user-friendly

---

### 🚀 How to Install

```bash
git clone https://github.com/Ze1glerf/ScanFacer.git
cd ScanFacer
pip install -r requirements.txt
