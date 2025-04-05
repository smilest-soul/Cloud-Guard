from flask import Flask, render_template_string, request, redirect, url_for, send_file, render_template, session, flash
import boto3
import os
from fpdf import FPDF
from datetime import datetime
import json
from functools import wraps
import botocore

app = Flask(__name__)
app.secret_key = os.urandom(24)

s3_client = boto3.client('s3')
ec2_client = boto3.client('ec2')

report_path = os.path.join(os.getcwd(), "report.pdf")

base_template = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>CloudGuard - AWS Security</title>
    <link href="https://fonts.googleapis.com/css2?family=Cascadia+Code&family=Rubik:wght@500&family=Poppins:wght@500&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(to right, #f8f8f8, #f0f0f0);
            margin: 0;
            padding: 0;
            animation: fadeIn 1s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .header {
            background: #b2244d;
            color: white;
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .logo {
            height: 90px;
            position: absolute;
            left: 2rem;
        }
        .title {
            font-family: 'Rubik', sans-serif;
            font-size: 2.3rem;
            font-weight: 600;
            color: white;
        }
        .nav {
            display: flex;
            justify-content: center;
            background: #8f1d3f;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .nav a {
            color: white;
            padding: 1rem 1.5rem;
            text-decoration: none;
            font-weight: bold;
            font-size: 1rem;
            transition: background 0.3s;
        }
        .nav a:hover {
            background: #721432;
        }
        .container {
            max-width: 900px;
            margin: 6rem auto 3rem auto;
            padding: 2rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            animation: slideUp 0.5s ease-in-out;
        }
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .standards {
            margin-top: 2rem;
            text-align: center;
        }
        .standards img {
            width: 60px;
            margin: 10px;
            vertical-align: middle;
        }
        .download-report {
            display: block;
            margin: 2rem auto 1rem auto;
            text-align: center;
        }
        .download-report a {
            background-color: #b2244d;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .download-report a:hover {
            background-color: #721432;
        }
        .issue ul { list-style: none; padding: 0; }
        .issue li {
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .mitigate-button {
            padding: 6px 12px;
            background-color: #b2244d;
            border: none;
            color: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background-color 0.3s ease;
        }
        .mitigate-button:hover {
            background-color: #8f1d3f;
        }
        .credentials-form {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }

        .credentials-form label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        .credentials-form input[type='text'],
        .credentials-form input[type='password'] {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box; /* Ensures padding doesn't affect width */
        }

        .credentials-form button {
            background-color: #5cb85c;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .credentials-form button:hover {
            background-color: #449d44;
        }
        .logout-button {
            background-color: #d9534f;
            color: white;
            padding: 8px 12px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            font-size: 0.9rem;
            transition: background-color 0.3s ease;
        }

        .logout-button:hover {
            background-color: #c9302c;
        }
    .flashes {
      list-style: none;
      padding: 0;
      margin-bottom: 1rem;
    }
    .flashes li {
      padding: 0.75rem;
      border-radius: 5px;
    }

    .flashes .error {
      background-color: #f8d7da;
      border: 1px solid #f5c6cb;
      color: #721c24;
    }

    .flashes .success {
      background-color: #d4edda;
      border: 1px solid #c3e6cb;
      color: #155724;
    }
    </style>
</head>
<body>
    <div class='header'>
        <img src='https://www.leadsquared.com/wp-content/uploads/2023/09/Amrita-vishwa-vidyapeetham-logo-1.png' alt='Amrita Logo' class='logo'>
        <div class='title'>CloudGuard - AWS Security Tool</div>
    </div>
    <div class='nav'>
        <a href='/'>Home</a>
        {% if session.get('access_key') %}
            <a href='/scan_s3'>S3 Scan</a>
            <a href='/scan_ec2'>EC2 Scan</a>
            
            
            <a href='/logout' class="logout-button">Logout</a>
        {% else %}
            <a href='/login'>Login</a>
        {% endif %}
    </div>
    <div class='container'>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <ul class="flashes">
                    {% for category, message in messages %}
                        <li class="{{ category }}">{{ message }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        {{ content | safe }}
        {% if show_download %}
        <div class="standards">
            <h3>We follow global security standards:</h3>
            <p><b>GDPR:</b> Ensures personal data protection for EU citizens.<br>
            <b>NIST:</b> Provides a framework for improving cybersecurity resilience.<br>
            <b>PCI DSS:</b> Sets security standards for handling cardholder data.</p>
           <img src="https://130e178e8f8ba617604b-8aedd782b7d22cfe0d1146da69a52436.ssl.cf1.rackcdn.com/nist-unveils-updated-guide-to-privacy-security-controls-showcase_image-5-a-15057.jpg" alt="NIST Updated Guide to Privacy and Security Controls" width="600" height="auto">
           <img src="https://www.ardentprivacy.ai/assets/img/gdpr_act.png" alt="GDPR Act Image" width="600" height="auto">
           <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnmMJ-v3wIN1_9gMykBO1WCMddiSTQzH_CXQ&s" alt="PCI DSS Image" width="600" height="auto">
        </div>
        <div class="download-report">
            <a href="/download_report">⬇️ Log Report</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def check_s3_security(access_key, secret_key):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    report = []

    try:
        for bucket in s3.list_buckets().get('Buckets', []):
            bucket_name = bucket['Name']
            acl = s3.get_bucket_acl(Bucket=bucket_name)
            public = any(grant['Grantee'].get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers' for grant in acl['Grants'])
            report.append(f"Bucket: {bucket_name} - {'Public' if public else 'Private'}")

    except Exception as e:
        report.append(f"Error checking S3 security: {str(e)}")
    return report

def check_ec2_security(access_key, secret_key):
    ec2 = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    report = []
    try:
        for sg in ec2.describe_security_groups()['SecurityGroups']:
            for rule in sg['IpPermissions']:
                if '0.0.0.0/0' in [ip['CidrIp'] for ip in rule.get('IpRanges', [])]:
                    report.append(f"Security Group {sg['GroupId']} has an open port {rule.get('FromPort', 'Unknown')}")
    except Exception as e:
        report.append(f"Error checking EC2 security: {str(e)}")

    return report

def generate_pdf(report):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="CloudGuard - AWS Security Report", ln=True, align='C')
    pdf.ln(10)
    for line in report:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        pdf.multi_cell(0, 10, f"{timestamp} - {line}")
    pdf.output(report_path)
    return report_path

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('access_key') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    content = """
    <h2>Welcome to CloudGuard</h2>
    <p>Login to scan your AWS resources.</p>
    """
    return render_template_string(base_template, content=content, show_download=True)

def get_login_form():
    return """
        <h2>Login</h2>
        <div class="credentials-form">
            <form method="post">
                <label for="access_key">AWS Access Key:</label>
                <input type="text" id="access_key" name="access_key" required><br><br>
                <label for="secret_key">AWS Secret Key:</label>
                <input type="password" id="secret_key" name="secret_key" required><br><br>
                <button type="submit">Login</button>
            </form>
        </div>
    """

@app.route('/login', methods=['GET', 'POST'])
# @app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        access_key = request.form['access_key']
        secret_key = request.form['secret_key']

        try:
            # Validate S3 access
            s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            s3.list_buckets()

            # Validate EC2 access
            ec2 = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            ec2.describe_instances()

            # If both S3 and EC2 access are successful, store the credentials in the session
            session['access_key'] = access_key
            session['secret_key'] = secret_key
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))

        except botocore.exceptions.ClientError as e:
            flash('Invalid AWS credentials. Please ensure credentials have access to S3 and EC2.', 'error')
            print(f"Authentication error: {e}")
            return render_template_string(base_template, content=get_login_form(), show_download=False)

        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
            print(f"An error occurred: {e}")
            return render_template_string(base_template, content=get_login_form(), show_download=False)

    else:
        return render_template_string(base_template, content=get_login_form(), show_download=False)
@app.route('/logout')
def logout():
    session.pop('access_key', None)
    session.pop('secret_key', None)
    return redirect(url_for('home'))

@app.route('/scan_s3')
@login_required
def scan_s3():
    access_key = session['access_key']
    secret_key = session['secret_key']
    s3_resource = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    buckets = []
    session['report_data'] = []
    try:
        for b in s3_resource.list_buckets()['Buckets']:
            bucket = b['Name']
            issues = []
            try:
                block = s3_resource.get_public_access_block(Bucket=bucket)
                if all(block['PublicAccessBlockConfiguration'].values()):
                    issues.append(('✅ Public access fully blocked.', None))
                    session['report_data'].append(f"S3 Bucket '{bucket}': Public access is fully blocked.")
                    mitigation_url = None
                else:
                    mitigation_url = url_for('mitigate_public_access', bucket=bucket)
                    issues.append(('❌ Public access NOT fully blocked.', mitigation_url))
                    session['report_data'].append(f"S3 Bucket '{bucket}': Public access is NOT fully blocked.")

            except Exception as e:
                issues.append((f'⚠️ Access block error: {str(e)}', None))
                mitigation_url = None
            try:
                cors = s3_resource.get_bucket_cors(Bucket=bucket)
                if cors.get('CORSRules'):
                    issues.append(('✅ CORS is configured.', None))
                    session['report_data'].append(f"S3 Bucket '{bucket}': CORS is configured.")
                    mitigation_url = None
                else:
                    mitigation_url = url_for('mitigate_cors', bucket=bucket)
                    issues.append(('⚠️ No CORS rules found.', mitigation_url))
                    session['report_data'].append(f"S3 Bucket '{bucket}': No CORS rules configured.")
            except Exception as e:
                mitigation_url = url_for('mitigate_cors', bucket=bucket)
                issues.append(('⚠️ No CORS configuration.', mitigation_url))
            buckets.append({'name': bucket, 'issues': issues})
    except Exception as e:
        buckets.append({'name': 'Error', 'issues': [(str(e), None)]})

    content = '<h2>S3 Scan Results</h2>'
    for bucket in buckets:
        content += f'<div class="issue"><h3>{bucket["name"]}</h3><ul>'
        for issue, action in bucket['issues']:
            content += f'<li>{issue}'
            if action:
                content += f'<form method="POST" action="{action}"><button class="mitigate-button">Mitigate</button></form>'
            content += '</li>'
        content += '</ul></div>'
    return render_template_string(base_template, content=content, show_download=False)

@app.route('/scan_ec2')
@login_required
def scan_ec2():
    access_key = session['access_key']
    secret_key = session['secret_key']
    ec2_resource = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    instances = []
    session['report_data'] = []
    try:
        reservations = ec2_resource.describe_instances()['Reservations']
        for res in reservations:
            for inst in res['Instances']:
                instance_id = inst['InstanceId']
                issues = []
                try:
                    attr = ec2_resource.describe_instance_attribute(InstanceId=instance_id, Attribute='disableApiTermination')
                    if attr['DisableApiTermination']['Value']:
                        issues.append(('✅ Termination protection is enabled.', None))
                        session['report_data'].append(f"EC2 Instance '{instance_id}': Termination protection enabled.")
                        mitigation_url = None
                    else:
                        mitigation_url = url_for('mitigate_termination', instance_id=instance_id)
                        issues.append(('❌ Termination protection is disabled.', mitigation_url))
                        session['report_data'].append(f"EC2 Instance '{instance_id}': Termination protection disabled.")
                except Exception as e:
                    issues.append((f'⚠️ Termination check error: {str(e)}', None))
                    mitigation_url = None

                try:
                    for sg in inst['SecurityGroups']:
                        sg_info = ec2_resource.describe_security_groups(GroupIds=[sg['GroupId']])
                        for perm in sg_info['SecurityGroups'][0]['IpPermissions']:
                            if perm.get('FromPort') == 22 and perm.get('ToPort') == 22:
                                for ip_range in perm.get('IpRanges', []):
                                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                                        mitigation_url = url_for('mitigate_ssh', instance_id=instance_id)
                                        issues.append(('❌ SSH is open to the world.', mitigation_url))
                                        session['report_data'].append(f"EC2 Instance '{instance_id}': SSH is open to world.")
                except Exception as e:
                    issues.append((f'⚠️ SSH check error: {str(e)}', None))
                    mitigation_url = None

                instances.append({'id': instance_id, 'issues': issues})
    except Exception as e:
        instances.append({'id': 'Error', 'issues': [(str(e), None)]})

    content = '<h2>EC2 Scan Results</h2>'
    for inst in instances:
        content += f'<div class="issue"><h3>{inst["id"]}</h3><ul>'
        for issue, action in inst['issues']:
            content += f'<li>{issue}'
            if action:
                content += f'<form method="POST" action="{action}"><button class="mitigate-button">Mitigate</button></form>'
            content += '</li>'
        content += '</ul></div>'
    return render_template_string(base_template, content=content, show_download=False)


@app.route('/mitigate_public_access/<bucket>', methods=['POST'])
@login_required
def mitigate_public_access(bucket):
    access_key = session['access_key']
    secret_key = session['secret_key']
    s3_resource = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    try:
        s3_resource.put_public_access_block(
            Bucket=bucket,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True,
            }
        )
        session['report_data'].append(f"S3 Bucket '{bucket}': Mitigated public access.")
        flash(f"Successfully mitigated public access for bucket '{bucket}'.", "success")
    except Exception as e:
        flash(f"Error mitigating public access for bucket '{bucket}': {str(e)}", "error")
    return redirect(url_for('scan_s3'))

@app.route('/mitigate_cors/<bucket>', methods=['POST'])
@login_required
def mitigate_cors(bucket):
    access_key = session['access_key']
    secret_key = session['secret_key']
    s3_resource = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        cors_configuration = {
            'CORSRules': [{
                'AllowedHeaders': ['Authorization'],
                'AllowedMethods': ['GET'],
                'AllowedOrigins': ['https://secure.example.com'],
                'ExposeHeaders': ['x-amz-request-id'],
                'MaxAgeSeconds': 3000,
            }]
        }
        s3_resource.put_bucket_cors(
            Bucket=bucket,
            CORSConfiguration=cors_configuration
        )
        session['report_data'].append(f"S3 Bucket '{bucket}': CORS configuration applied.")
        flash(f"Successfully configured CORS for bucket '{bucket}'.", "success")
    except Exception as e:
        flash(f"Error configuring CORS for bucket '{bucket}': {str(e)}", "error")

    return redirect(url_for('scan_s3'))

@app.route('/mitigate_termination/<instance_id>', methods=['POST'])
@login_required
def mitigate_termination(instance_id):
    access_key = session['access_key']
    secret_key = session['secret_key']
    ec2_resource = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    try:
        ec2_resource.modify_instance_attribute(
            InstanceId=instance_id,
            DisableApiTermination={'Value': True}
        )
        session['report_data'].append(f"EC2 Instance '{instance_id}': Termination protection enabled.")
        flash(f"Successfully enabled termination protection for instance '{instance_id}'.", "success")
    except Exception as e:
        flash(f"Error enabling termination protection for instance '{instance_id}': {str(e)}", "error")
    return redirect(url_for('scan_ec2'))

@app.route('/mitigate_ssh/<instance_id>', methods=['POST'])
@login_required
def mitigate_ssh(instance_id):
    access_key = session['access_key']
    secret_key = session['secret_key']
    ec2_resource = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    try:
        instance = ec2_resource.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
        sg_id = instance['SecurityGroups'][0]['GroupId']
        ec2_resource.revoke_security_group_ingress(
            GroupId=sg_id,
            IpProtocol='tcp',
            FromPort=22,
            ToPort=22,
            CidrIp='0.0.0.0/0'
        )
        session['report_data'].append(f"EC2 Instance '{instance_id}': SSH access from 0.0.0.0/0 revoked.")
        flash(f"Successfully revoked SSH access from 0.0.0.0/0 for instance '{instance_id}'.", "success")
    except Exception as e:
        flash(f"Error revoking SSH access for instance '{instance_id}': {str(e)}", "error")
    return redirect(url_for('scan_ec2'))

@app.route('/download_report')
@login_required
def download_report():
    try:
        report_data = session.get('report_data', [])
        report_data.insert(0, f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        pdf_path = generate_pdf(report_data)
        if pdf_path:
            return send_file(pdf_path, as_attachment=True)
        else:
            flash("Failed to generate the PDF report. Check server logs for more details.", "error")
            return redirect(url_for('home'))
    except Exception as e:
        flash(f"Failed to generate report: {str(e)}", "error")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)