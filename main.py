import time, sched
import board
import busio
import adafruit_sgp30
import adafruit_si7021
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import pytz


FIREBASE_UPDATE_SEC = 60
COLLECT_RECOVER_SEC = 1
local_time = pytz.timezone("America/Los_Angeles")
cred = credentials.Certificate('/home/pi/.ssh/firebase/greenhouse.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://greenhouse-85aa5.firebaseio.com'
})
s = sched.scheduler(time.time, time.sleep)
class SensorData:
	def __init__(self):
		self.firebaseref = db.reference('sensordata')
		self.i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
		self.sensor = adafruit_si7021.SI7021(self.i2c)
		# Create library object on our I2C port
		self.sgp30 = adafruit_sgp30.Adafruit_SGP30(self.i2c)
		print("SGP30 serial #", [hex(i) for i in self.sgp30.serial])
		self.sgp30.iaq_init()
		self.sgp30.set_iaq_baseline(0x8973, 0x8AAE)
		self.sgp30.set_iaq_humidity(0.015)			

	def collect(self,sc=None):
		sgp30 =  self.sgp30
		sensor = self.sensor
		firebaseref = self.firebaseref
		if sgp30.TVOC >= 0:
			try:
				utcdate = local_time.localize(datetime.now()).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S")
				firebaseref.update({
					utcdate:{
						'temp': sensor.temperature,
						'humid':sensor.relative_humidity,
						'co2':sgp30.eCO2,
						'tvoc':sgp30.TVOC,
						'imgpath': f'imgs/{utcdate}.png'
					# `	'imgpath': f'imgs/{utcdate}.png'
					}
				})
				print(f'saved data for {utcdate}')
				if sc:
					s.enter(FIREBASE_UPDATE_SEC, 1, self.collect, (sc,))
			except Exception as e:
				print(e)
		else:
			if sc:
				s.enter(COLLECT_RECOVER_SEC, 1, self.collect, (sc,))
			try:
				print(f'CO2 = {sgp30.eCO2} ppm \t TVOC = {sgp30.TVOC} ppb')
			except:
				print('co2 reading error')
			try:
				print(f'Temp ={sensor.temperature} \t Humid = {sensor.relative_humidity}')
			except:
				print('temp reading error')
	def loop(self):
		s.enter(0,1,data_collector.collect,(s,))
		s.run()
	def update_timeloop(self,event):
		global FIREBASE_UPDATE_SEC
		if isinstance(event.data,int) and event.data > 0 and not event.data == FIREBASE_UPDATE_SEC:
			print(event.data)
			FIREBASE_UPDATE_SEC = event.data
		self.firebaseref.child("updatesec").set(FIREBASE_UPDATE_SEC)
	def update(self, event):
		
		if event.data:
			print(event.data)
			self.collect()
		self.firebaseref.child("forceupdate").set(False)

data_collector = SensorData()
firebase_admin.db.reference('sensordata/forceupdate').listen(data_collector.update)
firebase_admin.db.reference('sensordata/updatesec').listen(data_collector.update_timeloop)
data_collector.loop()
