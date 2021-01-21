###CDP is a user friendly way to navigate directorys inside the terminal 

| Paypal |
[![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate?hosted_button_id=3SZVAQAEVAT6Q)

#Add the following to your bashrc file to use more efficiently:
	alias cdp = python3 /home/"file direcory"/cdp.py

To show hidden content use:
Use python3 /home/"file direcory"/cdp.py -sh

#How to use
	Move selection up = w
	Move selection down = s
	Move into selected directory = a
	Move out of current directory = d
	Enter directory = e
	Show/hide directory content = r
	Quit terminal = escape
	exit cdp = q
	Search file name = f
	
#Alternative keys
	Move selection up = up arrow
	Move selection down = down arrow
	Move into selected directory = right arrow
	Move out of current directory = left arrow
	Enter directory = enter

#Features currently in development (Not yet implemented):
	 Rename files and directorys
	 Copy a line of text to clipboard
	 (kinda working) Edit a line of text in a file.
	 Create new file and directory
	 Lunch application
	 Delete files and directorys
	 (working) Open a terminal at a (selected directory) without closing cdp.
	 (working) Open the directory and file with the default gui file manager
	 (working) Vim keys (H,J,K,L)
