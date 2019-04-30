import asyncio
import websockets
import os
import binascii
import sys
from hashlib import sha256

# Parameters
SERVER = "ws://com402.epfl.ch/hw2/ws"
USERNAME = "andrea.piccione@epfl.ch"

# Constants
H = sha256
N = "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3"
g = 2
p = "LwsSFxdBXRUHB0MITwYQLQQeRhhBQww="

# Client function
async def client():
    
    async with websockets.connect(SERVER) as websocket:
        # Encode username and send it to server
        U = USERNAME.encode("utf-8")

        # FIRST SEND
        await websocket.send(U)
        print("> Sending username")

        # Receiving the salt encoded
        salt = await websocket.recv()
        print("< Receiving salt")
        
        # Decoding salt in number
        salt_decoded = decode_number(salt)

        # Computing a
        a = int.from_bytes(os.urandom(32), 'big')

        # Computing A and encode it to send it
        A = pow(g, a, int(N, 16))
        A_encoded = encode_number(A)

        # SECOND SEND
        await websocket.send(A_encoded)
        print("> Sendng A")

        # Receiving B encoded
        B = await websocket.recv()
        print("< Receiving B")

        # Decoding B
        B_decoded = decode_number(B)

        # Computing u
        u = H(A.to_bytes((A.bit_length() + 7) // 8, 'big') + B_decoded.to_bytes((B_decoded.bit_length() + 7) // 8, 'big'))
        # Computing x
        x = H(salt_decoded.to_bytes((salt_decoded.bit_length() + 7) // 8, 'big') + binascii.unhexlify(H(USERNAME.encode("utf-8") + ":".encode("utf-8") + p.encode("utf-8")).hexdigest()))
        # Computing S
        S = pow((B_decoded - pow(g, (int(x.hexdigest(), 16)), int(N, 16))), (a + int(u.hexdigest(), 16) * int(x.hexdigest(), 16)), int(N, 16))

        # Preparing H(A || B || S)
        message = H(A.to_bytes((A.bit_length() + 7) // 8, 'big') + B_decoded.to_bytes((B_decoded.bit_length() + 7) // 8, 'big') + S.to_bytes((S.bit_length() + 7) // 8, 'big'))

        # THIRD SEND
        await websocket.send(message.hexdigest().encode("utf-8"))
        print("> Sending hash")

        # Receiving token
        token = await websocket.recv()
        print(f"< {token}")


# function to decode number encodings
def decode_number(i):
    buff = binascii.unhexlify(i)
    return int.from_bytes(buff, 'big')

# function to encode number encodings
def encode_number(i):
    buff = i.to_bytes((i.bit_length() + 7) // 8, 'big')
    return binascii.hexlify(buff).decode()


# Run client function 
asyncio.get_event_loop().run_until_complete(client())