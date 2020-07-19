import time
import board
import busio
import adafruit_sgp30
import adafruit_si7021
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
print("SGP30 serial #", [hex(i) for i in sgp30.serial])
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8AAE)
sgp30.set_iaq_humidity(0.015)
#eCO2 = 0x8973, TVOC = 0x8aae
elapsed_sec = 0
while True:
	try:
		co2,tvoc = sgp30.iaq_measure() 
		print(f'eCO2 = {co2} ppm \t TVOC = {tvoc} ppb')
	except:
		print('reading error')
	time.sleep(1)
	elapsed_sec += 1
	if elapsed_sec > 10:
		elapsed_sec = 0
		try:	
			print(
		"**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
% (sgp30.baseline_eCO2, sgp30.baseline_TVOC))
		except:
			print("baseline error")
