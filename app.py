import urllib.request, json, csv, os #, re
from collections import deque
from datetime import datetime
# import configuration variables
from alerts import *
from send_email import *
# todo alerts sev text http://aqicn.org/data-platform/register/

# read air data from json api and return average values
def get_air_data(station_id):
	p1, p2 = [], []
	with urllib.request.urlopen(api_url + station_id + "/") as url:
		data = json.loads(url.read().decode())
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
	print(p1, p2, location)
	return int(sum(p1) / len(p1)), int(sum(p2) / len(p2)), timestamp, location

# save the air data to a csv file
def write_to_csv(p1, p2, timestamp, csv_path):
	with open(csv_path, "a") as csv_file:
		csv_app = csv.writer(csv_file)
		csv_app.writerow([p1, p2, timestamp])
		
# read the last record from csv and get last alert date
def get_last_row(csv_filename, p1, p2):
	try:
		with open(csv_filename, 'r') as f:
			try:
				lastrow = deque(csv.reader(f), 1)[0]
			except IndexError:  # empty file
				lastrow = None
			return lastrow[0], lastrow[1], lastrow[2]
	# the file does not exist and we need to create it		
	except FileNotFoundError:
		write_to_csv(
			p1, p2,
			datetime.today().strftime("%Y-%m-%d %H:%M"),
			csv_filename
			)
		return p1, p2, datetime.today().strftime("%Y-%m-%d %H:%M")


# make sure the folder exists
def check_dir(file_path):
	directory = os.path.dirname(file_path)
	try:
		os.stat(directory)
	except:
		os.mkdir(directory) 	
	
def main(user):
	# get air pollution data
	p1, p2, timestamp, location = get_air_data(user['station_id'])	
	# Build the path to the csv file with previous air data
	csv_path = (os.path.dirname(os.path.realpath(__file__)) 
				+ "/" + csv_data_folder 
				+ "/air_data_" + user['station_id'] +"-" 
				+ user['email'].replace('@', '-') + ".csv"
				)
	# make sure the folder for the csv files exists
	check_dir(csv_path)
	# get last data from the last record in the csv file for the current user
	last_p1, last_p2, last_alert_date = get_last_row(csv_path, p1, p2)

	#p2 = 2 # current value of pm2.5 comment used for tests	
	#last_p2 = 202 # previous value of pm2.5 comment used for tests
	
	# pollution is high
	if p2 > alert_value:	
		# check if there was an alert today and if its value is > alert_value
		# - no alert is send
		if int(last_p2) > alert_value and p2 > int(last_p2):
			# record the new higher value
			write_to_csv(p1, p2, timestamp, csv_path)
		# check if last alert was positive and send polution alert		
		elif int(last_p2) < ok_value:
			# sends email notifications
			send_email(alert_message(p1, p2, user['station_id'], location),
							"Air Pollution Alert!",
							user['email']
							)
			# write new alert record to csv file
			write_to_csv(p1, p2, timestamp, csv_path)
	# check if polution is OK					
	elif p2 < ok_value:
		# check if last alert was negative and send clear air alert 
		if int(last_p2) > ok_value:
			# we need to send clear air alert
			send_email(ok_message(ok_value, p1, p2,
										last_p1, last_p2,
										user['station_id'],
										last_alert_date,
										location
										),
									"Clear Air Alert!",
									user['email']
									)
			# write new clear air record to the csv file
			write_to_csv(p1, p2, timestamp, csv_path)
	return
	
if __name__ == '__main__':	
	for user in email_list:
		#main(user)
		try:
			main(user)
		except:
			print("Problem with user: ", user)