'''
This script has a series of test commands for accessing and editing the database
'''

# import dependencies
import requests

# address of database, for this sample I just used by own local address to initialize the db 
BASE = "http://127.0.0.1:5000/"

see sample in database
response = requests.get(BASE + "image/2")
print(response.json())

# pause
input()

# edit sample in database
response = requests.patch(BASE + "image/2", {"ImageID": 2,"Type": "Mango"})
print(response.json())

# pause
input()

# delete sample in database
response = requests.delete(BASE + "image/2")
print(response.json())
