import smtplib, email.message
from config import *

def send_email(message, subject, recipient):
	msg = email.message.Message()
	msg['Subject'] = subject
	msg['From'] = smtp_user
	msg['To'] = recipient
	msg.add_header('Content-Type','text/html')
	msg.set_payload(message)
	
	server = smtplib.SMTP(smtp_host, smtp_port)
	server.ehlo()
	server.starttls()
	server.login(smtp_user, smtp_password)
	server.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
	server.quit()
