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

def printDict(dct):
	result = ""
	ind = 0
	while ind < len(dct.keys()):
		key1 = dct.keys()[ind]
		output1 = dct[key1]
		message = str(ind + 1) + " -->\t" + str(key1) + " : " + str(output1)
		if not (ind >= len(dct.keys())-1):
			key2 = dct.keys()[ind+1]
			output2 = dct[key2]
			message += "\t|\t"+str(key2)+" : "+str(output2)+"\t<-- "+str(ind+2)
		result += message+"\n"
		ind += 2
	print result


def printList(lst):
	printable = ""
	ind = 0
	while ind < len(lst):
		item1 = lst[ind]
		result = str(ind+1)+" -->\t" + str(item1)
		if ind != len(lst) - 1:
			item2 = lst[ind + 1]
			result += "\t|\t" + str(item2) + "\t<-- " + str(ind+2)
		ind += 2
		printable += result+"\n"
	print printable
