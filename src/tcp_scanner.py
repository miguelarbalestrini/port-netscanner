import socket
from socket import *

class TCP_scanner:
  
  def __init__(self, ip_address):
        self.ip_address = ip_address
        self.alive_ports = []

  def check_port(self, port):
      client_socket = socket(AF_INET, SOCK_STREAM)
      host = gethostbyname(self.ip_address)
      response = client_socket.connect_ex((host, port))
      if (response == 0):
        self.alive_ports.append(port)
        client_socket.close()

