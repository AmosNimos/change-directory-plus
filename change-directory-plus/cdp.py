#CDP (Change Directory Plus) by amos nimos
#Sun Jan 17 03:58:38 PM EST 2021
import numpy as np
import random as rn
from termcolor import colored
import os
import sys
import signal
from curtsies import Input

#Softwair title
sys.stdout.write("\x1b]2;CDP\x07")

debug=""

#cursor location
global xx
xx=1


def start():
	global path
	#path = os.path.dirname(os.path.realpath(__file__))
	path = os.getcwd()
	files = os.listdir(path)
	global grid
	grid = []
	for x in files:
		grid.append(x);

def goup():
	global path
	path = os.path.dirname(path)
	files = os.listdir(path)
	global grid
	grid = []
	for x in files:
		grid.append(x);

def display(xx):
	#Softwair title
	#print("~CHANGE DIRECTORY PLUS~")
	print(colored("Current Directory: ["+str(path)+"]\n",'green'))
	print("--------------------\n")
	for x in range(xx-2,xx+2):
		if(x == xx and x<len(grid) and x>0):
			print(colored(" "+str(xx)+" -> ["+str(grid[x])+"]\n",'red'))
		else:
			if x<len(grid) and x>0:
				print(colored(" "+str(x)+" ("+str(grid[x])+")\n",'white'))
			else:
				print(colored(" - (-)\n",'white'))
	print("--------------------\n")

def main():
	with Input(keynames='curses') as input_generator:
		for e in input_generator:
			return e

os.system('clear')
start()
display(xx)
while True:
	keypress = main()
	#press down
	if keypress == 's' or keypress == 'KEY_DOWN':
		#Move the selection down
		xx+=1;
	#press up
	if keypress == 'w' or keypress == 'KEY_UP':
		#Move the selection up
		xx-=1;

	#Go up and down a directory
	if keypress == 'KEY_RIGHT' or keypress == 'd':
		#Go down a directory
		try:
			os.chdir(str(path)+"/"+str(grid[xx]))
			start()
		except:
			debug = "I'm sorry user, I'm afraid I can't acces ["+str(grid[xx])+"]."
	if(keypress == ' '  or keypress == 'KEY_LEFT' or keypress == 'a'):
		#Go up a directory
		try:
			goup()
		except:
			debug = "I'm sorry user, I'm afraid I can't acces ["+str(os.path.dirname(path))+"]."
		if path == '/':
			debug = "I'm sorry user, I'm afraid I can't acces [ ]."
		#start()

	#press enter
	if keypress == 'e' or  keypress == '\n':
		#Enter the currently selected directory
		os.system("gnome-terminal --working-directory="+str(path)+"/"+str(grid[xx]))
		print(str(path))
		debug = "Exit"
		print(debug)
		os.kill(os.getppid(), signal.SIGHUP)
		exit()
	
	#press escape
	if keypress == '\x1b':
		os.kill(os.getppid(), signal.SIGHUP)
		exit()

	os.system('clear')

	#make the cursor loop around
	if xx>len(grid)-1:
		xx=1
	if xx<1:
		xx=len(grid)-1

	#Display directory
	display(xx)
	print(debug)
	debug=""
