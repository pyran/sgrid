#! /usr/bin/env python3

from inspect import getargspec
# Will need to make the argsStr into a list of arguments, right now it handles just one.
class Event(object):
	def __init__(self, funcStr, argsStrList, function, argsList):
		# TODO: Fix these variable names.  They are really confusing.
		self.funcStr = funcStr  # The string version of the function
		self.argsStrList = argsStrList  # list of arguments for the function
		self.function = function # actual function
		self.argsList= argsList # the functions arguments

class EventManager(object):
	def __init__(self):
		self.eventList = []

	def addEvent(self, e):
		self.eventList += e

	def parseLine(self, userInput):
		"""Parses the first item in input list as the function and the rest
		as arguments. Returns the two as a tuple."""
		funcStr = userInput[0]
		argsList = userInput[1:]
		return funcStr, argsList


	#inp is a list
	#world is the world object
	def serve(self, userInput):
		# parse the line input from user
		# TODO: Fix naming convention.  argsStrList is used as a local variable here,
		# But argsStrList is also a member variable of the Event object.  Confusing.
		funcStr, argsStrList = self.parseLine(userInput)
		for event in self.eventList:
			if event.funcStr == funcStr:
				if " ".join(userInput[1:]) in event.argsStrList:  # can change to user_input[1:]
					# The * symbol used here allows me to pass an argument list
					# It automattically unwraps them as function parameters
					event.function(*event.argsList)
				else:
					# TODO: Test this case and make a better error message
					print('Unknown command.')
