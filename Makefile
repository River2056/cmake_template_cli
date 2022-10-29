all: install

pre_install:
	pip install pyinstaller

install: pre_install
	pyinstaller -F ./cmake-template-cli.py
	cp ./dist/cmake-template-cli.exe C:/cli_tools
