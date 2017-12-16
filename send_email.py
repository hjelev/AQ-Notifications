import smtplib, email.message
import config as gl

def send_email(message, subject, recipient):
	msg = email.message.Message()
	msg['Subject'] = subject
	msg['From'] = gl.config.smtp_user
	msg['To'] = recipient
	msg.add_header('Content-Type','text/html')
	msg.set_payload(message)
	
	server = smtplib.SMTP(gl.config.smtp_host, gl.config.smtp_port)
	server.ehlo()
	server.starttls()
	server.login(gl.config.smtp_user, gl.config.smtp_password)
	server.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
	server.quit()