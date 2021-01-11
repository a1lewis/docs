# Import Modules
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.DigitalInput import *
import time  # control amount of time that commands work for
from playsound import playsound
import pyttsx3

# Config
ttsChoice = False  # Set to True if you would like the announcer to announce the game, this also enables/disables totals
soundChoice = True  # Set to True if you would like to hear sounds
customThreshold = 10  # Sets the number of points to win by in a compete game

# Start TTS Engine
if ttsChoice:
    engine = pyttsx3.init()
else:
    print("Skipped TTS startup")

# Set main variables
run = 0
playerOneGamesWon = 0
playerTwoGamesWon = 0

# Configure variables
flashTime = 0.175

# Create LED object
redLED = DigitalOutput()
greenLED = DigitalOutput()
redButton = DigitalInput()
greenButton = DigitalInput()

# Set Address
redLED.setHubPort(1)  # Red LED plugged into port 1
redLED.setIsHubPortDevice(True)
greenLED.setHubPort(4)
greenLED.setIsHubPortDevice(True)
redButton.setHubPort(0)
redButton.setIsHubPortDevice(True)
greenButton.setHubPort(5)
greenButton.setIsHubPortDevice(True)

# Open the connection
redLED.openWaitForAttachment(1000)
greenLED.openWaitForAttachment(1000)
redButton.openWaitForAttachment(1000)
greenButton.openWaitForAttachment(1000)


# Create flash-win functions
def red_win_flash():
    times_flashed = 0
    while times_flashed < 5:
        redLED.setState(True)
        time.sleep(0.1)
        redLED.setState(False)
        time.sleep(0.1)
        times_flashed = times_flashed + 1


def green_win_flash():
    times_flashed = 0
    while times_flashed < 5:
        greenLED.setState(True)
        time.sleep(0.1)
        greenLED.setState(False)
        time.sleep(0.1)
        times_flashed = times_flashed + 1


# Start game
print("Starting game?")
if ttsChoice:
    engine.say("Press both buttons to start a new game.")
    engine.runAndWait()
else:
    print("Press both buttons to start a new game.")
test = 1
while test == 1:
    redButtonState = redButton.getState()
    greenButtonState = greenButton.getState()
    if redButtonState and greenButtonState:
        if soundChoice:
            playsound("/Users/Andrew/Downloads/level-pop-4-music-089278720_prev.mp3", False)
        print("Starting game!")
        test = 0

# Flash Lights
x = 0
while x < 5:
    redLED.setState(True)
    time.sleep(flashTime)
    redLED.setState(False)
    greenLED.setState(True)
    time.sleep(flashTime)
    greenLED.setState(False)
    x = x + 1
while run == 0:
    # Select game mode
    if ttsChoice:
        engine.say("Select a game mode. Press the red button for speed mode, or the green button for compete mode.")
        engine.runAndWait()
    else:
        print("Select a game mode. Press the red button for speed mode, or the green button for compete mode.")
    totalButtonPresses = 0
    gameMode = 2
    # Game mode 0 = speed, Game mode 1 = compete, Game mode 2 = Setup
    while totalButtonPresses == 0:
        greenButtonState = greenButton.getState()
        redButtonState = redButton.getState()
        if redButtonState and (not greenButtonState):
            totalButtonPresses = 1
            if soundChoice:
                playsound("/Users/Andrew/Downloads/level-pop-4-music-089278720_prev.mp3", False)
            gameMode = 0
            redLED.setState(True)
            time.sleep(0.25)
            redLED.setState(False)
            if ttsChoice:
                engine.say("Game mode selected: speed mode! First to ten points wins!")
                engine.runAndWait()
            else:
                print("Game mode selected: speed mode! First to ten points wins!")
        if greenButtonState and (not redButtonState):
            if soundChoice:
                playsound("/Users/Andrew/Downloads/level-pop-4-music-089278720_prev.mp3", False)
            totalButtonPresses = 1
            gameMode = 1
            greenLED.setState(True)
            time.sleep(0.25)
            greenLED.setState(False)
            if ttsChoice:
                engine.say("Game mode selected: Compete mode! First to ten points more than the other wins!")
                engine.runAndWait()
            else:
                print("Game mode selected: Compete mode: First to ten points more than the other wins!")

    # Select players
    if ttsChoice:
        engine.say("Player one, select your color.")
        engine.runAndWait()
    else:
        print("Player one, select your color.")
    playerOne = 0
    redButtonPresses = 0
    greenButtonPresses = 0
    totalButtonPresses = 0
    while totalButtonPresses == 0:
        redButtonState = redButton.getState()
        if redButtonState:
            redButtonPresses = redButtonPresses + 1
            totalButtonPresses = totalButtonPresses + 1
            redLED.setState(True)
        greenButtonState = greenButton.getState()
        if greenButtonState:
            greenButtonPresses = greenButtonPresses + 1
            totalButtonPresses = totalButtonPresses + 1
            greenLED.setState(True)
        time.sleep(0.02)
    if redButtonPresses == 1 and greenButtonPresses == 0:
        if ttsChoice:
            engine.say("Player one has chosen red.")
            engine.runAndWait()
        else:
            print("Player one has chosen red.")
            time.sleep(1)
        playerOne = 1
        redLED.setState(False)
        greenLED.setState(True)
        if ttsChoice:
            engine.say("Player two, you have been assigned to green.")
            engine.runAndWait()
        else:
            print("Player two, you have been assigned to green.")
            time.sleep(1)
        greenLED.setState(False)
        print("P1R P2G")
    elif greenButtonPresses == 1 and redButtonPresses == 0:
        if ttsChoice:
            engine.say("Player one has chosen green.")
            engine.runAndWait()
        else:
            print("Player one has chosen green.")
            time.sleep(1)
        playerOne = 2
        greenLED.setState(False)
        redLED.setState(True)
        if ttsChoice:
            engine.say("Player two, you have been assigned to red.")
            engine.runAndWait()
        else:
            print("Player two, you have been assigned to red.")
            time.sleep(1)
        redLED.setState(False)
        print("P1G P2R")
    else:
        print("Only click one button!")
        print("Hmmph. Start over. :(")
        exit()

    # Await game start
    redIsPressed = False
    greenIsPressed = False
    redScore = 0
    greenScore = 0
    winner = False
    if ttsChoice:
        engine.say("Game will start when the lights come on. "
                   + "Game will stop when the lights stop reacting to your button presses.")
        engine.runAndWait()
    else:
        print("Game will start when the lights come on. "
              + "Game will stop when the lights stop reacting to your button presses.")
    time.sleep(2)

    # Start game
    print("Go!")
    redLED.setState(True)
    greenLED.setState(True)
    while not winner:
        redButtonState = redButton.getState()
        greenButtonState = greenButton.getState()
        if redButtonState and not redIsPressed:
            redIsPressed = True
            redLED.setState(False)
            redScore = redScore + 1
        if not redButtonState and redIsPressed:
            redIsPressed = False
            redLED.setState(True)
        if greenButtonState and not greenIsPressed:
            greenIsPressed = True
            greenLED.setState(False)
            greenScore = greenScore + 1
        if not greenButtonState and greenIsPressed:
            greenIsPressed = False
            greenLED.setState(True)
        if gameMode == 0:
            if redScore >= 10:
                winner = True
                print("Red win with 10 points")
            if greenScore >= 10:
                winner = True
                print("Green win with 10 points")
        if gameMode == 1:
            if redScore >= greenScore + customThreshold:
                winner = True
                print("Red win: " + str(redScore))
            if greenScore >= redScore + customThreshold:
                winner = True
                print("Green win: " + str(greenScore))

    # Play win sound
    if soundChoice:
        playsound("/Users/Andrew/Downloads/341985__unadamlar__goodresult.wav", False)

    # Flash Lights
    redLED.setState(False)
    greenLED.setState(False)
    time.sleep(0.25)
    redLED.setState(True)
    greenLED.setState(True)
    time.sleep(1)
    redLED.setState(False)
    greenLED.setState(False)
    timesFlashed = 0
    while timesFlashed < 5:
        time.sleep(0.175)
        redLED.setState(True)
        greenLED.setState(True)
        time.sleep(0.175)
        redLED.setState(False)
        greenLED.setState(False)
        timesFlashed = timesFlashed + 1

    # Announce Winner
    if ttsChoice:
        engine.say("The winner is...")
        engine.runAndWait()
        if gameMode == 1:
            if redScore >= greenScore + 10:
                if playerOne == 1:
                    red_win_flash()
                    engine.say("Player one, red, with " + str(redScore) + " points!")
                    engine.runAndWait()
                    playerOneGamesWon = playerOneGamesWon + 1
                if playerOne == 2:
                    red_win_flash()
                    engine.say("Player two, red, with " + str(redScore) + " points!")
                    engine.runAndWait()
                    playerTwoGamesWon = playerTwoGamesWon + 1
            if greenScore >= redScore + 10:
                if playerOne == 2:
                    green_win_flash()
                    engine.say("Player one, green, with " + str(greenScore) + " points!")
                    engine.runAndWait()
                    playerOneGamesWon = playerOneGamesWon + 1
                if playerOne == 1:
                    green_win_flash()
                    engine.say("Player two, green, with " + str(greenScore) + " points!")
                    playerTwoGamesWon = playerTwoGamesWon + 1
        if gameMode == 0:
            if redScore >= 10:
                if playerOne == 1:
                    red_win_flash()
                    engine.say("Player one, red, with ten points!")
                    engine.runAndWait()
                    playerOneGamesWon = playerOneGamesWon + 1
                if playerOne == 2:
                    red_win_flash()
                    engine.say("Player two, red, with ten points!")
                    engine.runAndWait()
                    playerTwoGamesWon = playerTwoGamesWon + 1
            if greenScore >= 10:
                if playerOne == 2:
                    green_win_flash()
                    engine.say("Player one, green, with ten points!")
                    engine.runAndWait()
                    playerOneGamesWon = playerOneGamesWon + 1
                if playerOne == 1:
                    green_win_flash()
                    engine.say("Player two, green, with ten points!")
                    playerTwoGamesWon = playerTwoGamesWon + 1

    # New Game?
    if ttsChoice:
        engine.say("Press the green button if you would like to start a new game. Otherwise, press the red button.")
        engine.runAndWait()
    else:
        print("Press the green button if you would like to start a new game. Otherwise, press the red button.")
    awaitTimer = 0
    pressState = False
    while (awaitTimer < 60) and (not pressState):
        greenButtonState = greenButton.getState()
        redButtonState = redButton.getState()
        if greenButtonState:
            greenLED.setState(True)
            time.sleep(0.25)
            greenLED.setState(False)
            print("New game")
            break
        if redButtonState:
            redLED.setState(True)
            time.sleep(0.25)
            redLED.setState(False)
            run = 1
            print("Game end")
            break

# Announce overall scores
if ttsChoice:
    engine.say("Player one has won " + str(playerOneGamesWon) + " games!")
    engine.runAndWait()
    engine.say("Player two has won " + str(playerTwoGamesWon) + " games!")
    engine.runAndWait()
    engine.say("Thanks for playing!")
    engine.runAndWait()
exit()
