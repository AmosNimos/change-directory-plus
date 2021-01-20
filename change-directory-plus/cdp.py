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



userName = str(getpass.getuser())

#Softwair title
sys.stdout.write("\x1b]2;CDP\x07")

#directory cursor location
xx=0
#file cursor location
yy=0

#I search mode on
SC = False

#initialise debug text as an epmty string
debug=""

#log the historic of selected directory index
dlog=[]

#Do not show all content of the working directory by default
showContent=False;

#hide hidden file by default
hide=True

#active cdp activity
activity=0
#0=directory scrolling
#1=file viewing
#2=line editing

for i in range(len(sys.argv)):
	if str(sys.argv[i]) == "-sh":
		hide=False	

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
	global dlog
	global xx
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
	if len(dlog)>0:
		xx = dlog[-1]
		del dlog[-1]
	return xx
		

#----------------------------------------------------------------------------------#
									# DISPLAY #
#----------------------------------------------------------------------------------#
#Main display function
def display(xx):
	global yy
	#Softwair title
	#print("~CHANGE DIRECTORY PLUS~")
	if activity==0:
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
	elif activity==1:
		#Open file
		fs = open(grid[xx], 'r')
		#store lines into an array
		linelist = fs.readlines()
		#debug=fs.read()
		fs.close()
		#loop file cursor
		if yy>len(linelist)-1:
			yy=0
		if yy<0:
			yy=len(linelist)-1
		print(colored("Current file: ["+str(grid[xx])+"]",'red'))
		print("")
		print("--------------------")
		for i in range(len(linelist)):
			linelist[i]=linelist[i].strip('\n')
		for x in range(yy-2,yy+2):
			if(x == yy and x<len(linelist) and x>=0):
				print(colored(" "+str(x)+" -> ["+str(linelist[x])+"]\n",'red'))
			else:
				if x<len(linelist) and x>=0:
					print(colored(" "+str(x)+" ("+str(linelist[x])+")\n",'white'))
				else:
					print(colored(" - (-)\n",'white'))
		print("--------------------\n")
	return yy

#Get keyboard input
def main():
	with Input(keynames='curses') as input_generator:
		for e in input_generator:
			return e

#clear the terminal.
os.system('clear')

#initialise programme
start()
display(xx)

#----------------------------------------------------------------------------------#
									# ACTIVITY #
#----------------------------------------------------------------------------------#
#activity 0
def scrolling(keypress):
	global xx
	global showContent
	global hide
	global debug
	global activity
	#press down
	if keypress == 's' or keypress == 'KEY_DOWN':
		#Move the selection down
		xx+=1

	#press up
	if keypress == 'w' or keypress == 'KEY_UP':
		#Move the selection up
		xx-=1

	#Go up and down a directory
	#RIGHT
	if keypress == 'KEY_RIGHT' or keypress == 'd':
		if len(grid)>0:
			#Go down a directory
			try:
				dlog.append(int(xx))
				os.chdir(str(path)+"/"+str(grid[xx]))
				start()
			except:
				oldPath=str(grid[xx])
				#try change activity to edit file
				if os.path.isfile(oldPath):
					activity=1
					#exit()
				else:
					debug = "I'm sorry "+userName+", I'm afraid I can't access ["+str(grid[xx])+"]."
		else:
				debug = "I'm sorry "+userName+", I'm afraid I can't access [Missing directory]."
	
	#LEFT
	if(keypress == ' '  or keypress == 'KEY_LEFT' or keypress == 'a'):
		#Go up a directory
		try:
			goup()
		except:
			debug = "I'm sorry "+userName+", I'm afraid I can't access ["+str(os.path.dirname(path))+"]."
		if path == '/':
			debug = "I'm sorry "+userName+", I'm afraid I can't access [Missing directory]."
		#start()

	#press r
	if keypress == 'r':
		showContent= not showContent

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
		#Loop trough the grid list to find a file that start with the same character as the search input.
		if SC:
			for x in range(len(grid)):
				if len(search)>0 and str(grid[x])[:1].lower() == search[:1].lower():
					xx=x
					SC=False
					debug="Selection moved to: ["+str(grid[x]+"]")
					break
		#In case the input is not in the directory.
		if SC:
			debug = "I'm sorry "+userName+", I'm afraid I can't find ["+str(search)+"]."
			SC=False
	return xx

#activity 1
def viewing(keypress):
	global yy
	global activity
	#press down
	if keypress == 's' or keypress == 'KEY_DOWN':
		#Move the selection down
		yy+=1

	#press up
	if keypress == 'w' or keypress == 'KEY_UP':
		#Move the selection up
		yy-=1
	#press left
	if(keypress == ' '  or keypress == 'KEY_LEFT' or keypress == 'a'):
		activity=0
	return yy

#main programme loop
while True:
	#get keypress function
	keypress = main()

	#If the user is not using search
	if SC==False:
		if activity==0:
			scrolling(keypress)
		elif activity==1:
			viewing(keypress)
			
	#refresh the terminal display
	os.system('clear')
	
	# Permanent keypress options ----------------------------
	#press escape
	if keypress == '\x1b':
		try:
			os.kill(os.getppid(), signal.SIGHUP)
			exit()
		except:
			debug = "I'm sorry "+userName+", I'm afraid I can't do that"

	#exit programme
	if keypress == 'q':
		exit()
		
	#press enter
	if keypress == 'e' or  keypress == '\n':
		#Enter the currently selected directory
		newPath=str(path)+"/"+str(grid[xx])
		oldPath=str(grid[xx])
		if os.path.isdir(newPath):
			os.system("gnome-terminal --working-directory="+newPath)
			os.kill(os.getppid(), signal.SIGHUP)
			exit()
		elif os.path.isdir(path):
			os.system("gnome-terminal --working-directory="+str(path))
			os.kill(os.getppid(), signal.SIGHUP)
			exit()
		else:
			debug = "I'm sorry "+str(userName)+", I can't open ["+str(grid[xx])+"]."
			print(debug)
			exit()

	#make the cursor loop around
	if xx>len(grid)-1:
		xx=0
	if xx<0:
		xx=len(grid)-1

	#Display directory
	display(xx)
	#display debug text to the terminal
	print(debug)

	#reset debug text to an empty string
	debug=""
