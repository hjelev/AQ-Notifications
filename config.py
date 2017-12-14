import  web
#configuration
alert_value = 100
ok_value = 50
api_url = "http://api.luftdaten.info/v1/sensor/"
air_map_url = "http://maps.luftdaten.info/#13/"
# configure smtp server for sending mail
web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'username@gmail.com'
web.config.smtp_password = 'password'
web.config.smtp_starttls = True
#Notification recipients
email_list =	[
					{"email":"username1@gmail.com", "station_id":"5690" },
					{"email":"username2@gmail.com", "station_id":"5690" },
					{"email":"username3@gmail.com", "station_id":"6771" },
					{"email":"username4@gmail.com", "station_id":"6195" },
				]
