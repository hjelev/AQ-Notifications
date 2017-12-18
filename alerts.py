from datetime import datetime

api_url = "http://api.luftdaten.info/v1/sensor/"
air_map_url = "http://maps.luftdaten.info/#13/"

AQI = [
		{"aqi": "0-50", "apl": "Good", 
		"health_implications": "Air quality is considered satisfactory, and air pollution poses little or no risk", 
		"cautionary_statement" : "None" 
		},		
		{"aqi": "51-100", "apl": "Moderate", 
		"health_implications": "Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.", 
		"cautionary_statement" : "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion" 
		},		
		{"aqi": "101-150", "apl": "Unhealthy for Sensitive Groups", 
		"health_implications": "Members of sensitive groups may experience health effects. The general public is not likely to be affected.",
		"cautionary_statement" : "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion." 
		},	
		{"aqi": "151-200", "apl": "Unhealthy", 
		"health_implications": "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects", 
		"cautionary_statement" : "Active children and adults, and people with respiratory disease, such as asthma, should avoid prolonged outdoor exertion; everyone else, especially children, should limit prolonged outdoor exertion" 
		},		
		{"aqi": "201-300", "apl": "Very Unhealthy", 
		"health_implications": "Health warnings of emergency conditions. The entire population is more likely to be affected.", 
		"cautionary_statement" : "Active children and adults, and people with respiratory disease, such as asthma, should avoid all outdoor exertion; everyone else, especially children, should limit outdoor exertion." 
		},		
		{"aqi": "300+", "apl": "Hazardous", 
		"health_implications": "Health alert: everyone may experience more serious health effects", 
		"cautionary_statement" : "Everyone should avoid all outdoor exertion" 
		},
	]

def alert_message(p1, p2, station_id, location):
	#get air pollutioin health message
	if p2 < 50:
		apl = AQI[0]['apl']
		health_implications = AQI[0]['health_implications']
		cautionary_statement = AQI[0]['cautionary_statement']
	elif p2 >= 50 and p2 <= 100:
		apl = AQI[1]['apl']
		health_implications = AQI[1]['health_implications']
		cautionary_statement = AQI[1]['cautionary_statement']
	elif p2 >= 101 and p2 <= 150:
		apl = AQI[2]['apl']
		health_implications = AQI[2]['health_implications']
		cautionary_statement = AQI[2]['cautionary_statement']
	elif p2 >= 151 and p2 <= 200:
		apl = AQI[3]['apl']
		health_implications = AQI[3]['health_implications']
		cautionary_statement = AQI[3]['cautionary_statement']		
	elif p2 >= 201 and p2 <= 300:
		apl = AQI[4]['apl']
		health_implications = AQI[4]['health_implications']
		cautionary_statement = AQI[4]['cautionary_statement']
	elif p2 > 300:
		apl = AQI[5]['apl']
		health_implications = AQI[5]['health_implications']
		cautionary_statement = AQI[5]['cautionary_statement']
	
	#read the html template 
	with open('templates/polluted_air.html', 'r') as templatefile:
		message = templatefile.readlines()
	#populate html template		
	message = "".join(message).format(	apl = apl,
					health_implications = health_implications,
					cautionary_statement = cautionary_statement,
					map_url = air_map_url + location.replace(",", "/"),
					today = datetime.today().strftime("%Y-%m-%d %H:%M"),
					p1 = p1,
					p2 = p2,
					stationid = station_id,
					location = location,
					)

	return message

def ok_message(ok_value, p1, p2, last_p1, last_p2, 
				station_id, last_alert_date, location):
	#read the html template 
	with open('templates/clear_air.html', 'r') as templatefile:
		message = templatefile.readlines()
		
	#populate html template				
	message = "".join(message).format(map_url = air_map_url + location.replace(",", "/"), 
					ok_value = ok_value,
					today = datetime.today().strftime("%Y-%m-%d %H:%M"),
					p1 = p1,
					p2 = p2,
					stationid = station_id,
					lastpolutiondate = last_alert_date,
					last_p1 = last_p1,
					last_p2 = last_p2,
					location = location
					)	

	return message