Welcome to Flashcards!

Readme File Version: 1.0
Readme File Date: 25 December 2020

-------------------------------------------------------------------
How to run the program from source code files on Microsoft Windows:
-------------------------------------------------------------------

	Your computer must be connnected to the internet for Step 1 and Step 4.

	Step 1: Download Python to your computer from www.python.org, and install it, if it is not already installed.

	Step 2: Open the command prompt (a.k.a command line, terminal). (Click on the Start button, type cmd, press ENTER)

	Step 3: Go to the directory of the Flashcards on your file system by using "cd" (example: cd Flashcards) command
		
	Step 4: If PIL (Pillow) module is not already installed on your computer (if you have just applied step 1, then you must apply this step 4 now), type the following command in the command prompt to install 'PIL' module (do this just once), and press ENTER:
	
			py -m pip install Pillow
			
		If you have seen "Successfully installed Pillow-8.0.1" (or newer version) message in the command prompt, you are ready to run the Flashcards. 
		
	Step 5: TO RUN THE PROGRAM:
			While you are in the Flashcards program directory, type the following command, and press ENTER: 
			
			py main.py
			
To learn how to use the program, please open and read the manual file located in the manual directory.

-------------------------------------------------------------------
How to run the program from .exe package on Microsoft Windows:
-------------------------------------------------------------------

	Simply run the Flashcards.exe file. There is no need to install Flashcards on your systme. It is a portable directory. You can run it from anywhere, including from a flash drive.


-------------------------------------------------------------------
TROUBLESHOOTING:
-------------------------------------------------------------------

	1) If you get "ModuleNotFoundError: No Module named 'PIL'" error when you run the program, you should apply step 4 above for once, before running the program.


	2) If you get import failed error, make sure that the CSV file you are trying to import is saved using UTF-8 encoding. Tip: Notepad++ can do the converting for you.	


-------------------------------------------------------------------
CSV files:
-------------------------------------------------------------------

	If there is a csv directory in your program folder, then you are provided with example csv files for testing purposes. Feel free to import them to the program and use them. To learn how to import them please refer to the manual.

-------------------------------------------------------------------
Acknowledgements:
-------------------------------------------------------------------
Program icon is made by Freepik (https://www.flaticon.com/authors/freepik) from www.flaticon.com

Enjoy!