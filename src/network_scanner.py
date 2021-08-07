import os
import platform
import ipaddress

class Network_scanner:
    def __init__(self, interface):
        self.interface = interface
        self.ip_range_list = [str(ip) for ip in ipaddress.IPv4Network(interface, False)]
        self.ip_live = []

    def ping_sweep(self):

        ip_list = self.ip_range_list

        oper = platform.system()

        if (oper == "Windows"):
            ping1 = "ping -n1 "
        elif (oper == "Linux"):
            ping1 = "ping -c1 "
        else:
            ping1 = "ping -c1 "

        for addr in ip_list:

            comm = ping1 + addr
            response = os.popen(comm)
            for line in response.readlines():
                if '1 packets transmitted, 1 received' in line:
                    self.ip_live.append(addr)
