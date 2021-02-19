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
	from configparser import ConfigParser
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
	print("pip3 install requirements.txt")
	print("--------------------")
	#I don't care that this is bad practice, it just work.
	#If you have a working better idea, do a merge request i will gladly accept it.
	print("Install the missing dependency automatically (N/y):")
	userInput = input().lower()[0]
	if userInput == "y":
		try:
			print("Attempting to acquire missing dependency, please wait.")
			os.system("pip3 install configparser")
			os.system("pip3 install getpass")
			os.system("pip3 install numpy")
			os.system("pip3 install pyperclip")
			os.system("pip3 install termcolor")
			os.system("pip3 install curtsies")
		except:
			print("The missing dependency could not be acquired.")
	sys.exit()
#----------------------------------------------------------------------------------#
	# CONFIGURATIONS #
#----------------------------------------------------------------------------------#
cdpPath = os.path.dirname(os.path.abspath(__file__))
configFile = str(cdpPath)+'/cdp.config'
config = ConfigParser()
config.read(configFile)
textColor="red"
highLights="white"
textEditor="$EDITOR"
textColor = str(config["theme"]["textColor"])
highLights = config["theme"]["highLights"]
textEditor = config["default"]["textEditor"]
keys= ['','','','','','']
keys[0] = config["keys"]["openSelection"]
keys[1] = config["keys"]["openGui"]
keys[2] = config["keys"]["createDirectory"]
keys[3] = config["keys"]["Delete"]
keys[4] = config["keys"]["searchName"]
keys[5] = config["keys"]["changeName"]
for x in range(len(keys)):
	if keys[x] == "*":
		keys[x] = '\n'

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
#initialisePath == False

#change the highlight string for the correct color syntax
if highLights != "":
	highLights = "on_"+highLights

marginX = "  "

initialpath = ""
#----------------------------------------------------------------------------------#
	# ARGUMENTS #
#----------------------------------------------------------------------------------#
#arg
if(len(sys.argv)>0):
	for i in range(len(sys.argv)):
		if str(sys.argv[i])[:1] == "/":
			print(str(sys.argv[i]))
			initialpath = str(sys.argv[i]);

#----------------------------------------------------------------------------------#
	# PATH #
#----------------------------------------------------------------------------------#
#pth
#set the path to current working directory
def initialStart(initialpath):
	#path = os.path.dirname(os.path.realpath(__file__))
	if(initialpath==str(__file__) or initialpath==''):
		initialpath = os.getcwd()
	files = os.listdir(initialpath)
	global grid
	grid = []
	for x in files:
		if x[:1]==".":
			if hide is False:
				grid.append(x)
		else:
			grid.append(x)
	grid.sort(key=str.casefold)
	os.chdir(str(initialpath))
	return initialpath

def start():
	global path
	#path = os.path.dirname(os.path.realpath(__file__))
	path = os.getcwd()
	files = os.listdir(path)
	global grid
	grid = []
	for x in files:
		if x[:1]==".":
			if hide is False:
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
			if hide is False:
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
			if hide is False:
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
	if(showContent is True):
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
		print(marginX+colored("[Empty directory]",textColor))
	print(marginX+"+"+(nameSizeLimit+7)*"-"+"+")
	cprint(marginX+colored("Current directory: ["+str(path)+"]",textColor))
	if(len(grid)>0):
		print(marginX+colored("Current selection: ["+grid[x-2]+"]",textColor))
	return fileSelection

#----------------------------------------------------------------------------------#
	# MAIN #
#----------------------------------------------------------------------------------#
#mn
def main():
	global path
	with Input(keynames='curses') as input_generator:
		for e in input_generator:
			return e

#clear the terminal.
os.system('clear')

#initialise programme
path = initialStart(initialpath)
display(directorySelection)

#----------------------------------------------------------------------------------#
	# Search #
#----------------------------------------------------------------------------------#

def searchInName(searchWord, listIndex):
	instences=[]
	for x in range(len(listIndex)):
		if searchWord in str(listIndex[x]):
			instences.append(int(x))
	if len(instences)>0:
	    return instences
	return False


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
	global path

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
					os.system(textEditor+" "+str(oldPath))
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
	if searching is False:
		searchingrolling(keypress)

#____ Permanently available keypress options ____#
	#--------- copy selection path---------#
	if keypress == 'u':
		pyperclip.copy(str(path)+"/"+str(grid[directorySelection]))
		debug = "path copyed to clipboard"

	#--------- creat empty file---------#
	if keypress == 'p':
		#Enter the currently selected directory
		newPath=str(path)+"/"+str(grid[directorySelection])
		oldPath=str(grid[directorySelection])
		try:
			print("How do you want to name this new file: ")
			directoryName = str(input())
			os.system(textEditor+" "+directoryName)
			start()
		except:
			debug = "I'm sorry "+str(userName)+", the file "+directoryName+" could not be created"
			print(debug)
			sys.exit()

	#--------- change directory index ---------#
	if keypress == 'i':
		searching=True
		repeat = True
		while repeat is True:
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

	#--------- change selection name ---------#
	if keypress == keys[5]:
		searching=True
		print("Current folder name "+str(grid[directorySelection]))
		renaming = input("Rename to: ")
		os.rename(str(grid[directorySelection]),str(renaming))
		searching=False
		os.system('clear')
		start()

	#--------- search name ---------#
	if keypress == keys[4]:
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
			srchin = searchInName(str(search),grid)
			if srchin is False:
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
			else:
				print(str(len(srchin)))
				if len(srchin) == 1:
					decision = 0
					directorySelection = srchin[decision]
					searching=False
					os.system('clear')
					debug="Selection moved to: ["+str(grid[srchin[decision]])+"]"
				else:
					print("You search content aprears in:")
					for i in range(len(srchin)):
						print(marginX+str(i)+"-"+str(grid[srchin[i]]))
					decision = len(srchin)+1
					print("")
					try:
						while decision > len(srchin):
							decision = int(input("Move selection to: "))
							if decision > len(srchin):
								print(str(decision)+" was not a valid option.")
								print("Human trying to cheat the system uh...")
								print("I will select for you, incompetent human.")
								decision = int(rn.randrange(0,len(srchin)))
						directorySelection = srchin[decision]
						searching=False
						os.system('clear')
						debug="Selection moved to: ["+str(grid[srchin[decision]])+"]"
					except:
						print("I'm sorry "+userName+", I'm afraid your search attempt faild.")
						searching=False
		#In case the input is not in the directory.
		if searching:
			debug = "I'm sorry "+userName+", I'm afraid I can't find ["+str(search)+"]."
			searching=False

	#exit cdp
	if keypress == 'q':
		sys.exit()

	#Enter the currently selected directory
	if keypress == keys[0]:
		choice = input("Close cdp? [N/y]: ")
		newPath=str(path)+"/"+str(grid[directorySelection])
		oldPath=str(grid[directorySelection])
		if os.path.isdir(newPath):
			os.system(sudoMode+"gnome-terminal --working-directory="+newPath)
			if choice[0].lower()=="y":
				os.kill(os.getppid(), signal.SIGHUP)
		elif os.path.isdir(path):
			os.system(sudoMode+"gnome-terminal --working-directory="+str(path))
			if choice[0].lower()=="y":
				os.kill(os.getppid(), signal.SIGHUP)
		else:
			debug = "I'm sorry "+str(userName)+", I can't open ["+oldPath+"]."
			print(debug)
			sys.exit()

	#Open with gui file manager (xdg)
	if keypress == keys[1]:
		print(keys[1])
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
			sys.exit()

#os.mkdir(path)

	#Create directory
	if keypress == keys[2]:
		#Enter the currently selected directory
		newPath=str(path)+"/"+str(grid[directorySelection])
		oldPath=str(grid[directorySelection])
		try:
			print("How do you want to name this new directory: ")
			directoryName = str(input())
			os.mkdir(directoryName)
			debug = oldPath+" was successfully created"
			start()
		except:
			debug = "I'm sorry "+str(userName)+", the directory "+directoryName+" could not be created"
			print(debug)
			sys.exit()

	#Delete selection
	if keypress == keys[3]:
		#Enter the currently selected directory
		newPath=str(path)+"/"+str(grid[directorySelection])
		oldPath=str(grid[directorySelection])
		try:
			if os.path.isdir(path):
				print("are you sure you want to delete "+oldPath+" (y/n)?: ")
				userInput = input().lower()[0]
				if userInput == "y":
					os.rmdir(oldPath)
					start()
					debug = oldPath+" was successfully deleted"
				else:
					debug = oldPath+" deletion as been aborted"
			else:
				print("are you sure you want to delete "+oldPath+" (y/n)?: ")
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
			sys.exit()

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
