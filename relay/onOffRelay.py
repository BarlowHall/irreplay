#!/usr/bin/python

"""
irreplay is a commandline utility that uses lirc to receive a sequence of
IR remote button presses and plays back that sequence.
Copyright (C) 2017  Alex Barlow-Hall

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""

import RPi.GPIO as gpio
import sys

pin = 4
numOfArgs = len(sys.argv)

if numOfArgs == 2:
	data = int(sys.argv[1])
	gpio.setmode(gpio.BCM)
	gpio.setwarnings(False)
	gpio.setup(pin, gpio.OUT)
	if data == 1:
		gpio.output(pin, gpio.HIGH)
	elif data == 0:
		gpio.output(pin, gpio.LOW)
		
elif numOfArgs > 2:
	print "ArgumentError: Too many arguments given! (only needs one)"
else:
	print "ArgumentError: No argument given! (needs only one!)"
