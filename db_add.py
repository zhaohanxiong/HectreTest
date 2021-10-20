'''
This script adds initial values to the empty database defined
'''

# run this code after running "initialize_backendAPI.py" which sets up the Flask environment

# import dependencies
import requests

# address of database, for this sample I just used by own local address to initialize the db
BASE = "http://127.0.0.1:5000/"

# create a list of mock data to store, dictionaries are used for each sample
# this dataset could have also been imported from another source, such as a csv table and converted into the SQL database
# if importing from another source, datatypes need to be converted (especially datetime)
data = [{"ImageID": 1, "Date": "2021-10-1 14:01:30", "Type": "Apple", "User": "Joe Farmer", "Email": "JF@gmail.com", "TenantID": "1A"},
		{"ImageID": 2, "Date": "2021-10-3 15:02:40", "Type": "Orange", "User": "John Doe", "Email": "JD@gmail.com", "TenantID": "2B"},
		{"ImageID": 3, "Date": "2021-10-5 16:03:50", "Type": "Cherry", "User": "John Doe", "Email": "JD@gmail.com", "TenantID": "2B"},
		]

# simply loop through each data sample and insert it into database
for i in range(len(data)):
	response = requests.put(BASE + "image/"+str(i), data[i])
	print(response.json())
