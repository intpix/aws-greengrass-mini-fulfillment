#!/usr/bin/env python

# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License is
# located at
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

"""
GGD Button
This GGD will send "green", "red", or "white" button messages.
"""
import json
import time
import random
import socket
import logging
import argparse
import datetime
from gpiozero import PWMLED, Button

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

log = logging.getLogger('button')
# logging.basicConfig(datefmt='%(asctime)s - %(name)s:%(levelname)s: %(message)s')
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s|%(name)-8s|%(levelname)s: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)


GGD_NAME = "GGD_button"
GGD_BUTTON_TOPIC = "/button"

mqttc = AWSIoTMQTTClient(GGD_NAME)
mqttc.configureTlsInsecure(True)
mqttc.configureEndpoint("localhost", 8883)
mqttc.configureCredentials(
    CAFilePath="certs/master-server.crt",
    KeyPath="certs/GGD_button.private.key",
    CertificatePath="certs/GGD_button.certificate.pem.crt"
)
mqttc.connect()

hostname = socket.gethostname()
green_led = PWMLED(4)
green_button = Button(5)
red_led = PWMLED(17)
red_button = Button(6)
white_led = PWMLED(27)
white_button = Button(13)


def button(sensor_id, toggle):
    now = datetime.datetime.now()
    if toggle:
        val = "on"
    else:
        val = "off"

    msg = {
        "version": "2016-11-01",
        "ggd_id": GGD_NAME,
        "hostname": hostname,
        "data": [
            {
                "sensor_id": sensor_id,
                "ts": now.isoformat(),
                "value": val
            }
        ]
    }
    mqttc.publish(GGD_BUTTON_TOPIC, json.dumps(msg), 0)
    return msg


def red_push():
    msg = button(sensor_id="red-button", toggle=True)
    log.info("[red_push] publishing button msg: {0}".format(msg))
    red_led.on()
    green_led.off()
    red_led.pulse()


def red_release():
    msg = button(sensor_id="red-button", toggle=False)
    log.info("[red_release] publishing button msg: {0}".format(msg))


def green_push():
    msg = button(sensor_id="green-button", toggle=True)
    log.info("[green_push] publishing button msg: {0}".format(msg))
    green_led.on()
    red_led.off()
    green_led.pulse()


def green_release():
    msg = button(sensor_id="green-button", toggle=False)
    log.info("[green_release] publishing button msg: {0}".format(msg))


def white_push():
    msg = button(sensor_id="white-button", toggle=True)
    log.info("[white_push] publishing button msg: {0}".format(msg))
    white_led.pulse()


def white_release():
    msg = button(sensor_id="white-button", toggle=False)
    log.info("[white_release] publishing button msg: {0}".format(msg))
    white_led.on()


def use_box(cli):
    red_button.when_pressed = red_push
    red_button.when_released = red_release
    green_button.when_pressed = green_push
    green_button.when_released = green_release
    white_button.when_pressed = white_push
    white_button.when_released = white_release
    white_led.on()
    try:
        while 1:
            time.sleep(0.2)
    except KeyboardInterrupt:
        log.info(
            "[__main__] KeyboardInterrupt ... exiting box monitoring loop")
    red_led.off()
    green_led.off()
    white_led.off()


def button_green(cli):
    if cli.light:
        green_led.on()

    msg = button(sensor_id="green-button", toggle=cli.toggle)
    print("[cli.button_green] publishing button msg: {0}".format(msg))


def button_red(cli):
    if cli.light:
        red_led.on()

    msg = button(sensor_id="red-button", toggle=cli.toggle)
    print("[cli.button_red] publishing button msg: {0}".format(msg))


def button_white(cli):
    if cli.light:
        white_led.on()

    msg = button(sensor_id="white-button", toggle=cli.toggle)
    print("[cli.button_white] publishing button msg: {0}".format(msg))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sorting Hat GGAD and CLI button',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()

    box_parser = subparsers.add_parser(
        'box', description='Use the physical button box to drive.')
    box_parser.add_argument('--on', action='store_true',
                            help="Toggle box ON")
    box_parser.set_defaults(func=use_box, on=True)

    green_parser = subparsers.add_parser(
        'green',
        description='Virtual GREEN button pushed')
    green_parser.add_argument('--on', dest='toggle', action='store_true',
                              help="Virtual toggle ON")
    green_parser.add_argument('--off', dest='toggle', action='store_false',
                              help="Virtual toggle OFF")
    green_parser.add_argument('--light', action='store_true')
    green_parser.set_defaults(func=button_green, toggle=True)

    red_parser = subparsers.add_parser(
        'red',
        description='Virtual RED button pushed')
    red_parser.add_argument('--on', dest='toggle', action='store_true',
                            help="Virtual toggle ON")
    red_parser.add_argument('--off', dest='toggle', action='store_false',
                            help="Virtual toggle OFF")
    red_parser.add_argument('--light', action='store_true')
    red_parser.set_defaults(func=button_red, toggle=True)

    white_parser = subparsers.add_parser(
        'white',
        description='Virtual WHITE button toggled')
    white_parser.add_argument('--on', dest='toggle', action='store_true',
                              help="Virtual toggle ON")
    white_parser.add_argument('--off', dest='toggle', action='store_false',
                              help="Virtual toggle OFF")
    white_parser.add_argument('--light', action='store_true')
    white_parser.set_defaults(func=button_white, toggle=True)

    args = parser.parse_args()
    args.func(args)

    time.sleep(1)
    mqttc.disconnect()
    time.sleep(1)
