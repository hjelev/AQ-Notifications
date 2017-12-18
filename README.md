# AQ-Notifications
Python script to check air pollution data and sent email alerts.

With this script you can monitor multiple airpolution sensors from http://maps.luftdaten.info and get email alerts.
There are two type of alerts. The first one is send when the air is polluted and the second when the pollution is over.

The script will create a csv file for each airpolution sensor you track and use it to store the alerts data.

# Installation

To install the script clone this reporitory, fill the configuration vairables in config.py.example and rename it to config.py .

To get your sensor_id (this is the air quality sensor for your location) go to http://maps.luftdaten.info,
navigate to your location, click on the colored hexagon that is located near you and get Station ID.

Finally set a cron job to execute app.py each hour or more often depending on your needs:

1 */1 * * * /usr/bin/python3 /path/to/app.py
