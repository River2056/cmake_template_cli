all: upload

setup:
	python setup.py sdist

upload: setup
	twine upload dist/*
