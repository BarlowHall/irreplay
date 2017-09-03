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

# Input = String
# Output = The same string or if possible the same contents made into a float
def ifFloat(string):
	try:
		return float(string)
	except ValueError:
		return string


# Input = String (filename), Anything (data to write)
# Output = None
def override(filename, data):
	with open(str(filename), "w") as txtFile:
		txtFile.write(str(data))


# Input = String (filename), Anything (data to write)
# Output = None
def write(filename, data):
	with open(str(filename), "a") as txtFile:
		txtFile.write(str(data))


# Input = String (filename), list (a list of lines)
# Output = None
def writelinebyline(filename, lines):
	with open(str(filename), "w") as txtFile:
		for i in lines:
			txtFile.write(str(i)+"\n")


# Input = String (filename)
# Output = lines
def readlists(filename):
	with open(str(filename), "r") as txtFile:
		lines = txtFile.readlines()
	ind = 0
	for i in lines:
		part = i[1:-3].split(", '")
		x = ifFloat(part[0])
		part[0] = x
		lines[ind] = part
		ind += 1
	return lines


# Input: String (filename)
# Output: List (list of lines)
def readlinebyline(filename):
	with open(str(filename), "r") as txtFile:
		lines = txtFile.readlines()
		ind = 0
		for item in lines:
			lines[ind] = item[:-1]
			ind += 1
	return lines

