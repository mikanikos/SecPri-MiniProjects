from flask import Flask, request, Response
import base64

# Creating Flask app
app = Flask(__name__)

# Login Flask application
@app.route('/hw2/ex1', methods=['POST'])
def login():

    # if not json, return 400
    if not request.json:
        return Response(status=400)

    # Parsing json
    content = request.json
    username = content["user"]
    password = content["pass"]
    
    mySecureOneTimePad = "Never send a human to do a machine's job"

    # If inputs are too long, return 400
    if len(username) > 100 or len(password) > 100 :
        return Response(status=400)

    # Applying encryption by using the algorithm
    encryption = superencryption(username, mySecureOneTimePad)

    # If there is a match, returns positive status code, otherwise negative
    if encryption != password:
        return Response(status=400)
    else:
        return Response(status=200)

# Algorithm for encryption
def superencryption(msg, key):
    if len(key) < len(msg):
        diff = len(msg) - len(key)
        key += key[0:diff]
    
    amsg = list(map(ord, msg))
    akey = list(map(ord, key[0:len(msg)]))
    result_xor = applyXOR(amsg, akey)
    string_res = "".join(map(chr, result_xor)) 
    return (base64.b64encode(string_res.encode("ascii"))).decode("ascii")

# Auziliary function for doing a bitwise XOR between elements in the same position of two lists  
def applyXOR(amsg, akey):
    l = []
    for i, v in enumerate(akey):
        l.append(amsg[i] ^ v)
    return l

# Running Flask app
app.run()
