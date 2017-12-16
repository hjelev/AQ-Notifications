from datetime import datetime

api_url = "http://api.luftdaten.info/v1/sensor/"
air_map_url = "http://maps.luftdaten.info/#13/"

def alert_message(p1, p2, station_id, location):
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
		'''.format(map_url = air_map_url + location.replace(",", "/"),
					today = datetime.today().strftime("%Y-%m-%d %H:%M"),
					p1 = p1,
					p2 = p2,
					stationid = station_id,
					location = location
					)
	return message

def ok_message(ok_value, p1, p2, last_p1, last_p2, 
				station_id, last_alert_date, location):
	#compose email body for clear air alert
	message = '''
		<!DOCTYPE html>
		<html>
			<head>
			</head>
			<body>
				<h1>Clear Air Alert!</h1>
				<h2>The amount of PM2.5 is below {ok_value} µg/m³</h2> <br>
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
				<small>
					Latest air pollution was on {lastpolutiondate}<br>
					<br>
					PM10 = {last_p1} µg/m³<br>
					PM2.5 = {last_p2} µg/m³<br>
				</small>
			</body>
		</html>
		'''.format(map_url = air_map_url + location.replace(",", "/"), 
					ok_value = ok_value,
					today = datetime.today().strftime("%Y-%m-%d %H:%M"),
					p1 = p1,
					p2 = p2,
					stationid = station_id,
					lastpolutiondate = last_alert_date,
					last_p1 = last_p1,
					last_p2 = last_p2,
					location = location)	
	return message