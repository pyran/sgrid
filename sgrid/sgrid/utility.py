#! /usr/bin/env python3

from textwrap import wrap
from time import sleep

class Utility:
	WIDTH = 80  # number of characters that fit the game window per row.

	def formatPrint(self, paragraph, width=WIDTH):
		"""When printing text that was formatted using tripple quotes that spans
		multiple lines, the format of the printed text is usually bad.  This 
		function will help parse the text, wrap it with the textwrap module and
		print to to screen with the proper width and format."""
		# remove any newline chars, excessive white space (tabs)
		parsedInput = paragraph.split() 
		# Now join the list of words with one space
		oneLongLine = " ".join(parsedInput) 
		# Break the long single line paragraph into 70 characters per line.
		# The wrap function makes sure not to break in the middle of a word.
		# It returns a list of formated lines
		formattedLines = wrap(oneLongLine, width)
		for f in formattedLines:
			print(f)
		print("") # end the paragraph with a new line

	def pressToPrint(self, paragraphList, message="."):
		"""After printing each paragraph, the prompt waits for ENTER key press"""
		for paragraph in paragraphList:
			self.formatPrint(paragraph)
			#print("")
			input(message) # can customize the message to say somthing like
			# [Press Enter] or [Continue], but I find it simpliest to have the "..."
			print("")


	def waitToPrint(self, paragraphList, waitTime=0):
	    """Function to print text to screen. Enter text as a list of paragraphs.
	    The optional waitTime argument (seconds) allows display of text to be
	    time delayed for dramatic effect.  Use waitTime=0 for immediate."""
	    for paragraph in paragraphList:
	        self.formatPrint(paragraph)
	        sleep(waitTime)
	        print("")


if __name__ == '__main__':
    # Test area
	print("Testing Utility Class")

	text = """YOU don't know about me without you have read a book by the name
    of The Adventures of Tom Sawyer; but that ain't no matter.  That book was 
    made by Mr. Mark Twain, and he told the truth, mainly.  There was things 
    which he stretched, but mainly he told the truth.  That is nothing.  I never
     seen anybody but lied one time or another, without it was Aunt Polly, or 
     the widow, or maybe Mary.  Aunt Polly—Tom's Aunt Polly, she is—and Mary, 
     and the Widow Douglas is all told about in that book, which is mostly a 
     true book, with some stretchers, as I said before. """

	x = Utility()
	x.formatPrint(text)

	textList = ['''WE went tiptoeing along a path amongst the trees back towards
     the end of the widow's garden, stooping down so as the branches wouldn't 
     scrape our heads. When we was passing by the kitchen I fell over a root and
      made a noise.  We scrouched down and laid still.  Miss Watson's big 
      nigger, named Jim, was setting in the kitchen door; we could see him 
      pretty clear, because there was a light behind him.  He got up and 
      stretched his neck out about a minute, listening.  Then he says:''',

	'''"Who dah?"''',

	'''He listened some more; then he come tiptoeing down and stood right 
	between us; we could a touched him, nearly.  Well, likely it was minutes and
	 minutes that there warn't a sound, and we all there so close together.  
	 There was a place on my ankle that got to itching, but I dasn't scratch it;
	  and then my ear begun to itch; and next my back, right between my 
	  shoulders.  Seemed like I'd die if I couldn't scratch.  Well, I've noticed
	   that thing plenty times since.  If you are with the quality, or at a 
	   funeral, or trying to go to sleep when you ain't sleepy—if you are 
	   anywheres where it won't do for you to scratch, why you will itch all 
	   over in upwards of a thousand places. Pretty soon Jim says:''',

	'''Say, who is you?  Whar is you?  Dog my cats ef I didn' hear sumf'n. 
	Well, I know what I's gwyne to do:  I's gwyne to set down here and listen 
	tell I hears it agin."''' ]

	x.pressToPrint(textList)

	#x.waitToPrint(textList, 2)
