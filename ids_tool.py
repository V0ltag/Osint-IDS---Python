import scapy.all as scapy

# Capture packets
def capture_packets(interface="eth0"):
    print(f"Starting packet capture on {interface}...")
    scapy.sniff(iface=interface, store=0, prn=process_packet)

# Process each packet
def process_packet(packet):
    print(f"Packet captured: {packet.summary()}")
    # Add packet inspection logic here (e.g., for anomalies)
