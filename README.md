# ☁️ CloudGuard - AWS Cloud Misconfiguration Scanner

**CloudGuard** is a Flask-based web tool that performs real-time security analysis of AWS cloud environments. By accepting user-provided AWS credentials (Access Key and Secret Key), it scans for misconfigurations in services like **S3** and **EC2**, suggests mitigations, and generates a comprehensive **PDF report**.

---

## 🚀 Features

- 🔐 **Credential-based Access**: Users input AWS Access & Secret keys for analysis.
- 🧠 **Misconfiguration Detection**:
  - Public S3 Buckets
  - S3 Bucket Versioning
  - EC2 Security Group Exposure
  - EC2 Key Pair Analysis
- 📄 **PDF Report Generation**: Summarized results and mitigation suggestions.
- 🌐 **Simple Flask Web Interface**
- 🛠️ **Modular Code**: Easy to extend with more AWS services and rules.
- ✅ Built with best practices for AWS security audits.

---

## 📸 Screenshots

| Dashboard | PDF Report |
|----------|------------|
| ![dashboard](screenshots/dashboard.png) | ![report](screenshots/pdf_report.png) |

---

## 🧰 Tech Stack

- **Python 3**
- **Flask** (Web Framework)
- **Boto3** (AWS SDK for Python)
- **ReportLab** (for PDF generation)
- **HTML/CSS** (Frontend)

---

## 🔧 Installation & Setup

```bash
git clone https://github.com/smilest-soul/CloudGuard.git
cd CloudGuard
pip install -r requirements.txt
