import urllib.request, json, csv, os, re
from collections import deque
from dateutil import parser
from datetime import datetime
#import configuration variables
from config import *

# todo alerts sev text http://aqicn.org/data-platform/register/

#read air data from joson and get average values
def get_air_data(station_id):
	p1, p2 = [],[]
	with urllib.request.urlopen(api_url+station_id+"/") as url:
		data = json.loads(url.read().decode())
		for results in data:			
			timestamp = results['timestamp']
			if 'sensordatavalues' in results:
				location = results['location']['latitude']+","+results['location']['longitude']
				for readings in results['sensordatavalues']:
					if readings['value_type'] == 'P1':
						p1.append(float(readings['value']))
						
					elif readings['value_type'] == 'P2':
						p2.append(float(readings['value']))						
	print(p1, p2, location)
	return int(sum(p1)/len(p1)), int(sum(p2)/len(p2)), timestamp, location

# Save the air data to csv
def write_to_csv(p1,p2,timestamp,csv_path):
	with open(csv_path,"a") as csv_file:
		csv_app = csv.writer(csv_file)
		csv_app.writerow([p1,p2,timestamp])
		
# Read the last record from csv and get last alert date
def get_last_row(csv_filename, p1, p2):
	try:
		with open(csv_filename, 'r') as f:
			try:
				lastrow = deque(csv.reader(f), 1)[0]
			except IndexError:  # empty file
				lastrow = None
			return lastrow[0], lastrow[1], lastrow[2]
			
	except FileNotFoundError:
		write_to_csv(p1, p2, datetime.today().strftime("%Y-%m-%d %H:%M"), csv_filename)
		return p1, p2, datetime.today().strftime("%Y-%m-%d %H:%M")
		
#Check if there was an alert today
def alert_today(adate):	
	if (datetime.today() - adate).days == 0:
		return True
	else:
		return False

#Send email notification
def send_message(message,subject,recipient):
	web.sendmail(web.config.smtp_username, recipient, subject, message, headers={'Content-Type':'text/html;charset=utf-8'})
#	print(recipient,subject)

#make sure the folder exists
def check_dir(file_path):
	directory = os.path.dirname(file_path)
	try:
		os.stat(directory)
	except:
		os.mkdir(directory) 	

def alert_message(p1, p2, station_id,location):
	#compose email body from air polution alert
	message = '''
		<h1>High Air Pollution alert!</h1><br>
		Alert Date {today} <br>
		<p>PM10 = {p1} µg/m³ <br> PM2.5 = {p2} µg/m³ </p>
		<img src="https://api.luftdaten.info/grafana/render/dashboard-solo/db/single-sensor-view?orgId=1&panelId=2&width=300&height=200&tz=UTC%2B02%3A00&var-node={stationid}">
		<br>
		<small>
		PM10 -  fine particles with a diameter of 10 μm or less
		<br>
		PM2.5 -  fine particles with a diameter of 2.5 μm or less
		</small>
		<br><br>
		Sensor Location<br>
		<a href="{map_url}">
		<img src="https://maps.googleapis.com/maps/api/staticmap?center={location}&zoom=12&size=300x200&maptype=roadmap&markers=color:blue%7Clabel:S%7C{location}&markers=color:red%7C&key=AIzaSyBmdDFqNyjLOUUwMzXmskur36QdbF4oPao">
		</a>
		<br>
		'''.format(map_url = air_map_url+location.replace(",","/"), today=datetime.today().strftime("%Y-%m-%d %H:%M"), p1=p1, p2=p2, stationid=station_id,location=location)
	return message

def ok_message(ok_value, p1, p2, last_p1, last_p2, station_id, last_alert_date, location):
	#compose email body for clear air alert
	message = '''
		<!DOCTYPE html>
		<html>
			<head>
			</head>
			<body>
				<h1>Clear Air Alert!</h1>
				<h2>The amount of pm2.5 is below {ok_value} µg/m³</h2> <br>
				Alert Date {today} <br>
				<p>PM10 = {p1} µg/m³ <br> PM2.5 = {p2} µg/m³ </p>
				<img src="https://api.luftdaten.info/grafana/render/dashboard-solo/db/single-sensor-view?orgId=1&panelId=2&width=300&height=200&tz=UTC%2B02%3A00&var-node={stationid}">
					<small>
					PM10 -  fine particles with a diameter of 10 μm or less
					<br>
					PM2.5 -  fine particles with a diameter of 2.5 μm or less
				</small>
				<br><br>
				Sensor Location<br>
				<a href="{map_url}">
				<img src="https://maps.googleapis.com/maps/api/staticmap?center={location}&zoom=12&size=300x200&maptype=roadmap&markers=color:blue%7Clabel:S%7C{location}&markers=color:red%7C&key=AIzaSyBmdDFqNyjLOUUwMzXmskur36QdbF4oPao">
				</a>
				<br>
					<small>
					Latest air pollution was on {lastpolutiondate}<br>
					<br>
					PM10 = {last_p1} µg/m³<br>
					PM2.5 = {last_p2} µg/m³<br>
				</small>
			</body>
		</html>
		'''.format( map_url = air_map_url+location.replace(",","/"), ok_value=ok_value, today=datetime.today().strftime("%Y-%m-%d %H:%M"), p1=p1, p2=p2, stationid=station_id,lastpolutiondate = last_alert_date, last_p1 = last_p1, last_p2 = last_p2,location=location )	
	return message
	
def main(user):
	#get air pollution data
	p1, p2, timestamp, location = get_air_data(user['station_id'])
	
	# Get last data from the last record in the csv file for the current user
	csv_path = os.path.dirname(os.path.realpath(__file__))+"/"+csv_data_folder+"/"+"air_data_" + user['station_id'] +"-"+ user['email'].replace('@', '-')+".csv"
	
	#make sure the folder for the csv files exists
	check_dir(csv_path)
	
	#read the last record from the csv file
	last_p1, last_p2, last_alert_date = get_last_row(csv_path, p1, p2)

#	p2 = 241 # current value of pm2.5 comment used for tests	
#	last_p2 = 20 # previous value of pm2.5 comment used for tests
	
	#print(air_map_url+location.replace(",","/"))
	
	#pollution is high
	if p2 > alert_value:
		#print('We need to send an alert')		
		# Check if there was an alert today and if its value is  > alert_value - no alert is send
		if int(last_p2) > alert_value and p2 > int(last_p2):
			#record the new higher value
			write_to_csv(p1, p2, timestamp, csv_path)
		#check if last alert was positive and send polution alert		
		elif int(last_p2) < ok_value:
			#sends email notifications
			send_message(alert_message(p1, p2, user['station_id'], location), "Air Pollution Alert!", user['email'])
			#write new alert record to csv file
			write_to_csv(p1, p2, timestamp, csv_path)
	#check if polution is OK					
	elif p2 < ok_value:
		#check if last alert was negative and send clear air alert 
		if int(last_p2) > ok_value:
			#we need to send clear air alert
			send_message(ok_message(ok_value, p1, p2, last_p1, last_p2, user['station_id'], last_alert_date, location), "Clear Air Alert!", user['email'])
			#write new record to csv file
			write_to_csv(p1, p2, timestamp, csv_path)
	return
	
if __name__ == '__main__':	
	for user in email_list:
#		main(user)
		try:
			main(user)
		except:
			print("Problem with user: ", user)