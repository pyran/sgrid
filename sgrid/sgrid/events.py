#! /usr/bin/env python3

# Will need to make the argsStr into a list of arguments, right now it handles just one.
class Event(object):
	def __init__(self, funcStr, argsStr, function, funcArgs):
		self.funcStr = funcStr  # The string version of the function
		self.argsStr = argsStr  # list of arguments for the function
		self.function = function # actual function
		self.funcArgs= funcArgs # the functions arguments

class EventManager(object):
	def __init__(self):
		self.eventList = []

	def addEvent(self, e):
		self.eventList += e

	#inp is a list
	#world is the world object
	def serve(self, user_input):
		for event in self.eventList:
			if event.funcStr == user_input[0]:
				if event.argsStr == user_input[1]:  # can change to user_input[1:]
					event.function(event.funcArgs)