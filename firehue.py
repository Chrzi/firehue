#!/usr/bin/python3 -u

from phue import Bridge
import argparse
import time
import RPi.GPIO as GPIO

bridge_ip='Philips-hue.teapot'
cooldownTime = 5 * 60
gpioPin = 17


def connect(bridge):
    input("To connect to the bridge press the button on your Hue bridge and then press enter to contiune...")
    bridge.connect()


def alarm(bridge):
    print("Alarm, turning lamps on")
    for light in bridge.lights:
        light.on = True
        light.brightness = 254


def reset(bridge):
    print("Cooldown expired, turning off light")
    for light in bridge.lights:
        light.on = False


def main():
    bridge = Bridge(bridge_ip)
    if args.connect is True:
        connect(bridge)
    else:
        try:
            bridge.connect()
        except Exception:
            print("Failed to connect to bridge, please use --connect for first setup")
            exit(1)
    
    print('Connection to bridge successful!')

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print('Setup GPIO, ready to receive signal...')
    try:
        while True:
            GPIO.wait_for_edge(gpioPin, GPIO.FALLING)
            alarm(bridge)
            time.sleep(cooldownTime)
            reset(bridge)
    finally:
        GPIO.cleanup()


parser = argparse.ArgumentParser(description="An awesome python script to control my Hue lamps to THE MAX!")
parser.add_argument('-c', '--connect', action='store_true', default=False, help="First time connect to bridge")
args = parser.parse_args()


if __name__ == '__main__':
    main()
