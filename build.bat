pyi-makespec --onedir --windowed --name Flashcards cli.py
echo Manually add data files and icon line into the spec file then press ENTER
pause
pyinstaller --clean Flashcards.spec