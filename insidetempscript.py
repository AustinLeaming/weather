# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Datadog dependencies
from datadog import initialize, statsd
import time
import board 
import adafruit_dht
import logging

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

# for statsd
options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':'8125'
}

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        # 
	#print section
	# 
	#print(
        #    "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
        #        temperature_f, temperature_c, humidity
        #    )
        #)
        # submit metrics to Datadog through dogstatsd
        statsd.gauge("weather.inside.temp_f",temperature_f)
        statsd.gauge("weather.inside.temp_C", temperature_c)
        statsd.gauge("weather.inside.humidity", humidity)
        break 
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        # print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(60)
