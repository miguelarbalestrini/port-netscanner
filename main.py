import argparse
from posixpath import expanduser
import sys
import json
import os
import requests
import src.network_scanner as ip_scanner
import src.tcp_scanner as tcp_scanner
import src.udp_scanner as udp_scanner

def generate_json(data):
    dir = './output'
    file_name = "data.json"
    sys.stdout.write("\nGenerando archivo json: " + " . . . .")
    try:
        with open(os.path.join(dir, file_name), 'w') as file:
            json.dump(data, file)
            sys.stdout.write("     [OK]\n")
    except:
         sys.stdout.write("     [FAIL]\n")
        
def send_to_url(data_to_send):
    url = 'http://127.0.0.1/example/fake_url.php'
    sys.stdout.write("\nEnviando resultados a la url: " + url + " . . . .")
    response = requests.post(url, data = data_to_send)
    if (response == 200):
         sys.stdout.write("     [OK]\n")
    else:
        sys.stdout.write("     [FAIL]\n")

def dump(current_ip, tcp_alive_ports, udp_alive_ports):    
    sys.stdout.write("\n" + current_ip + "\n")
    sys.stdout.write("==================\n")
    sys.stdout.write("      TCP: ")

    for port in tcp_alive_ports:
        sys.stdout.write("\n           " + str(port) + "\n")
    sys.stdout.write("      UDP: ")

    for port in udp_alive_ports:
        sys.stdout.write("\n           " + str(port) + "\n")
    sys.stdout.write("\n..................\n")

def init_scan(interface):
    sys.stdout.write("\nbuscando máquinas en la red " + interface + "\n")
    net_scanner = ip_scanner.Network_scanner(interface)
    net_scanner.ping_sweep()

    dic_for_dump = {}
    for alive_ip in net_scanner.ip_live:
        current_tcp_scanner = tcp_scanner.TCP_scanner(alive_ip)
        current_udp_scanner = udp_scanner.UDP_scanner(alive_ip)
        for port in range(1, 65536):
            current_tcp_scanner.check_port(port)
            current_udp_scanner.check_port(port)
        dump(alive_ip, current_tcp_scanner.alive_ports, current_udp_scanner.alive_ports)
        dic_for_dump[alive_ip] = current_tcp_scanner.alive_ports, current_udp_scanner.alive_ports
    send_to_url(dic_for_dump)
    generate_json(dic_for_dump)

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser("Network Scanner")
        parser.add_argument("-i", "--interface", type=str,
                            help="Enter the network interface to scan")
        args = parser.parse_args()
        interface = args.interface
        if (interface.count('.') == 3 and interface.count('/') == 1):
            init_scan(interface)
        else:
            sys.stderr.write("Enter the network interface to scan\n")
    except KeyboardInterrupt: 
        sys.stderr.write("\n")
    except:
        print("[+] No Arugments Supplied\n example: python3 main.py -i 192.168.0.105/32")
    