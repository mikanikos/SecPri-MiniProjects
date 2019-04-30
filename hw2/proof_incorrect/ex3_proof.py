from flask import Flask, request, Response, make_response
import base64
import hmac
import time
import sys

# Secret key for computing hmac
HMAC_KEY = "LwsSFxdBXRUHB0MITwYQLQQeRhhBQww="

# Keeping track of the users who logged in when their session cookie expires
logged_users = []

# Creating Flask app
app = Flask(__name__)


# Method when a user returns to the page with a cookie
@app.route('/ex3/list', methods=['POST'])
def list_login():

    # Getting cookie and decoding information
    cookie = request.cookies.get('LoginCookie')
    cookie_info = base64.b64decode(cookie).decode()

    print("Full Cookie received: " + cookie_info, file=sys.stderr)
    
    # Separate fields and discard empty strings
    cookie_list = list(filter(None, cookie_info.split(",")))
    
    # Check integrity of the "body" of the cookie
    identity_check = (cookie_list[0], cookie_list[1]) in logged_users
    integrity_check = identity_check and (cookie_list[2] == "com402") and (cookie_list[3] == "hw2") and (cookie_list[4] == "ex3") and (cookie_list[5] in ["administrator", "user"])
    if not (integrity_check):
        return Response(status=403)

    # BELOW TWO INSTRUCTIONS COMMENTED TO SHOW ERROR --> A COOKIE THAT DOESN'T HAVE HMAC (BELONGING TO USER) IS CONSIDERED LEGITIMATE BUT SHOULD EVIDENTLY BE CONSIDERD TAMPERED 
    # UNCOMMENTING THIS CONDITION WILL MAKE THE SCRIPT WORK EVERY TIME
    
    ### If the cookie doesn't have any hmac but it does belong to a user who has logged in, returns user code --> WRONG (see above)
    ###if len(cookie_list) == 6 and cookie_list[5] == "user":
    ###    return Response(status=201)

    # In case the hmac doesn't have an appropriate hmac format, cookie was tampered
    if not (cookie_list[-1].isalnum()):
        return Response(status=403)   

    # Getting hmac and the rest of the cookie
    hmac_field = cookie_list[-1]
    cookie_previous_info = cookie_info[0: cookie_info.index(hmac_field)]

    # Recomputing the hmac with the rest of the information
    hmac_recompute = hmac.new(HMAC_KEY.encode(), cookie_previous_info.encode())
    # Check validity of hmac: if it is the same it's safe, otherwise it was tampered
    hmac_check = hmac.compare_digest(hmac_recompute.hexdigest(), hmac_field)

    # Check administrator details
    admin_check = (cookie_list[0] == "administrator") and (cookie_list[5] == "administrator")
    if  admin_check and hmac_check:
        return Response(status=200)
    
    # Check user details
    if cookie_list[5] == "user" and hmac_check:
        return Response(status=201)
    
    # In all other cases, cookie was tampered
    return Response(status=403)

    
# Method when a user tries to login
@app.route('/ex3/login', methods = ['POST'])
def login():
   
   # if not json, return 400
    if not request.json:
        return Response(status=400)

    # Parsing json
    content = request.json
    username = content["user"]
    password = content["pass"]

    # Computing timestamp
    timestamp = str(int(time.time()))

    # Check if the user is an administrator or not, creating the cookie according to this information
    if username == "administrator" and password == "42":
        cookie_content = "administrator," + timestamp + ",com402,hw2,ex3,administrator,"
    else:
        cookie_content = username + "," + timestamp + ",com402,hw2,ex3,user,"
    
    # Keeping track of the users who logged in with their timestamp
    logged_users.append((username, timestamp))

    # Encode information in hmac and use secret key
    HMAC = hmac.new(HMAC_KEY.encode(), cookie_content.encode())

    print("Full Cookie generated: " + cookie_content + HMAC.hexdigest(), file=sys.stderr)

    # Creating cookie with information and hmac
    cookie = base64.b64encode(cookie_content.encode()) + base64.b64encode(HMAC.hexdigest().encode())

    # Setting cookie and return response
    response = make_response()
    response.set_cookie('LoginCookie', cookie)
   
    return response


# Running Flask app
app.run()