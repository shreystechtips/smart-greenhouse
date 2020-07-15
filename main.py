import time
import board
import busio
import adafruit_sgp30
import adafruit_si7021
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
sensor = adafruit_si7021.SI7021(i2c)
# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
print("SGP30 serial #", [hex(i) for i in sgp30.serial])
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8AAE)
elapsed_sec = 0
while True:
	try:
		print(f'CO2 = {sgp30.eCO2} ppm \t TVOC = {sgp30.TVOC} ppb')
	except:
		print('co2 reading error')
	try:
		print(f'Temp ={sensor.temperature} \t Humid = {sensor.relative_humidity}')
	except:
		print('temp reading error')
	time.sleep(0.5)
