#CDP (Change Directory Plus) by AKUMA/Amos Nimos
#Sun Jan 17 03:58:38 PM EST 2021

#----------------------------------------------------------------------------------#
	# DEPENDENCY #
#----------------------------------------------------------------------------------#
try:
	#from The Python Standard Library
	import random as rn
	import os
	import sys
	import signal
	#External library
	import getpass
	import numpy as np
	import pyperclip
	from termcolor import colored, cprint
	from curtsies import Input
except:
	print("--------------------")
	print("Missing dependency error!")
	print("")
	print("Manual installation:")
	print("pip3 install requirement.txt")
	print("--------------------")
	"""
	print("Install the missing dependency automatically (N/y):")
	userInput = input().lower()[0]
	if userInput == "y":
		try:
			print("Attempting to acquire missing dependency, please wait.")
			os.system("pip3 install requirement.txt")
		except:
			print("The missing dependency could not be acquired.")
	"""
	exit()

#----------------------------------------------------------------------------------#
	# VARIABLES #
#----------------------------------------------------------------------------------#
#var
#Get username for debug and acces home/user directory
userName = str(getpass.getuser())

#Softwair title
sys.stdout.write("\x1b]2;Change Dicrectory Plus\x07")

#btw (Idealy the would only be a single cursor variable)
#directory cursor location
directorySelection=0

#file cursor location
fileSelection=0

#I search mode on
searching = False

#initialise debug text as an epmty string
debug=""

#log the historic of selected directory index
directoryLog=[]

#Do not show all content of the working directory by default
showContent=False;

#hide hidden file by default
hide=True

#active cdp activity
#0=directory searchingrolling
#1=file viewing
#2=line editing
activity=0

#contain the sudo command if sudo is activated
sudoMode=""

nameSizeLimit= 16

#Text colors options:
#grey
#red
#green
#yellow
#blue
#magenta
#cyan
#white

#Text highlights options:
#grey
#red
#green
#yellow
#blue
#magenta
#cyan
#white

#theme color
textColor = "red"
highLights = "white"

if highLights != "":
	highLights = "on_"+highLights

marginX = "  "

#----------------------------------------------------------------------------------#
	# ARGUMENTS #
#----------------------------------------------------------------------------------#
#arg
for i in range(len(sys.argv)):
	if str(sys.argv[i]) == "-h":
		print("Sorry the info page for cdp is currently not available, use the readme file instead.")
		debug="Sorry the info page for cdp is currently not available, use the readme file instead."
	if str(sys.argv[i]) == "-sh":
		hide=False
	if str(sys.argv[i]) == "-sc":
		showContent=True
	if str(sys.argv[i]) == "-sudo":
		sudoMode="sudo"

#----------------------------------------------------------------------------------#
	# PATH #
#----------------------------------------------------------------------------------#
#pth
#set the path to current working directory
def start():
	global path
	#path = os.path.dirname(os.path.realpath(__file__))
	path = os.getcwd()
	files = os.listdir(path)
	global grid
	grid = []
	for x in files:
		if x[:1]==".":
			if hide == False:
				grid.append(x)
		else:
			grid.append(x)
	grid.sort(key=str.casefold)

#set the path to current working directory parent directory
def goup():
	global path
	global directoryLog
	global directorySelection
	path = os.path.dirname(path)
	files = os.listdir(path)
	global grid
	grid = []
	for x in files:
		if x[:1]==".":
			if hide == False:
				grid.append(x)
		else:
			grid.append(x)
	grid.sort(key=str.casefold)
	if len(directoryLog)>0:
		directorySelection = directoryLog[-1]
		del directoryLog[-1]
	return directorySelection

#set the path to the home/user directory
def goHome():
	global path
	global directoryLog
	global directorySelection
	path = "/home/"+userName
	files = os.listdir(path)
	global grid
	grid = []
	for x in files:
		if x[:1]==".":
			if hide == False:
				grid.append(x)
		else:
			grid.append(x)
	grid.sort(key=str.casefold)
	if len(directoryLog)>0:
		directorySelection = directoryLog[-1]
		del directoryLog[-1]
	return directorySelection


#----------------------------------------------------------------------------------#
	# DISPLAY #
#----------------------------------------------------------------------------------#
#dsp
#Main display function
def display(directorySelection):
	global fileSelection
	#Softwair title
	#print("~CHANGE DIRECTORY PLUS~")

	#activity-0-dsp
	print("")
	print(marginX+"Change Directory Plus")
	#cprint(colored(" Current directory: ["+str(path)+"]",textColor))
	if(showContent==True):
		print(colored("| List of content: ["+str(os.listdir(path))+"]",'green'))
	#print("")
	print(marginX+"+"+(nameSizeLimit+7)*"-"+"+")
	if len(grid)>0:
		for x in range(directorySelection-2,directorySelection+3):
			try:
				selectionName = grid[x]
				#limit selection lenght
				if len(str(selectionName))<nameSizeLimit:
					toAdd = nameSizeLimit-len(str(grid[x]))
					selectionName = selectionName+(toAdd*" ")
				if len(str(selectionName))>nameSizeLimit:
					selectionName = selectionName[0:nameSizeLimit-3]+"..."
			except:
				selectionName=""
			if(x == directorySelection and x<len(grid) and x>=0):
				#print(colored(" "+str(directorySelection)+" -> ["+str(grid[x])+"]\n",'red'))
				if os.path.isdir(grid[directorySelection]):
					cprint(marginX+"|"+"📁 "+str(directorySelection)+" ["+str(selectionName)+"]"+"|", textColor, highLights)
				else:
					cprint(marginX+"|"+"📄 "+str(directorySelection)+" ["+str(selectionName)+"]"+"|", textColor, highLights)
			else:
				if x<len(grid) and x>=0:
					if os.path.isdir(grid[x]):
						print(marginX+"|"+colored("📁 "+str(x)+" ("+str(selectionName)+")",textColor)+"|")
					else:
						print(marginX+"|"+colored("📄 "+str(x)+" ("+str(selectionName)+")",textColor)+"|")
				else:
					print(colored(marginX+"|"+"🚫 - ("+nameSizeLimit*" "+")"+"|",textColor))
	else:
		print(colored("[Empty directory]",textColor))
	print(marginX+"+"+(nameSizeLimit+7)*"-"+"+")
	cprint(marginX+colored("Current directory: ["+str(path)+"]",textColor))
	print(marginX+colored("Current selection: ["+grid[x-2]+"]",textColor))
	return fileSelection

#----------------------------------------------------------------------------------#
	# MAIN #
#----------------------------------------------------------------------------------#
#mn
def main():
	with Input(keynames='curses') as input_generator:
		for e in input_generator:
			return e

#clear the terminal.
os.system('clear')

#initialise programme
start()
display(directorySelection)

#----------------------------------------------------------------------------------#
	# Directory #
#----------------------------------------------------------------------------------#
#moving around directory
def searchingrolling(keypress):

	#--------- a0-global variables ---------#
	global directorySelection
	global showContent
	global hide
	global debug
	global activity

	#press down
	if keypress == 's' or keypress == 'KEY_DOWN' or keypress == 'j':
		#Move the selection down
		directorySelection+=1

	#Go to the Home/user directory
	if keypress == 't':
		#Go to the home/user a directory
		try:
			goHome()
		except:
			debug = "I'm sorry "+userName+", I'm afraid I can't access ["+str(path)+"]."

	#press up
	if keypress == 'w' or keypress == 'KEY_UP' or keypress == 'k':
		#Move the selection up
		directorySelection-=1

	#change hidden file viewing variable
	if keypress == "v":
		hide=not hide
		goHome()

	#Go up and down a directory
	#RIGHT
	if keypress == 'd' or keypress == 'KEY_RIGHT' or keypress == 'l':
		if len(grid)>0:
			#Go down a directory
			try:
				directoryLog.append(int(directorySelection))
				os.chdir(str(path)+"/"+str(grid[directorySelection]))
				start()
			except:
				oldPath=str(grid[directorySelection])
				if os.path.isfile(oldPath):
					#edit file
					os.system("nano "+str(oldPath))
				else:
					debug = "I'm sorry "+userName+", I'm afraid I can't access ["+str(grid[directorySelection])+"]."
		else:
				debug = "I'm sorry "+userName+", I'm afraid I can't access [Missing directory]."

	#LEFT
	if keypress == 'a'  or keypress == 'KEY_LEFT' or keypress == 'h':
		#Go up a directory
		try:
			goup()
			os.chdir(str(path))

		except:
			debug = "I'm sorry "+userName+", I'm afraid I can't access ["+str(os.path.dirname(path))+"]."
		if path == '/':
			debug = "I'm sorry "+userName+", I'm afraid I can't access [Missing directory]."

	if keypress == 'u':
		pyperclip.copy(str(path)+"/"+str(grid[directorySelection]))
		debug = "path copyed to clipboard"

	#search directory index
	if keypress == 'i':
		searching=True
		repeat = True
		while repeat == True:
			try:
				search = int(input("Index: "))
				if search < len(grid):
					directorySelection=search
					repeat=False
					debug="Selection moved to index: ["+str(search)+"]"
				else:
					debug = "I'm sorry "+userName+", I'm afraid I can't acces index ["+str(search)+"]"
					#Refresh the terminal display
					os.system('clear')
					print(debug)
			except:
				debug = "Index must be integer."
				#Refresh the terminal display
				os.system('clear')
				print(debug)

	#--------- change directory name ---------#
	if keypress == 'y':
		searching=True
		print("Current folder name "+str(grid[directorySelection]))
		renaming = input("Rename to: ")
		os.rename(str(grid[directorySelection]),str(renaming))
		searching=False
		os.system('clear')
		start()

	#--------- search directory name ---------#
	if keypress == 'f':
		searching=True
		search = input("Search: ")
		#Loop trough the grid list to find a file with the same name as the search input.
		for x in range(len(grid)):
			if str(grid[x]).lower()==str(search).lower():
				directorySelection=x
				searching=False
				os.system('clear')
				debug="Selection moved to: ["+str(grid[x])+"]"
				break
		#Loop trough the grid list to find a file that start with the same character as the search input.
		if searching:
			for x in range(len(grid)):
				#ignore the dot in hidden file titles for single character search
				if(str(grid[x])[:1]!="."):
					if len(search)>0 and str(grid[x])[0].lower() == search[0].lower():
						directorySelection=x
						searching=False
						os.system('clear')
						debug="Selection moved to: ["+str(grid[x])+"]"
						break
				else:
					if len(search)>0 and str(grid[x])[1].lower() == search[0].lower():
						directorySelection=x
						searching=False
						debug="Selection moved to: ["+str(grid[x])+"]"
						break
		#In case the input is not in the directory.
		if searching:
			debug = "I'm sorry "+userName+", I'm afraid I can't find ["+str(search)+"]."
			searching=False
	return directorySelection

#----------------------------------------------------------------------------------#
	# LOOP #
#----------------------------------------------------------------------------------#
#lp
#Main programme loop
while True:

	#Get keypress from the main function
	keypress = main()

	#Refresh the terminal display
	os.system('clear')

	#If the user is not using search
	if searching==False:
		searchingrolling(keypress)

	#--------- Permanently available keypress options ---------#
	#press esearchingape
	if keypress == '\x1b':
		try:
			os.kill(os.getppid(), signal.SIGHUP)
			exit()
		except:
			debug = "I'm sorry "+userName+", I'm afraid I can't do that"

	#exit cdp
	if keypress == 'q':
		exit()

	#open dir in terminal and quiting cdp
	if keypress == 'e' or  keypress == '\n':
		#Enter the currently selected directory
		newPath=str(path)+"/"+str(grid[directorySelection])
		oldPath=str(grid[directorySelection])
		if os.path.isdir(newPath):
			os.system(sudoMode+"gnome-terminal --working-directory="+newPath)
			os.kill(os.getppid(), signal.SIGHUP)
			exit()
		elif os.path.isdir(path):
			os.system(sudoMode+"gnome-terminal --working-directory="+str(path))
			os.kill(os.getppid(), signal.SIGHUP)
			exit()
		else:
			debug = "I'm sorry "+str(userName)+", I can't open ["+str(grid[directorySelection])+"]."
			print(debug)
			exit()

	#open dir in terminal without quiting cdp
	if keypress == ' ':
		#Enter the currently selected directory
		newPath=str(path)+"/"+str(grid[directorySelection])
		oldPath=str(grid[directorySelection])
		if os.path.isdir(newPath):
			os.system(sudoMode+"gnome-terminal --working-directory="+newPath)
		elif os.path.isdir(path):
			os.system(sudoMode+"gnome-terminal --working-directory="+str(path))
		else:
			debug = "I'm sorry "+str(userName)+", I can't open ["+oldPath+"]."
			print(debug)
			exit()

	#Open with gui file manager (xdg)
	if keypress == 'o':
		#Enter the currently selected directory
		newPath=str(path)+"/"+str(grid[directorySelection])
		oldPath=str(grid[directorySelection])
		try:
			os.system(sudoMode+" xdg-open " + newPath)
			start()
		except:
			debug = "I'm sorry "+str(userName)+", I can't open ["+oldPath+"]."
			print(str(Exception))
			print(debug)
			exit()

#os.mkdir(path)

	#create directory
	if keypress == 'g':
		#Enter the currently selected directory
		newPath=str(path)+"/"+str(grid[directorySelection])
		oldPath=str(grid[directorySelection])
		try:
			print("How do you whant to name this new directory: ")
			directoryName = str(input())
			os.mkdir(directoryName)
			debug = oldPath+" was successfully created"
			start()
		except:
			debug = "I'm sorry "+str(userName)+", directory "+directoryName+" could not be created"
			print(debug)
			exit()

	#Delete file
	if keypress == 'r':
		#Enter the currently selected directory
		newPath=str(path)+"/"+str(grid[directorySelection])
		oldPath=str(grid[directorySelection])
		try:
			if os.path.isdir(path):
				print("are you sure you whant to delete "+oldPath+" (y/n)?: ")
				userInput = input().lower()[0]
				if userInput == "y":
					os.rmdir(oldPath)
					start()
					debug = oldPath+" was successfully deleted"
				else:
					debug = oldPath+" deletion as been aborted"
			else:
				print("are you sure you whant to delete "+oldPath+" (y/n)?: ")
				userInput = input().lower()[0]
				if userInput == "y":
					os.remove(oldPath)
					start()
					debug = oldPath+" was successfully deleted"
				else:
					debug = oldPath+" deletion as been aborted"
		except:
			debug = "I'm sorry "+str(userName)+", I can't delete ["+str(grid[directorySelection])+"]."
			print(debug)
			exit()

	#make the cursor loop around
	if directorySelection>len(grid)-1:
		directorySelection=0
	if directorySelection<0:
		directorySelection=len(grid)-1

	#Display directory
	display(directorySelection)

	#editing line activity
	if activity==2:
		editing(keypress)

	#display debug text to the terminal
	print(" "+debug)

	#reset debug text to an empty string
	debug=""
#----------------------------------------------------------------------------------#
	# END #
#----------------------------------------------------------------------------------#
