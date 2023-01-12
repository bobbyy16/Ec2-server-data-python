import requests
import smtplib
import os
import paramiko


EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

def send_notification(msg):
    # send email to me
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, "Subject: SITE DOWN\n Fix the issue")

try:
    response = requests.get('http://ec2-3-111-31-100.ap-south-1.compute.amazonaws.com:8080/')
    if response.status_code == 200:
        print("Application is running")
    else:
        print("Application down. Fix it")
        msg = f'Application returned {response.status_code}'
        send_notification(msg)

        # restart docker
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='3.111.31.100', username='root', key_filename='/home/abhishek/.ssh/id_rsa')
        stdin, stdout, stderr =  ssh.exec_command('docker ps')
        print(stdout.readlines())
        ssh.close()
        print('Application restarted')

except Exception as ex:
    print(f'Connection error happend {ex}')
    msg = "Subject: SITE DOWN\nApplication not accessible at all."
    send_notification(msg)