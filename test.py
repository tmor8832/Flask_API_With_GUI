import requests

BASE = "http://0.0.0.0:5000/" #default URL given when you run the flask file main.py

data = [{"likes":1500, "name": "Video1", "views":1000}, 
        {"likes":2500, "name": "Video2", "views":2000},
        {"likes":3500, "name": "Video3", "views":3000},
        {"likes":4500, "name": "Video4", "views":4000},
        {"likes":5500, "name": "Video5", "views":5000},
        {"likes":6500, "name": "Video6", "views":20000}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE + "video/2")
print(response.json())
input()
response = requests.delete(BASE + "video/2")
input()
response = requests.get(BASE + "video/2")
print(response.json())