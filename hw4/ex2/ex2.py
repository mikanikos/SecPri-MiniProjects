from flask import Flask, request, Response, make_response
import base64
import bcrypt


# Creating Flask app
app = Flask(__name__)


# Login Flask application
@app.route('/hw4/ex2', methods=['POST'])
def login():

    # if not json, return 400
    if not request.json:
        return Response(status=400)

    # Parsing json
    content = request.json
    password = content["pass"]
    
    # Encrypt password and send it back
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return Response(hashed, status=200)


# Running Flask app
app.run()