call "C:\\TechPlan\\server\\venv\\Scripts\\activate.bat"
pyinstaller --onefile core.spec --distpath .\digiPrint
pyinstaller --onefile top-main.spec --distpath .\digiPrint
pause