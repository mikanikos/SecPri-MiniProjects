import requests
from phe import paillier
import numpy as np

URL_INPUT = "http://com402.epfl.ch/hw5/ex3/get_input"
URL_SERVICE = "http://com402.epfl.ch/hw5/ex3/securehealth/prediction_service"
URL_TOKEN = "http://com402.epfl.ch/hw5/ex3/get_token_2"
EMAIL = "andrea.piccione@epfl.ch"

# Seding request
r = requests.post(URL_INPUT, json={"email": EMAIL})

# Get feature vector
feature_vector = r.json()["x"]

# Record inputs and predictions
predictions = []
inputs = []

print("Starting with the 13 consecutive requests...")

# Asking for predictions in order to get 13 values 
for i in range(-1, 12):

    # Set a different input every time with a different position of the unique 1 in the vector with all zeros or use initial input if it is the first iteration
    # 13 iterations in total and 13 different inputs
    if (i >= 0):
        feature_vector = [0] * 12
        feature_vector[i] = 1

    # Record input
    inputs.append(feature_vector)

    # Generate public and private key
    public_key, private_key = paillier.generate_paillier_keypair()

    # Encrypt vector with public key
    encrypted_vector = [public_key.encrypt(x) for x in feature_vector]

    # Serialization, prepare input
    encrypted_input = [i[0] for i in [(str(x.ciphertext()), x.exponent) for x in encrypted_vector]]

    # Convert to list of integers
    encrypted_input = list(map(int, encrypted_input))

    # Sending request with encrypted input
    r = requests.post(URL_SERVICE, json={"email": EMAIL, "pk": public_key.n, "encrypted_input": encrypted_input, "model": 2})

    # Getting response with the prediction
    encrypted_prediction = r.json()["encrypted_prediction"]

    # Decrypt prediction with private key
    decrypted_prediction = private_key.decrypt(paillier.EncryptedNumber(public_key, encrypted_prediction))

    # Record prediction
    predictions.append(decrypted_prediction)


# Account for the bias term with coefficient 1, add another term to all the inputs vectors
inputs_bias = []
for v in inputs:
    new_v = v
    new_v.append(1)
    inputs_bias.append(new_v)

# Solve linear system
a = np.array(inputs)
b = np.array(predictions)
weights_bias = np.linalg.solve(a,b)

# Convert to int
weights_bias = list(map(int, weights_bias))

# Sending request to get the token
r = requests.post(URL_TOKEN, json={"email": EMAIL, "weights": weights_bias[:-1], "bias": weights_bias[-1]})

print("Token: " + r.json()["token"])