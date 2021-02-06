# change-directory-plus

## Meta
	Cdp is a small minimalist open-source file manager, that try to be efficient and user friendly, the initial concept aimed to be an alternative to the "cd" command, but it evolved into somthing closer to a file manager.


## Screenshot
![](cdp_screenshot/cdp_001.png)

## How to use
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
	return to the home/user directory = c
	show/hide hidden directory = v
	Rename files and directorys = y
	copy path to selection = u
	create file = p
	create directory = g
	open images, videos, or any file type with the default gui = o
	change directory index = i 
	(All the keys will be mappable trough a file soon.)
	
## Alternative keys
	Move selection up = up-arrow or k
	Move selection down = down-arrow or j
	Move into selected directory = right-arrow or l
	Move out of current directory = left-arrow or h

## Tips
	Add the following to your bashrc file to use more efficiently:
	alias cdp = python3 /home/"file direcory"/cdp.py

	To show hidden content use:
	Use python3 /home/"file direcory"/cdp.py -sh
	
| Help to support this project with a Liberapay donation |

[![](https://liberapay.com/assets/widgets/donate.svg)](
https://liberapay.com/Amos_Nimos/donate)


