#!/usr/bin/python
import random
import socket
import struct

class UDP_scanner:

    def __init__(self, serverIP):
        self.url = 'www.google.com'
        self.serverIP = serverIP
        self.alive_ports = []

    def send_pkt(self, port):
        pkt=self.build_packet()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(bytes(pkt), (self.serverIP, port))
        data, addr = sock.recvfrom(1024)
        sock.close()
        return data

    def build_packet(self):
        randint = random.randint(0, 65535)
        packet = struct.pack(">H", randint)  # Query Ids (Just 1 for now)
        packet += struct.pack(">H", 0x0100)  # Flags
        packet += struct.pack(">H", 1)  # Questions
        packet += struct.pack(">H", 0)  # Answers
        packet += struct.pack(">H", 0)  # Authorities
        packet += struct.pack(">H", 0)  # Additional
        split_url = self.url.split(".")
        for part in split_url:
            packet += struct.pack("B", len(part))
            for s in part:
                packet += struct.pack('c',s.encode())
        packet += struct.pack("B", 0)  # End of String
        packet += struct.pack(">H", 1)  # Query Type
        packet += struct.pack(">H", 1)  # Query Class
        return packet

    def check_port(self, port):
        portOpen = False
        for _ in range(5): # udp is unreliable.Packet loss may occur
            try:
                self.send_pkt(port)
                portOpen = True
                break
            except socket.timeout:
                pass
        if portOpen:
            self.alive_ports.append(port)
