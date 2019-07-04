import requests
from phe import paillier

URL_INPUT = "http://com402.epfl.ch/hw5/ex3/get_input"
URL_SERVICE = "http://com402.epfl.ch/hw5/ex3/securehealth/prediction_service"
URL_TOKEN = "http://com402.epfl.ch/hw5/ex3/get_token_1"
EMAIL = "andrea.piccione@epfl.ch"

# Seding request
r = requests.post(URL_INPUT, json={"email": EMAIL})

# Get feature vector
feature_vector = r.json()["x"]

# Generate public and private key
public_key, private_key = paillier.generate_paillier_keypair()

# Encrypt vector with public key
encrypted_vector = [public_key.encrypt(x) for x in feature_vector]

# Serialization, prepare input
encrypted_input = [i[0] for i in [(str(x.ciphertext()), x.exponent) for x in encrypted_vector]]

# Convert to list of integers
encrypted_input = list(map(int, encrypted_input))

# sending request with encrypted input
r = requests.post(URL_SERVICE, json={"email": EMAIL, "pk": public_key.n, "encrypted_input": encrypted_input, "model": 1})

# Getting response with the prediction
encrypted_prediction = r.json()["encrypted_prediction"]

# Decrypt prediction with private key
decrypted_prediction = private_key.decrypt(paillier.EncryptedNumber(public_key, encrypted_prediction))

# Sending request to get the token
r = requests.post(URL_TOKEN, json={"email": EMAIL, "prediction": decrypted_prediction})

print("Token: " + r.json()["token"])