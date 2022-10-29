install:
	pyinstaller -F ./cmake-template-cli.py
	cp ./dist/cmake-template-cli.exe C:/cli_tools
