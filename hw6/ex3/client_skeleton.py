#!/usr/bin/env python3

import sys
import string
import random
import time
import socket
import binascii

char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits

CHAT_MSG_LEN        = 64
CHAT_MSG_BODY_LEN   = 44
CHAT_MSG_INDEX_LEN  = 20
NUMBER_OF_CHAT_MSGS = 10

PRIMARY_SERVER_ID = 0

class ServerData:

    server_id  = None
    public_key = None
    shared_key = None
    server_ip  = None
    udp_port   = None

    def __init__(self, server_id, server_ip, udp_port):

            self.server_id  = server_id
            self.server_ip  = server_ip
            self.udp_port  = udp_port

def read_server_data():

    # Read data about the servers from a file
    servers_filename = 'all_servers.txt'

    all_servers = []
    with open(servers_filename, 'r') as fp:

        for line in fp.readlines():
            server_id = int(line.split()[0])
            server_ip = line.split()[1]
            udp_port  = int(line.split()[2])

            all_servers.append(ServerData(server_id, server_ip, udp_port))

    return all_servers

# Sends a message to the server
# Important: Expects a response from the server
# Input argument msg should be a string
def send_msg_to_server(server, msg):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (server.server_ip, server.udp_port))

    data = None
    sock.settimeout(1)
    try:
        data, other = sock.recvfrom(4096)
    except socket.timeout:
        print('UDP receive request from server %d timed-out' % server.server_id)
    finally:
        sock.close()

    return data

# Sends a message to the server
# Doesn't expect a response from server
# Input argument msg should be a string
def send_msg_to_server_async(server, msg):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (server.server_ip, server.udp_port))
    sock.close()

def generate_random_message(msg_len):

    return ''.join([random.choice(char_set) for _ in range(msg_len)])

# Generates random chat messages of the following format:
# first CHAT_MSG_INDEX_LEN characters represent msg index
# next  CHAT_MSG_BODY_LEN characters are the message itself
def generate_chat_messages(num_msg):

    messages = []
    for i in range(num_msg):
        msg = generate_random_message(CHAT_MSG_BODY_LEN)
        msg_idx = str(i).zfill(CHAT_MSG_INDEX_LEN)

        messages.append(msg_idx + msg)

    return messages

# Client which is responsible for:
#   - Generate and send a shared key to each server
#   - Generate chat messages and
#     send them to the primary server
def client_sender(servers, num_messages):

    messages = generate_chat_messages(num_messages)

    # Send messages to the primary server
    # See server_skeleton script for the expected format of a messsage
    for m in messages:
        send_msg_to_server_async(servers[PRIMARY_SERVER_ID], 'chat_msg_client ' + m)

    # TODO: insert your code here!
    #pass

    return messages

# Client which is responsible for making the PIR
# It should generate appropriate random masks for each server,
# send the pir requests and finally recover the target message
# Target message is the one with the provided target_msg_index
def client_receiver(servers, num_messages, target_msg_index):
    # TODO: insert your code here!

    target_bitmask = ["0"] * num_messages
    target_bitmask[target_msg_index] = "1"
    target_bitmask = "".join(target_bitmask)

    comb_found = False
    while(not comb_found):
        bitmasks = [bin(random.getrandbits(num_messages))[2:].ljust(num_messages, "0") for i in range(len(servers))] 
        xor_result = bitmasks[0]
        for i in range(1,len(bitmasks)):
            current = bitmasks[i]  
            xor_result = ''.join(str(ord(a) ^ ord(b)) for a, b in zip(xor_result,current))

        #print(xor_result)
        if xor_result == target_bitmask:
            comb_found = True

    random.shuffle(bitmasks)

    #print(bitmasks)

    received_data = []
    for s,b in zip(servers, bitmasks):
        response = send_msg_to_server(s, 'pir_req ' + str(int(b, 2)))
        if response.decode() != "":
            received_data.append(response.decode())

    result = ""
    if received_data != []:
        result = received_data[0]
        for i in range(1,len(received_data)):
            current = received_data[i]  
            result = ''.join(chr(ord(a)^ord(b)) for a, b in zip(result, current))
 
    # Return the target message (string), only the body of the message,
    # without the message index
    return result[CHAT_MSG_INDEX_LEN:]


# This function is for your convenience, so you could test your solution locally
# Feel free to write your own test functions, this is just an example
def test_function():

    all_servers = read_server_data()

    messages = client_sender(all_servers, NUMBER_OF_CHAT_MSGS)

    print('Allow servers some time to exchange the messages')
    time.sleep(5)

    target_msg_index = random.randrange(NUMBER_OF_CHAT_MSGS)

    res = client_receiver(all_servers, NUMBER_OF_CHAT_MSGS, target_msg_index)

    for s in all_servers:
        send_msg_to_server_async(s, 'quit')

    target = messages[target_msg_index]

    if res == target[CHAT_MSG_INDEX_LEN:]:
        print('Success')
    else:
        print('Failure')



# This is the function which should be called when you upload your solution
# Your script will be provided with one cmd line argument, which is the index
# of the target message that you should recover with PIR
# Don't change this function!
def grading_main():

    if len(sys.argv) != 2:
        print('Wrong number of commmand line arguments')
    else:
        target_index = int(sys.argv[1])

        all_servers = read_server_data()

        result = client_receiver(all_servers, NUMBER_OF_CHAT_MSGS, target_index) 

        print(result)


if __name__ == '__main__':

    # Feel free to replace the function and insert your own tests here
    # while you test your solution localy,
    # but when you want to upload your script for grading,
    # make sure this is the function which is called here!
    #grading_main()
    test_function()



