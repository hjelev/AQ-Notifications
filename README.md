# AQ-Notifications
Python script to check air pollution data and sent email alerts
# AQ-Notification

To install the script fill the configuration vairables in config.py.example and rename it ot config.py .

Install web.py http://webpy.org/install which is used for sending the email notifications.

Set a cron job to execute app.py each hour:

1 */1 * * * /usr/bin/python3 /path/to/app.py
