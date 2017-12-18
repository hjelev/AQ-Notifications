# AQ-Notifications
Python script to check air pollution data and sent email alerts.

With this script you can monitor multiple airpollution sensors from http://maps.luftdaten.info and get email alerts.
There are two type of alerts. The first one is send when the air is polluted and the second when the pollution is over.

The script will create a csv file for each airpolution sensor you track and use it to store the alerts data.

# Installation

1. Clone the reporitory
2. Open config.py.example and configure your data, then save it as config.py
3. Set a cron job to execute app.py each hour or more often depending on your needs 
4. Test the cron to make sure the script works properly

Cronjob Example

#run once each hour
1 */1 * * * /usr/bin/python3 /path/to/app.py



To get your sensor_id (this is the air quality sensor for your location) go to http://maps.luftdaten.info,
navigate to your location, click on the colored hexagon that is located near you and get Station ID.