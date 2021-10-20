# HectreTest

Summary of Scripts:

	- 
	
Summary of files:
	
	- 

Setting up to run the code in a linux environment:

	1)	SSH into the desired server (could be cloud, hpc cluster, or just a local server)
	2)	Set up virtual environment (or could be container):
		a)	mkdir Virtual_ENV
		b)	cd Virtual_ENV
		c)	virtualenv -p /usr/bin/python3.6 Virtual_ENV

		This will then install python/pip and other basic tools

	3)	Activate virtual environment:
		a)	source Virtual_ENV/bin/activate

	4)	Install the python dependencies which are in the requirements.txt file that I have provided in the repository:
		a)	pip install –r requirements.txt

	5)	The python code can then be run through commands in the terminal etc:
		a)	python sample.py

		But make sure to activate the virtual environment in #4 every time you reconnect to the server.