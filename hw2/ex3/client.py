import requests

url='http://127.0.0.1:5000/ex2/login'

hj=requests.post(url,json = {
 "user":"andrea.piccione@epfl.ch",
 "pass":"LwsSFxdBXRUHB0MITwYQLQQeRhhBQww=",
})

print(hj.text)