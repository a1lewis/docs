# Import statements, to allow the code access to the Phidget box thing
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.DigitalInput import *
import time

# Create objects for the inputs and outputs
redLED = DigitalOutput()
greenLED = DigitalOutput()
redButton = DigitalInput()
greenButton = DigitalInput()

# Set addresses
redLED.setHubPort(1)  # Red LED plugged into port 1
redLED.setIsHubPortDevice(True)
greenLED.setHubPort(4)  # Green LED plugged into port 4
greenLED.setIsHubPortDevice(True)
redButton.setHubPort(0)  # Red button plugged into port 0
redButton.setIsHubPortDevice(True)
greenButton.setHubPort(5)  # Green button plugged into port 5
greenButton.setIsHubPortDevice(True)

# Open the connections to the inputs/outputs
redLED.openWaitForAttachment(1000)
greenLED.openWaitForAttachment(1000)
redButton.openWaitForAttachment(1000)
greenButton.openWaitForAttachment(1000)


# Countdown
print("3...")
time.sleep(1)
print("2...")
time.sleep(1)
print("1...")
time.sleep(1)
print("Go!!")

# Set variables for game

redIsPressed = False
greenIsPressed = False
redScore = 0
greenScore = 0
winner = False
winnerColor = ""

# Run the game

while not winner:  # Runs if nobody has won the game yet
    redButtonState = redButton.getState()
    greenButtonState = greenButton.getState()

    if redButtonState and not redIsPressed:  # Checks if the red button is pressed and it was not previously pressed
        redIsPressed = True  # Set the button state to true so the code can check next time
        redLED.setState(True)  # Turn on the red LED
        redScore += 1  # Add one to the red score
    if not redButtonState and redIsPressed:  # Checks if the red button is not pressed and it was previously pressed
        redIsPressed = False  # Sets the button state to false so the code can check next time
        redLED.setState(False)  # Turn off the red LED
    if greenButtonState and not greenIsPressed:
        greenIsPressed = True
        greenLED.setState(True)
        greenScore += 1
    if not greenButtonState and greenIsPressed:
        greenIsPressed = False
        greenLED.setState(False)
    if (redScore >= 10) or (greenScore >= 10):
        # Set the 'winner' variable to True, so the code does not run again
        winner = True
        # Set a variable so the code can announce the winner later.
        # This is biased towards red in case of both winning at the same time, but it's the easiest thing I can think of
        if redScore >= 10:
            winnerColor = "red"
        elif greenScore >= 10:
            winnerColor = "green"

# Turn off the lights that are on
redLED.setState(False)
greenLED.setState(False)
time.sleep(2)  # Delay

# Flash both lights once
redLED.setState(True)
greenLED.setState(True)
time.sleep(1)
redLED.setState(False)
greenLED.setState(False)
time.sleep(1)

# Flash winner's LED 5 times
flashes = 0
while flashes < 5:
    if winnerColor == "red":
        redLED.setState(True)
        time.sleep(0.5)
        redLED.setState(False)
        time.sleep(0.5)
        flashes += 1
    if winnerColor == "green":
        greenLED.setState(True)
        time.sleep(0.5)
        greenLED.setState(False)
        time.sleep(0.5)
        flashes += 1
