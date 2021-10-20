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

response = requests.get(BASE + "video/2")
print(response.json())

response = requests.patch(BASE + "video/2", {"name": "get rich quick", "views": 666, "likes": 888})
print(response.json())