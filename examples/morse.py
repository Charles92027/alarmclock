import time, RPi.GPIO as GPIO

dotTime = .2

morseLetters = [
	".-", "-...", "-.-.", "-..", ".",
	"..-.", "--.", "....", "..", ".---",
	"-.-", ".-..", "--", "-.", "---",
	".--.", "--.-", ".-.", "...", "-",
	"..-", "...-", ".--", "-..-", "-.--",
	"--.."]

bigButtonLedPin = 16
bigButtonPin = 25

def lightButton():
	GPIO.output(bigButtonLedPin, GPIO.HIGH)

def unLightButton():
	GPIO.output(bigButtonLedPin, GPIO.LOW)

def dot():
	lightButton()
	time.sleep(dotTime)
	unLightButton()
	time.sleep(dotTime)
	
def dash():
	lightButton()
	time.sleep(dotTime * 3)
	unLightButton()
	time.sleep(dotTime)

def letterSpace():
	time.sleep(dotTime * 2)

def wordSpace():
	time.sleep(dotTime * 4)
	
	
def pressed(channel):
	
	if GPIO.input(channel) == GPIO.HIGH:
	
		print("big button pressed")
	
		while GPIO.input(channel) == GPIO.HIGH:
			pass

		print("big button released")

		helloWorld = "HELLO WORLD"

		for letter in helloWorld:
			index = ord(letter)
			if index == 32:
				wordSpace()
			else:
				index -= 65
				digits = morseLetters[index]
				print("{} {}".format(letter, digits))
				for digit in digits:
					if digit == ".":
						dot()
					elif digit == "-":
						dash()
				letterSpace()
			
		wordSpace()


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(bigButtonLedPin, GPIO.OUT)
GPIO.setup(bigButtonPin, GPIO.IN)

GPIO.add_event_detect(bigButtonPin, GPIO.RISING, callback = pressed, bouncetime = 500)

print("big button initialized")

message = input("press enter to quit")

GPIO.cleanup()