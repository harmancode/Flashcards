# Flashcards
Flashcards is a cross-platform study tool. It calculates which flashcards you should study, and how often, based on a psychologically-proven spaced repetition algorithm. Create, edit, import, and export your own decks and flashcards, and do not forget anything you learn ever again!

It can be used on Windows and GNU/Linux.

## Screenshots

### Decks


![Decks](./image/screenshots/Decks%20view.png)


### Flashcards


![Flashcards](./image/screenshots/Flashcards%20view.png)


### Question (Front)


![Question](./image/screenshots/Question%20view.png)


### Answer (Back)


![Answer](./image/screenshots/Answer%20view.png)


## Download

### Option 1:
You can download the source code from GitHub: https://github.com/harmancode/Flashcards 
Follow the instructions below to run the program from source code.

### Option 2:
If you are using Microsoft Windows you can also download portable binary packages from project's ![GitHub page](https://github.com/harmancode/Flashcards/releases).

## Manual

![Click here to open the manual.](./manual/Flashcards.pdf)

## How to install/run

### How to run the program from source code files on Microsoft Windows:

	Your computer must be connnected to the internet for Step 1 and Step 4.

	Step 1: Download Python to your computer from www.python.org, and install it, if it is not already installed.

	Step 2: Open the command prompt (a.k.a command line, terminal). (Click on the Start button, type cmd, press ENTER)

	Step 3: Go to the directory of the Flashcards on your file system by using "cd" (example: cd Flashcards) command
		
	Step 4: If PIL (Pillow) module is not already installed on your computer (if you have just applied step 1, then you must apply this step 4 now), type the following command in the command prompt to install 'PIL' module (do this just once), and press ENTER:
	
			py -m pip install Pillow
			
		If you have seen "Successfully installed Pillow-8.0.1" (or newer version) message in the command prompt, you are ready to run the Flashcards. 
		
	Step 5: TO RUN THE PROGRAM:
			While you are in the Flashcards program directory, type the following command, and press ENTER: 
			
			python3 main.py
			
To learn how to use the program, please open and read the manual file located in the manual directory.

### How to run the program from source code files on debian (GNU/Linux):

	Your computer must be connnected to the internet for Step 1 and Step 4.

	Step 1: Open the command prompt (a.k.a command line, terminal). 

	Step 2: Go to the directory of the Flashcards on your file system by using "cd" (example: cd Flashcards) command
	
	Step 3: Enter this command:
	
			sudo apt install python3-tk python3-pip 
		
	Step 4: If PIL (Pillow) module is not already installed on your computer, type the following command in the command prompt to install 'PIL' module (do this just once), and press ENTER:
	
			python3 -m pip install --upgrade pip
		
	Step 5: TO RUN THE PROGRAM:
			While you are in the Flashcards program directory, type the following command, and press ENTER: 
			
			py main.py
			
To learn how to use the program, please open and read the manual file located in the manual directory.

### How to run the program from .exe package on Microsoft Windows:

	Simply run the Flashcards.exe file. There is no need to install Flashcards on your system. It is a portable directory. You can run it from anywhere, including from a flash drive.

## Troubleshooting

	1) If you get "ModuleNotFoundError: No Module named 'PIL'" error when you run the program, you should apply step 4 above for once, before running the program.

	2) If you get import failed error, make sure that the CSV file you are trying to import is saved using UTF-8 encoding. Tip: Notepad++ can do the converting for you.	


## License

Flashcards is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 

See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

Copyright 2020 Ertugrul Harman

## Contact

E-mail: harmancode@gmail.com

Twitter: https://twitter.com/harmancode

Web: https://harman.page

## Acknowledgment

<div>Program icon is made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
