import time
import board
import busio
import adafruit_sgp30
import adafruit_si7021
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Create library object on our I2C port
sensor = adafruit_si7021.SI7021(i2c)
while True:
	try:
		print("Temp =%d \t Humid = %d" % (sensor.temperature, sensor.relative_humidity))
	except:
		print('reading error')
	time.sleep(0.5)
