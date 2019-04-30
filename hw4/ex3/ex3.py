#!/usr/bin/env python3
import os
import sys
import populate
from flask import g
from flask import Flask, current_app
from flask import render_template, request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw4_ex3"

# This method returns a list of messages in a json format such as
# [
# { "name": <name>, "message": <message> },
# { "name": <name>, "message": <message> },
# ...
# ]
# If this is a POST request and there is a parameter "name" given, then only
# messages of the given name should be returned.
# If the POST parameter is invalid, then the response code must be 500.


@app.route("/messages", methods=["GET", "POST"])
def messages():
    with db.cursor() as cursor:

        # Handling GET requests
        if request.method == 'GET':
            # returning all (name, message) in database
            sql = "SELECT name, message FROM messages"
            cursor.execute(sql)

        # Handling POST requests
        if request.method == 'POST':
            
            # Get parameter
            name = request.form['name']

            # If no parameter given, throw error
            if not name:
                return 500
            else:
                # Sanitizing input
                name.replace("'", "\'")

                # Execute query with parameter given
                sql = "SELECT name, message FROM messages WHERE name=%s"
                cursor.execute(sql, (name,))

        # Getting result and building the response
        result = cursor.fetchall()
        json = [{"name": i[0], "message": i[1]} for i in result]

        return jsonify(json), 200


# This method returns the list of users in a json format such as
# { "users": [ <user1>, <user2>, ... ] }
# This methods should limit the number of users if a GET URL parameter is given
# named limit. For example, /users?limit=4 should only return the first four
# users.
# If the paramer given is invalid, then the response code must be 500.
@app.route("/users", methods=["GET"])
def contact():
    with db.cursor() as cursor:

        # Getting possible parameter
        parameter = request.args.get('limit')

        # If no paramter given, return all name of the users
        if parameter is None:
            sql = "SELECT name FROM users"
            cursor.execute(sql)
        else:

            # If not a number, throw error
            if parameter.isdigit():
                limit = int(parameter)
            else:
                return 500

            # If number is not in an acceptable range, throw error
            if limit < 0 or limit > 110:
                return 500

            # Execute query with paramter given
            sql = "SELECT name FROM users LIMIT %s"
            cursor.execute(sql, (limit,))

        # Getting result and building the response
        result = cursor.fetchall()
        json = {"users": [i[0] for i in result]}

        return jsonify(json), 200


if __name__ == "__main__":
    seed = "randomseed"
    if len(sys.argv) == 2:
        seed = sys.argv[1]

    db = pymysql.connect("localhost",
                         username,
                         password,
                         database)
    with db.cursor() as cursor:
        populate.populate_db(seed, cursor)
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0', port=80)
