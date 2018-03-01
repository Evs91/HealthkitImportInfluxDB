from xml.dom import minidom
from influxdb import InfluxDBClient

#variables
IP = '127.0.0.1'
USERNAME = 'admin'
PASSWORD = 'admin'
DB_NAME = 'Healthkit'
NAME = 'MyNameHere'

#setup influx client
client = InfluxDBClient(IP, 8086, USERNAME, PASSWORD, DB_NAME)
client.create_database(DB_NAME)

#parse xml and add to influx via API
xmldoc = minidom.parse('export.xml')
recordlist = xmldoc.getElementsByTagName('Record')
for s in recordlist:
    if s.attributes['type'].value == "HKQuantityTypeIdentifierHeartRate":
        HealthKitTimeStamp = s.attributes['startDate'].value
        AppleWatchHRValue = s.attributes['value'].value
        json_body = [{"measurement": "heartrate","tags": {"service": "HealthKit","person": NAME},"time": HealthKitTimeStamp,"fields": {"watch_heartrate": float(AppleWatchHRValue)}}]
        client.write_points(json_body)
    else:
        pass