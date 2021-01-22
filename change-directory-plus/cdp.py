#CDP (Change Directory Plus) by AKUMA/Amos Nimos
#Sun Jan 17 03:58:38 PM EST 2021

#----------------------------------------------------------------------------------#
	# DEPENDENCY #
#----------------------------------------------------------------------------------#
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
except:
	print("Missing dependency")
	try:
		print("Attempting to acquire missing dependency, please wait.")
		os.system("pip3 install numpy")
		os.system("pip3 install termcolor")
		os.system("pip3 install curtsies")
	except:
		print("The missing dependency could not be acquired.")
		print("(Be sure to have pip3 installed)")
	exit()

#----------------------------------------------------------------------------------#
	# VARIABLES #
#----------------------------------------------------------------------------------#
#var
#Get username for debug
#btw (is optional)
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

#----------------------------------------------------------------------------------#
	# ARGUMENTS #
#----------------------------------------------------------------------------------#
#arg
for i in range(len(sys.argv)):
	if str(sys.argv[i]) == "-sh":
		hide=False
	if str(sys.argv[i]) == "-searching":
		showContent=True

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
	if activity==0:
		print(colored("Current directory: ["+str(path)+"]",'red'))
		if(showContent==True):
			print(colored("List of content: ["+str(os.listdir(path))+"]",'green'))
		print("")

		print("--------------------")
		if len(grid)>0:
			print("")
			for x in range(directorySelection-2,directorySelection+2):
				if(x == directorySelection and x<len(grid) and x>=0):
					print(colored(" "+str(directorySelection)+" -> ["+str(grid[x])+"]\n",'red'))
				else:
					if x<len(grid) and x>=0:
						print(colored(" "+str(x)+" ("+str(grid[x])+")\n",'white'))
					else:
						print(colored(" - (-)\n",'white'))
		else:
			print(colored("[Empty directory]",'white'))
		print("--------------------\n")
	#activity-1-dsp
	elif activity==1:
		#Open file
		fs = open(grid[directorySelection], 'r')
		#store lines into an array
		linelist = fs.readlines()

		#check for empty line
		#if len(linelist)<1:
			#file = open(grid[directorySelection], 'w')
			#file.write("")
			#file.close()
			#linelist = fs.readlines()

		fs.close()
		#loop file cursor
		#if fileSelection>len(linelist)-1:
			#fileSelection=0
		if fileSelection<0:
			fileSelection=len(linelist)-1
		print(colored("Current file: ["+str(grid[directorySelection])+"]",'red'))
		print("")
		print("--------------------")
		#remove end line.
		for i in range(len(linelist)):
			linelist[i]=linelist[i].strip('\n')
		#file delimitation begin and end
		fd=""
		for x in range(fileSelection-2,fileSelection+2):
			#file delimitation warning
			if x==0:
				fd=colored("[BEGIN]:",'green')
			elif x==len(linelist)-1:
				fd=colored("[END]:",'green')
			else:
				fd=""

			#if is selected and is within file delimitation
			if(x == fileSelection and x<len(linelist) and x>=0):
				#if line is empty
				if(str(linelist[x])==""):
					print(fd+colored(" "+str(x)+" ()\n",'red'))
				else:
					print(fd+colored(" "+str(x)+" -> ["+str(linelist[x]).strip()+"]\n",'red'))
			else:
				if x<len(linelist) and x>=0 and str(linelist[x])!="":
					print(fd+colored(" "+str(x)+" ("+str(linelist[x])+")\n",'white'))
				elif x == fileSelection:
					print(fd+colored(" "+str(x)+" ()\n",'red'))
				elif x>=0:
					print(fd+colored(" "+str(x)+" ()\n",'white'))
				else:
					print(colored(" - (-)\n",'white'))
		print("--------------------\n")
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
	# ACTIVITY 0 #
#----------------------------------------------------------------------------------#
#a0
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
	if keypress == 'c':
		#Go up a directory
		try:
			goHome()
		except:
			debug = "I'm sorry "+userName+", I'm afraid I can't access ["+str(os.path.dirname(path))+"]."
		if path == '/':
			debug = "I'm sorry "+userName+", I'm afraid I can't access [Missing directory]."
		#start()

	#press up
	if keypress == 'w' or keypress == 'KEY_UP' or keypress == 'k':
		#Move the selection up
		directorySelection-=1

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
				#try change activity to edit file
				if os.path.isfile(oldPath):
					activity=1
					#exit()
				else:
					debug = "I'm sorry "+userName+", I'm afraid I can't access ["+str(grid[directorySelection])+"]."
		else:
				debug = "I'm sorry "+userName+", I'm afraid I can't access [Missing directory]."

	#LEFT
	if keypress == 'a'  or keypress == 'KEY_LEFT' or keypress == 'h':
		#Go up a directory
		try:
			goup()
		except:
			debug = "I'm sorry "+userName+", I'm afraid I can't access ["+str(os.path.dirname(path))+"]."
		if path == '/':
			debug = "I'm sorry "+userName+", I'm afraid I can't access [Missing directory]."
		#start()

	#search directory index
	if keypress == 'r':
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

	#--------- activity-0-search  ---------#
	if keypress == 'f':
		searching=True
		search = input("Search: ")
		#Loop trough the grid list to find a file with the same name as the search input.
		for x in range(len(grid)):
			if str(grid[x]).lower()==str(search).lower():
				directorySelection=x
				searching=False
				debug="Selection moved to: ["+str(grid[x])+"]"
				break
		#Loop trough the grid list to find a file that start with the same character as the search input.
		if searching:
			for x in range(len(grid)):
				if len(search)>0 and str(grid[x])[:1].lower() == search[:1].lower():
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
	# ACTIVITY 1 #
#----------------------------------------------------------------------------------#
#a1
#moving around file
def viewing(keypress):
	#--------- activity-1 global variables ---------#
	global fileSelection
	global activity
	global directorySelection

	#get file lines
	fs = open(grid[directorySelection], 'r')
	#store lines into an array
	linelist = fs.readlines()
	fs.close()

	#press down
	if keypress == 's' or keypress == 'KEY_DOWN' or keypress == 'j':
		#Move the selection down
		fileSelection+=1

	#press up
	if keypress == 'w' or keypress == 'KEY_UP' or keypress == 'k':
		#Move the selection up
		fileSelection-=1
	#press left
	if(keypress == 'a'  or keypress == 'KEY_LEFT' or keypress == 'h'):
		activity=0

	#search file index
	if keypress == 'r':
		searching=True
		repeat = True
		while repeat == True:
			try:
				search = int(input("Index: "))
				if search < len(linelist):
					fileSelection=search
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

	#--------- activity-1-search  ---------#
	if keypress == 'f':
		searching=True
		search = input("Search: ")
		#Loop trough the grid list to find a file with the same name as the search input.
		#currently will find the word even if it is in the middle of another one wich is not ideal. (need to be fix)
		for x in range(len(linelist)):
			if str(search).lower() in str(linelist[x]).lower():
				fileSelection=x
				searching=False
				debug="Selection moved to: ["+str(linelist[x]+"]")
				break
		#Loop trough the grid list to find a file that start with the same character as the search input.
		if searching:
			for x in range(len(linelist)):
				if  len(search)>0 and str(linelist[x])[:1].lower() == search[:1].lower():
					fileSelection=x
					searching=False
					debug="Selection moved to: ["+str(linelist[x]+"]")
					exit()
					break
			debug = "I'm sorry "+userName+", I'm afraid I can't find ["+str(search)+"]."
			searching=False
	return fileSelection

#----------------------------------------------------------------------------------#
	# ACTIVITY 2 #
#----------------------------------------------------------------------------------#
#a2
#editing file line

### In development

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
		if activity==0:
			searchingrolling(keypress)
		elif activity==1:
			viewing(keypress)

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
			os.system("gnome-terminal --working-directory="+newPath)
			os.kill(os.getppid(), signal.SIGHUP)
			exit()
		elif os.path.isdir(path):
			os.system("gnome-terminal --working-directory="+str(path))
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
			os.system("gnome-terminal --working-directory="+newPath)
		elif os.path.isdir(path):
			os.system("gnome-terminal --working-directory="+str(path))
		else:
			debug = "I'm sorry "+str(userName)+", I can't open ["+str(grid[directorySelection])+"]."
			print(debug)
			exit()

	#Open with gui file manager (xdg)
	if keypress == 'o':
		#Enter the currently selected directory
		newPath=str(path)+"/"+str(grid[directorySelection])
		oldPath=str(grid[directorySelection])
		try:
			os.system("xdg-open " + newPath)
		except:
			debug = "I'm sorry "+str(userName)+", I can't open ["+str(grid[directorySelection])+"]."
			print(debug)
			exit()

	#make the cursor loop around
	if directorySelection>len(grid)-1:
		directorySelection=0
	if directorySelection<0:
		directorySelection=len(grid)-1

	#Display directory
	display(directorySelection)

	#display debug text to the terminal
	print(debug)

	#reset debug text to an empty string
	debug=""
#----------------------------------------------------------------------------------#
	# END #
#----------------------------------------------------------------------------------#
