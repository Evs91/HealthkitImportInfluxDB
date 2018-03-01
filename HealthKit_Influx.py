from xml.dom import minidom
from influxdb import InfluxDBClient

#variables
IP = ''
username = ''
password = ''
database_name = 'Healthkit'

#setup influx client
client = InfluxDBClient(IP, 8086, username, password, database_name)
client.create_database(database_name)

#parse xml and add to influx via API
xmldoc = minidom.parse('export.xml')
recordlist = xmldoc.getElementsByTagName('Record')
for s in recordlist:
    if s.attributes['type'].value == "HKQuantityTypeIdentifierHeartRate":
        HealthKitTimeStamp = s.attributes['startDate'].value
        AppleWatchHRValue = s.attributes['value'].value
        json_body = [{"measurement": "heartrate","tags": {"service": "HealthKit","person": "Everett"},"time": HealthKitTimeStamp,"fields": {"watch_heartrate": float(AppleWatchHRValue)}}]
        client.write_points(json_body)
    else:
        pass