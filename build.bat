pyi-makespec --onefile --windowed --name Flashcards cli.py
echo Manually add data files into the spec file then press ENTER
pause
pyinstaller --clean Flashcards.exe.spec