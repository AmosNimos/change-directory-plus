# change-directory-plus

## Screenshot
![](cdp_screenshot/cdp_001.png)

## Setup
	Add the following lines to the .bashrc file. Replace both occurrences of nano with the editor you want to set as the default editor: 
	export EDITOR='nano'
	export VISUAL='nano'
	Add the following line to the .bashrc file. Replace xfce4-terminal with the terminal-emulator you want to set as the default terminal-emulator: 
	export TERM='xfce4-terminal'



## How to use
	help = b
	Move selection up = w
	Move selection down = s
	Move into selected directory/file = a
	Move out of current directory = d
	(like in vim you can use hjkl keys to move)
	Enter directory = e
	Quit terminal = escape
	exit cdp = q
	Search file by full name or by the first character = f
	remove file = r
	return to the home/user directory = t
	show/hide hidden directory = v
	Rename files and directorys = y
	copy path to selection = u
	create file = p
	create directory = g
	open images, videos, or any file type with the default gui = "Enter-key"
	change directory index = i 

## Tips
	You can add the following to your bashrc file to start cdp with the cdp command:
		"alias cdp = python3 /file-directory/cdp.py"
	You can also type the following command to acces cdp from anywhere on your system:
		"export PATH=$PATH:/file-directory/cdp.py"
	
	
	
	
## cdp.config options
	colors options:
	* grey
	* red
	* green
	* yellow
	* blue
	* magenta
	* cyan
	* white

	keys options:
	The * symbol represent the "Enter-key" in the cdp.config

	warning:
	keep the cdp.config in the same file as cdp.py

## Arguments
	cdp /"directory-path"
	
| Help to support this project with a Liberapay donation |

[![](https://liberapay.com/assets/widgets/donate.svg)](
https://liberapay.com/Amos_Nimos/donate)


