from xml.dom import minidom
from influxdb import InfluxDBClient

#variables
IP = ''
USERNAME = 'admin'
PASSWORD = 'admin'
DB_NAME = 'Healthkit'
NAME = 'Username'

#setup influx client
client = InfluxDBClient(IP, 8086, USERNAME, PASSWORD, DB_NAME)
client.create_database(DB_NAME)

#heartrate
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

#distance walked
for distance in recordlist:
    if distance.attributes['type'].value == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
        HealthKitTimeStamp = distance.attributes['startDate'].value
        HealthKitDist = distance.attributes['value'].value
        source_device = distance.attributes['sourceName'].value
        json_body = [
            {"measurement": "steps", "tags": {"service": "HealthKit", "person": NAME, "source": source_device}, "time": HealthKitTimeStamp, "fields": {"miles": float(HealthKitDist)}}]
        client.write_points(json_body)
    else:
        pass

#basal calories
for basal in recordlist:
    if basal.attributes['type'].value == 'HKQuantityTypeIdentifierBasalEnergyBurned':
        HealthKitTimeStamp = basal.attributes['startDate'].value
        HealthKitBasal = basal.attributes['value'].value
        source_device = basal.attributes['sourceName'].value
        json_body = [
            {"measurement": "BasalCalories", "tags": {"service": "HealthKit", "person": NAME, "source": source_device}, "time": HealthKitTimeStamp, "fields": {"basal_kcal": float(HealthKitBasal)}}]
        client.write_points(json_body)
    else:
        pass

#active calories
for active in recordlist:
    if active.attributes['type'].value == 'HKQuantityTypeIdentifierActiveEnergyBurned':
        HealthKitTimeStamp = active.attributes['startDate'].value
        HealthKitActive = active.attributes['value'].value
        source_device = active.attributes['sourceName'].value
        json_body = [
            {"measurement": "ActiveCalories", "tags": {"service": "HealthKit", "person": NAME, "source": source_device}, "time": HealthKitTimeStamp, "fields": {"active_kcal": float(HealthKitActive)}}]
        client.write_points(json_body)
    else:
        pass