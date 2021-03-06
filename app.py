"""
Python script to check air pollution data and sent email alerts.
"""

import urllib.request, json, csv, os , logging, smtplib, email.message, time
from collections import deque
from datetime import datetime
from functools import reduce

import config as gl
from alerts import *

# read air data from json api and return average values
def get_air_data(sensor_id):
	p1, p2 = [], []
	try:
		with urllib.request.urlopen(gl.config.api_url + sensor_id + "/") as url:
			data = json.loads(url.read().decode())
			#we need this as there are multiple sensor readings in the api response
			for results in data:			
				timestamp = results['timestamp']
				if 'sensordatavalues' in results:
					location = (results['location']['latitude']
								+ ","
								+ results['location']['longitude'])
					for readings in results['sensordatavalues']:
						if readings['value_type'] == 'P1':
							p1.append(float(readings['value']))	
						elif readings['value_type'] == 'P2':
							p2.append(float(readings['value']))						
		average_p1 = int(reduce(lambda x, y: x + y / float(len(p1)), p1, 0))
		average_p2 = int(reduce(lambda x, y: x + y / float(len(p2)), p2, 0))
	except:
		pass
		average_p1, average_p2 = 0, 0
		#raise RuntimeError('Problem with sensor ID: {}'.format(sensor_id))
	return average_p1, average_p2, timestamp, location

# save sensor data to a csv file
def write_to_csv(p1, p2, timestamp, csv_path):
	with open(csv_path, "a") as csv_file:
		csv_app = csv.writer(csv_file)
		csv_app.writerow([p1, p2, timestamp])
		
# read the last record and alert date
def get_last_row(csv_filename, p1, p2):
	try:
		with open(csv_filename, 'r') as f:
			try:
				lastrow = deque(csv.reader(f), 1)[0]
			except IndexError:  # empty file
				lastrow = None
			return lastrow[0], lastrow[1], lastrow[2]
	# the file does not exist and we need to create
	except FileNotFoundError:
		write_to_csv(
			p1, p2,
			datetime.today().strftime("%Y-%m-%d %H:%M"),
			csv_filename
			)
		return p1, p2, datetime.today().strftime("%Y-%m-%d %H:%M")

# make sure the folder from file_path exists
def check_dir(file_path):
	directory = os.path.dirname(file_path)
	try:
		os.stat(directory)
	except:
		os.mkdir(directory) 	
		
# enable logging stored in file logs_file_name
def enable_logging():	
	log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
				gl.config.logs_file_name
				)		
	logging.basicConfig(filename=log_path,
						format='%(asctime)s %(message)s',
						datefmt='%m/%d/%Y %I:%M:%S %p',
						level=logging.INFO
						)
						
# send the notification					
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

# decide if a notification is needed
def main(user):
	# get current air pollution data
	p1, p2, timestamp, location = get_air_data(user['sensor_id'])	

	csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)) ,
				gl.config.csv_data_folder ,
				"air_data_{}-{}.csv".format(
						user['sensor_id'],
						user['email'].replace('@', '-')
					)
				)

	check_dir(csv_path)
	# get previus air data from the csv file for the current user
	last_p1, last_p2, last_alert_date = get_last_row(csv_path, p1, p2)

	#p2 = 127 # current value of pm2.5 comment used for tests	
	#last_p2 = 12 # previous value of pm2.5 comment used for tests
	
	# check if there is air pollution
	if p2 > gl.config.alert_value:	
		# check if there was a pollution alert already send
		# - no alert is send
		if int(last_p2) > gl.config.alert_value and p2 > int(last_p2):
			write_to_csv(p1, p2, timestamp, csv_path)
		# check if last alert was positive and
		# send polution alert		
		elif int(last_p2) < gl.config.ok_value:
			send_email(alert_message(p1, p2, user['sensor_id'], location),
							"Air Pollution Alert!",
							user['email']
							)
			logging.info("- Polluted Air Alert sent to {} ".format(user['email'])
							+"PM10= {} PM2.5={}".format(p1, p2,))
			write_to_csv(p1, p2, timestamp, csv_path)
	# check if air is clear	and last alert was negative
	# - send clear air alert	
	elif p2 < gl.config.ok_value and int(last_p2) > gl.config.ok_value:
		send_email(ok_message(gl.config.ok_value, p1, p2,
									last_p1, last_p2,
									user['sensor_id'],
									last_alert_date,
									location
									),
								"Clear Air Alert!",
								user['email']
								)
		logging.info("- Clear Air Alert sent to {} ".format(user['email'])
						+ "PM10= {} PM2.5={}".format(p1, p2,))
		write_to_csv(p1, p2, timestamp, csv_path)
	return
						
if __name__ == '__main__':
	enable_logging()
	#run the code for all recipents of email_list
	for user in gl.config.email_list:
		#main(user)
		try:
			main(user)
			# wait 1 second to avoid api errors
			time.sleep(1)
		except Exception as e:
			print("Problem with user: ", user['email'],e)
			#logging.error("Problem with user: {} {}".format(user['email'], e))
			#send_email(str(e),"Problem with user: {}".format(user['email']),gl.config.email_list[0]['email'])