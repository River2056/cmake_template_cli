all: install

pre_install:
	pip install pyinstaller

install: pre_install
	pyinstaller -F ./create-cmake-app.py
	cp ./dist/create-cmake-app.exe C:/cli_tools
