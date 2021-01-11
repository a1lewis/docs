from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.DigitalOutput import *
import time

# Create objects for the inputs and outputs
redLED = DigitalOutput()
greenLED = DigitalOutput()
tempSensor = TemperatureSensor()

# Set addresses
redLED.setHubPort(1)  # Red LED plugged into port 1
redLED.setIsHubPortDevice(True)
greenLED.setHubPort(4)  # Green LED plugged into port 4
greenLED.setIsHubPortDevice(True)

# Open the connections to the inputs/outputs
redLED.openWaitForAttachment(1000)
greenLED.openWaitForAttachment(1000)
tempSensor.openWaitForAttachment(1000)

# Print tempSensor output
while True:
    celsiusTemp = tempSensor.getTemperature()
    fahrenheitTemp = celsiusTemp*(9/5)+32
    roundedFahrenheitTemp = round(fahrenheitTemp, 2)
    print(roundedFahrenheitTemp)
    # Set lights
    if (fahrenheitTemp > 68) and (fahrenheitTemp < 75):
        redLED.setState(False)
        greenLED.setState(True)
    else:
        redLED.setState(True)
        greenLED.setState(False)
    # Add to log file
    log = open("/Users/andrew/Desktop/temp_history.log", "a")
    log.write(str(round(time.time())) + ": " + str(roundedFahrenheitTemp) + "\n")
    log.close()
    time.sleep(1)
