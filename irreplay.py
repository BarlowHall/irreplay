#! /usr/bin/python

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

import os
from datetime import datetime as dt
from os import system as syst
from time import sleep

import pylirc

import fileManage
import nicePrint

menu = "\t\tMenu:\n" \
		"\t1: Learn remote\n" \
		"\t2: Set remote buttons for use\n" \
		"\t3: Record sequence of buttons (CTRL+C to exit)\n" \
		"\t4: Play sequence (CTRL+C to exit)\n" \
		"\t5: Load sequence from file\n" \
		"\t6: Save sequence to file\n" \
		"\t7: Load remote buttons for use\n" \
		"\t8: Add relay on/off to sequence\n" \
		"\t9: Add KEY to sequence\n" \
		"\ta: Add time gap to sequence\n" \
		"\tq: Exit"
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = dir_path + "/sequence.txt"
lircrcPath = dir_path + "/lircrc"
out = ""
keyoutput = {}
blocking = 0
sequence = []

while True:
	print menu
	option = raw_input("Option: ")
	if option == "q":
		break
	elif option == "1":
		print "Starting learn script..."
		syst("sudo kill `cat /var/run/lirc/lircd.pid`")
		syst("if [ -f /etc/lirc/lircd.conf ]; then sudo mv /etc/lirc/lircd.conf /etc/lirc/lircd.conf.bak; fi")
		syst("sudo irrecord -d /dev/lirc0 -f /etc/lirc/lircd.conf")
		syst("sudo lircd")
		print "Finished!"
	elif option == "2":
		fileManage.override(lircrcPath, "")
		while True:
			key = raw_input("Type the full key name and then enter (or 'q' to quit): ")
			if key == 'q':
				break
			out = raw_input("Type the value you want as output: ")
			keyoutput[out] = key
			data = "begin\n" \
					" button="+key+"\n" \
					" prog=pylirc\n" \
					" config="+out+"\n" \
					"end\n"
			fileManage.write(lircrcPath, data)
		print "Finished!\n"
	elif option == "3":
		sequence = []
		print "Start pressing the buttons when and which you want to play!"
		try:
			if pylirc.init("pylirc", lircrcPath, blocking):
				code = {"config" : ""}
				timeBefore = dt.now()
				while code["config"] != "quit":
					s = pylirc.nextcode(1)
					
					while s:
						for (code) in s:
							key = code["config"]

							# print len(keyoutput), len(code)
							# print key, keyoutput[key]
							timeAfter = dt.now()
							timeDiff = timeAfter-timeBefore
							# print timeDiff.seconds, timeDiff.microseconds
							timeSec = str(timeDiff.seconds)
							timeMicro = str(timeDiff.microseconds)
							timeStr = timeSec+"."+timeMicro
							timeResult = float(timeStr)
							data = [timeResult, keyoutput[key]]
							print data
							sequence.append(data)

							s = pylirc.nextcode(1)
							timeBefore = dt.now()
		except KeyboardInterrupt:
			pass
		finally:
			pylirc.exit()
	elif option == "4":
		print len(sequence)
		timesRound = 0
		try:
			while True:
				for data in sequence:
					time = data[0]
					key = data[1]
					# print key, time
					sleep(time)
					if key != " ":
						if key == '1' or key == '0':
							syst("/usr/bin/python /home/pi/programs/gpio/relay/onOffRelay.py "+str(key))
							if key == '1':
								print "turned device on after", time, "seconds"
							elif key == '0':
								print "turned device off after", time, "seconds"
						else:
							syst("irsend SEND_ONCE /etc/lirc/lircd.conf "+key)
							print "sent", key, "after", time, "seconds"
					else:
						print "Slept for", time, "seconds"
				print "\nFinished loop!\n"
				timesRound += 1
		except KeyboardInterrupt:
			pass
		if timesRound > 1:
			print "Loop was executed", timesRound, "times"
		elif timesRound == 1:
			print "Loop was executed once"
		else:
			print "Loop wasn't executed fully."
	elif option == "5":
		print "Loading sequence from", filename
		sequence = fileManage.readlists(filename)
		print "Sequence contains:"
		nicePrint.printList(sequence)
		print "Done!"
	elif option == "6":
		print "Saving sequence to", filename
		fileManage.writelinebyline(filename, sequence)
		print "Sequence contains:"
		nicePrint.printList(sequence)
		print "Done!"
	elif option == "7":
		print "Loading keys that are to be used from", lircrcPath
		data = fileManage.readlinebyline(lircrcPath)
		# print data
		ind = 0
		while ind < len(data):
			item = data[ind]
			if data[ind + 1] == " prog=pylirc":
				if " button=" in item:
					button = item[8:]
					config = data[ind + 2][8:]
					# print button, config
					keyoutput[config] = button
					ind += 5
			else:
				ind += 1
		print "Keys that are being used (output: key):"
		nicePrint.printDict(keyoutput)
	elif option == "8":
		print "Adding on/off into place in sequence:"
		nicePrint.printList(sequence)
		ind = int(raw_input("Where do you want to put it? (1 being first): "))
		timeGap = float(raw_input("How long do you want the gap before turning on/off? (in seconds) "))
		onOff = raw_input("Do you want to turn it off or on? (1 for on, 0 for off.) ")
		print "Inserting turn", onOff, "to sequence at place", ind, "with a", timeGap, "second gap before turning", onOff, "\n"
		data = [timeGap, onOff]
		sequence.insert(ind-1, data)
	elif option == "9":
		print "Adding key into place in sequence:"
		nicePrint.printList(sequence)
		ind = int(raw_input("Where do you want to put it? (1 being first): "))
		timeGap = float(raw_input("How long do you want the gap before the key? (in seconds) "))
		key = raw_input("What key do you want out of "+str(keyoutput.keys())+"? ")
		print "Inserting", key, "to sequence at place", ind, "with a", timeGap, "second gap before", key, "\n"
		data = [timeGap, key]
		sequence.insert(ind-1, data)
	elif option == "a":
		print "Adding time gap into place in sequence:"
		nicePrint.printList(sequence)
		ind = int(raw_input("Where do you want to put it? (1 being first): "))
		timeGap = float(raw_input("How long do you want the gap before the key? (in seconds) "))
		print "Inserting time gap of", timeGap, "to sequence at place", ind, "\n"
		data = [timeGap, " "]
		sequence.insert(ind - 1, data)
	else:
		print "That was not an option. Please try again."
