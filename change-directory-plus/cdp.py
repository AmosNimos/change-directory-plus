#CDP (Change Directory Plus) by amos nimos
#Sun Jan 17 03:58:38 PM EST 2021
try:
	import numpy as np
	import random as rn
	from termcolor import colored
	#to acces directory path
	import os
	import sys
	import signal
	#to get user keyboard input
	from curtsies import Input
	#to get user name
	import getpass
	import pyttsx3
except:
	print("Missing dependency")
	try:
		print("Attempting to acquire missing dependency, please wait.")
		os.system("pip3 install numpy")
		os.system("pip3 install termcolor")
		os.system("pip3 install curtsies")
		os.system("pip install pyttsx3")
	except:
		print("The missing dependency could not be acquired.")
		print("(Be sure to have pip3 installed)")
	exit()

userName = str(getpass.getuser())

#Text to speach option voice desactivated by default
TTS = False
for i in range(len(sys.argv)):
	if str(sys.argv[i]) == "-tts":
		TTS=True
		#sound
		engine = pyttsx3.init()
		engine.setProperty('rate', 135) 

#Softwair title
sys.stdout.write("\x1b]2;CDP\x07")

#cursor location
global xx
xx=0

#I search mode on
SC = False
#initialise debug text as an epmty string
debug=""

#Do not show all content of the working directory by default
global showContent
showContent=False;

#set the path to current working directory
def start():
	global path
	#path = os.path.dirname(os.path.realpath(__file__))
	path = os.getcwd()
	files = os.listdir(path)
	global grid
	grid = []
	for x in files:
		grid.append(x);
	grid.sort()

#set the path to current working directory parent directory
def goup():
	global path
	path = os.path.dirname(path)
	files = os.listdir(path)
	global grid
	grid = []
	for x in files:
		grid.append(x);
	grid.sort()

#main display function
def display(xx):
	#Softwair title
	#print("~CHANGE DIRECTORY PLUS~")
	print(colored("Current directory: ["+str(path)+"]",'red'))
	if(showContent==True):
		print(colored("List of content: ["+str(os.listdir(path))+"]",'green'))
	print("")

	print("--------------------")
	if len(grid)>0:
		print("")
		for x in range(xx-2,xx+2):
			if(x == xx and x<len(grid) and x>=0):
				print(colored(" "+str(xx)+" -> ["+str(grid[x])+"]\n",'red'))
			else:
				if x<len(grid) and x>=0:
					print(colored(" "+str(x)+" ("+str(grid[x])+")\n",'white'))
				else:
					print(colored(" - (-)\n",'white'))
	else:
		print(colored("[Empty directory]",'white'))
	print("--------------------\n")

#get keyboard input
def main():
	with Input(keynames='curses') as input_generator:
		for e in input_generator:
			return e

#clear the terminal.
os.system('clear')

#initialise programme
start()
display(xx)

#main programme loop
while True:
	#get keypress function
	keypress = main()

	#If the user is not using search
	if SC==False:
		#press down
		if keypress == 's' or keypress == 'KEY_DOWN':
			#Move the selection down
			xx+=1;
			#Text to speach for deaf
			#if(debug == "" and TTS==True):
				#engine.say(str(grid[xx]))
				#engine.runAndWait()
				#engine.stop()
		#press up
		if keypress == 'w' or keypress == 'KEY_UP':
			#Move the selection up
			xx-=1;
			#Text to speach for deaf
			#if(debug == "" and TTS==True):
				#engine.say(str(grid[xx]))
				#engine.runAndWait()
				#engine.stop()

		#Go up and down a directory
		if keypress == 'KEY_RIGHT' or keypress == 'd':
			if len(grid)>0:
				#Go down a directory
				try:
					os.chdir(str(path)+"/"+str(grid[xx]))
					start()
				except:
					debug = "I'm sorry "+userName+", I'm afraid I can't access ["+str(grid[xx])+"]."
			else:
					debug = "I'm sorry "+userName+", I'm afraid I can't access [Missing directory]."
		if(keypress == ' '  or keypress == 'KEY_LEFT' or keypress == 'a'):
			#Go up a directory
			try:
				goup()
			except:
				debug = "I'm sorry "+userName+", I'm afraid I can't access ["+str(os.path.dirname(path))+"]."
			if path == '/':
				debug = "I'm sorry "+userName+", I'm afraid I can't access [Missing directory]."
			#start()

		#press enter
		if keypress == 'e' or  keypress == '\n':
			#Enter the currently selected directory
			newPath=str(path)+"/"+str(grid[xx])
			
			if os.path.isdir(newPath):
				os.system("gnome-terminal --working-directory="+newPath)
			else:
				if os.path.isdir(path):
					os.system("gnome-terminal --working-directory="+str(path))
				else:	
					debug = "I'm sorry "+userName+", I can only access directory"
					print(debug)
					exit()
			print(debug)
			os.kill(os.getppid(), signal.SIGHUP)
			exit()

		#press q
		if keypress == 'q':
			showContent= not showContent;

		#press f to search word
		if keypress == 'f':
			SC=True
			search = input("Search: ")
			print(search)
			#Loop trough the grid list to find a file with the same name as the search input.
			for x in range(len(grid)):
				if str(grid[x]).lower()==str(search).lower():
					xx=x
					SC=False
					debug="Selection moved to: ["+str(grid[x]+"]")
			#In case the input is not in the directory.
			if SC:
				debug = "I'm sorry "+userName+", I'm afraid I can't find ["+str(search)+"]."
				SC=False
				
	#press escape
	if keypress == '\x1b':
		try:
			os.kill(os.getppid(), signal.SIGHUP)
			exit()
		except:
			debug = "I'm sorry "+userName+", I'm afraid I can't do that"

	#Missing single character search

	#refresh the terminal display	
	os.system('clear')

	#make the cursor loop around
	if xx>len(grid)-1:
		xx=0
	if xx<0:
		xx=len(grid)-1

	#Display directory
	display(xx)
	#display debug text to the terminal
	print(debug)
	
	#text to speach
	if(debug != "" and TTS==True):
		engine.say(debug)
		engine.runAndWait()
		engine.stop()
	#reset debug text to an empty string
	debug=""
