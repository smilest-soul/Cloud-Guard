# 🌟 AWS Cloud Guard - Setup Guide 🚀🔐🌍

## Overview 📖🔍
AWS Cloud Guard is a powerful security monitoring and compliance tool designed to help organizations maintain security best practices across their AWS infrastructure. The tool provides real-time monitoring, security assessment, and compliance reporting capabilities.

## Features ✨🛡️

- **Multi-Service Security Monitoring**
  - IAM (Identity and Access Management)
  - EC2 (Elastic Compute Cloud)
  - S3 (Simple Storage Service)
  - SQS (Simple Queue Service)
  - SNS (Simple Notification Service)
  - CloudWatch
  - CloudFormation
  - DynamoDB
  - Glacier
  - OpsWorks

- **Security Assessments**
  - Identity and Access Management audits
  - Resource configuration analysis
  - Security group and network security checks
  - Compliance monitoring
  - Vulnerability scanning

- **Reporting** 📊📄
  - PDF report generation
  - Security findings documentation
  - Compliance status reports
  - Visual data representation

- **Web Interface** 🌐💻
  - User-friendly dashboard
  - Real-time monitoring
  - Interactive security controls
  - Customizable views

---

## System Requirements ✅⚙️💻
Ensure your system meets the following requirements before running the application:

- Windows 10/11 or Linux/macOS
- Python 3.13 or higher
- AWS CLI installed
- Internet connection

### **Core Dependencies** 📦🔧
```
boto3>=1.34.0
botocore>=1.34.0
flask>=3.1.0
werkzeug>=3.1.3
numpy>=1.26.0
Pillow>=10.2.0
PyFPDF>=1.7.2
```

### **Additional Dependencies** 🔌📂
```
pywin32>=306
markupsafe>=3.0.2
itsdangerous>=2.2.0
charset-normalizer>=3.3.0
certifi>=2024.2.2
python-dateutil>=2.8.2
PyYAML>=6.0.1
```

### **Hardware Requirements** 🖥️⚡
- Windows 10 or higher
- Minimum 4GB RAM
- 500MB free disk space
- Internet connection for AWS service access

---

## Step 1: Install Required Dependencies 📦🔧⚡

### **Windows** (Command Prompt / PowerShell):
```sh
pip install -r requirements.txt
```

### **Linux/Mac** (Terminal):
```sh
pip3 install -r requirements.txt
```

---

## Step 2: Configure AWS Credentials 🔑☁️🌍
Run the following command in your terminal or command prompt:
```sh
aws configure
```
Enter the following details when prompted:
- **AWS Access Key ID**: (Provided by Admin)
- **AWS Secret Access Key**: (Provided by Admin)
- **Default region name**: us-east-1 (or as per your AWS setup)
- **Default output format**: json

**Alternatively**, set credentials manually in environment variables:

### **Windows (CMD/PowerShell)**:
```sh
set AWS_ACCESS_KEY_ID=your-access-key
set AWS_SECRET_ACCESS_KEY=your-secret-key
set AWS_REGION=us-east-1
```

### **Linux/Mac (Terminal)**:
```sh
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_REGION=us-east-1
```

---

## Step 3: Verify AWS Configuration ✅🔍📡
To check if AWS CLI is configured correctly, run:
```sh
aws s3 ls
```
If it returns a list of S3 buckets (or an access denied error), AWS is set up correctly.

---

## Step 4: Running the Application 🚀💻⚙️
Navigate to the application folder and execute:
```sh
./app.exe  # (For Windows)
./app  # (For Linux/Mac)
```
If you encounter issues, ensure:
- AWS credentials and region are configured
- All dependencies are installed
- Internet connection is stable

---

## Troubleshooting 🛠️❗📢

### **Error: 'botocore.exceptions.NoRegionError'**
**Solution:** Set the region manually as shown in Step 2.

### **Error: 'AWS CLI not recognized'**
**Solution:** Install AWS CLI from [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)

### **Error: 'ModuleNotFoundError'**
**Solution:** Run `pip install -r requirements.txt` to install missing packages.

---

## Security Features 🔒🛡️
- SSL/TLS encryption
- Secure credential management
- Role-based access control
- Audit logging
- Real-time security alerts

## Support 📩📞🛡️
For support and issues, please contact the development team or create an issue in the repository.

## License 📜⚖️
This project is proprietary software. All rights reserved.

## Disclaimer ⚠️📢
This tool is designed to assist with AWS security monitoring but should be used as part of a comprehensive security strategy. Always follow AWS security best practices and maintain proper security controls.

## Deployment Guide 🚀☁️

### AWS Elastic Beanstalk Deployment

#### Prerequisites
- AWS Elastic Beanstalk CLI installed
- AWS CLI configured with appropriate credentials
- Git installed

#### Step 1: Install EB CLI
```sh
pip install awsebcli
```

#### Step 2: Initialize EB Project
```sh
eb init aws-cloud-guard
```
When prompted:
- Select your region
- Create new application
- Select Python platform
- Choose Python 3.13
- Set up SSH for instances (recommended)
- Choose your keypair

#### Step 3: Create Environment
```sh
eb create production-env
```
This will:
- Create an Elastic Beanstalk environment
- Deploy your application
- Set up load balancer
- Configure auto-scaling

#### Step 4: Configure Environment Variables
Set up required environment variables in Elastic Beanstalk:
```sh
eb setenv AWS_ACCESS_KEY_ID=your-access-key \
          AWS_SECRET_ACCESS_KEY=your-secret-key \
          AWS_REGION=your-region \
          FLASK_ENV=production
```

#### Step 5: Deploy Updates
For future updates:
```sh
eb deploy
```

#### Step 6: Monitor Deployment
```sh
eb health
eb status
```

#### Important Configuration Files

1. **requirements.txt** (already present)
```
boto3>=1.34.0
botocore>=1.34.0
flask>=3.1.0
werkzeug>=3.1.3
numpy>=1.26.0
Pillow>=10.2.0
PyFPDF>=1.7.2
pywin32>=306
markupsafe>=3.0.2
itsdangerous>=2.2.0
charset-normalizer>=3.3.0
certifi>=2024.2.2
python-dateutil>=2.8.2
PyYAML>=6.0.1
```

## Version History 📌📅
- **v1.0.0 - Initial Release** 🎉
  - Basic security monitoring
  - PDF report generation
  - Web interface
  - Multi-service support
 
