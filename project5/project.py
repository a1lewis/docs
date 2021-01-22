from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.TemperatureSensor import *
import time


intervals = 10


tempSensor = TemperatureSensor()
redLED = DigitalOutput()
greenLED = DigitalOutput()
redButton = DigitalInput()
greenButton = DigitalInput()

redLED.setHubPort(1)
redLED.setIsHubPortDevice(True)
greenLED.setHubPort(4)
greenLED.setIsHubPortDevice(True)
redButton.setHubPort(0)
redButton.setIsHubPortDevice(True)
greenButton.setHubPort(5)
greenButton.setIsHubPortDevice(True)

tempSensor.openWaitForAttachment(1000)
redLED.openWaitForAttachment(1000)
greenLED.openWaitForAttachment(1000)
redButton.openWaitForAttachment(1000)
greenButton.openWaitForAttachment(1000)

setTemp = 70
redIsPressed = False
greenIsPressed = False
timesRun = 0
originalTime = time.time()

currentPlural = "degrees"
setPlural = "degrees"

currentTemp = (tempSensor.getTemperature()) * (9 / 5) + 32
print("The current temperature is " + str(
    round(currentTemp, 2)) + " " + currentPlural + ". The temperature is set to " + str(
    setTemp) + " " + setPlural + ".")

while True:
    redButtonState = redButton.getState()
    greenButtonState = greenButton.getState()
    currentTemp = (tempSensor.getTemperature())*(9/5) + 32
    if redButtonState and not redIsPressed:
        setTemp -= 1
        redIsPressed = True
    if greenButtonState and not greenIsPressed:
        setTemp += 1
        greenIsPressed = True
    if not redButtonState and redIsPressed:
        redIsPressed = False
    if not greenButtonState and greenIsPressed:
        greenIsPressed = False

    minTemp = setTemp - 2
    maxTemp = setTemp + 2

    if (currentTemp <= minTemp) or (currentTemp >= maxTemp):
        redLED.setState(True)
        greenLED.setState(False)
    else:
        redLED.setState(False)
        greenLED.setState(True)
    timesRun += 1
    currentTime = time.time()
    if currentTemp == 1:
        currentPlural = "degree"
    if setTemp == 1:
        setPlural = "degree"
    if setTemp != 1:
        setPlural = "degrees"
    if currentTemp != 1:
        currentPlural = "degrees"
    if (currentTime - originalTime) >= intervals:
        print("The current temperature is " + str(
            round(currentTemp, 2)) + " " + currentPlural + ". The temperature is set to " + str(
            setTemp) + " " + setPlural + ".")
        log = open("project.log", "a")
        log.write(str(round(currentTime)) + ": Set temperature: "
                  + str(setTemp) + ", current temperature: " + str(round(currentTemp, 2)) + "\n")
        log.close()
        originalTime = currentTime
    time.sleep(0.015)  # Prevent crash from too much data going from the USB device into the computer (yes, it happened.)
