# HectreTest

Summary of Scripts:

	- initialize_backendAPI.py initializes the Flask API environment to read data in  given a user input, it also creates the relational database
		
	- db_add_initial.py and db_query.py are test scripts to insert data and extract/edit data in the database

	- ...unit test
	
	- ...cloud stuff
	
Summary of files:
	
	- "Techinical Test Answers.docx" is the written answers to the tasks given in this technical test
	
	- image_database.db is the SQLite relational database created using flask SQLalchemy (contains Image Table and User Table)

	- requirements.txt are all the python dependencies needed
	
	- image_filesystem is a folder which is used to store images when given an image path to read an input image
	
	- .git is a folder which has all the history of commands to github (only visible in the local repository)
	
	- mock_image.png is just the test image used to run the test scripts defined above

	
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
	
	6)	Run “initialize_backendAPI.py” which sets up the API so data can be fed in to the database in real time.