import requests

# location of url
BASE = "http://127.0.0.1:5000/"

"""
# write a data
response = requests.put(BASE + "video/1",{"name": "pewdiepie", "likes": 10, "views": 300000})
print(response.json())

input() # pause UI

# grab the written data for undefined data
response = requests.get(BASE + "video/2")
print(response.json())

# grab the written data for known data
response = requests.get(BASE + "video/1")
print(response.json())
"""

# Currently this all just stores temporarily in memory

# create a list of queries
data = [{"name": "pewdiepie", "likes": 10, "views": 300000},
		{"name": "plain bagel", "likes": 100, "views": 25},
		{"name": "fake pewds", "likes": 1, "views": 99999999}]

for i in range(len(data)):
	response = requests.put(BASE + "video/"+str(i),data[i])
	print(response.json())
	
response = requests.delete(BASE + "video/0")
print(response) # dont return json if the request is delete

response = requests.get(BASE + "video/69")
print(response.json())

response = requests.get(BASE + "video/2")
print(response.json())