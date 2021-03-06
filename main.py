import argparse
import re
import subprocess
from time import sleep
from colorama import Fore
from scapy.all import Ether, srp, ARP

'''
TodoList:
1. Remove unecessary code
2. Fix the scapy error NoModuleFound and/or calling pkt(str) python 3 makes no sense Suggestion-> Read the scapy documentation
'''

parser = argparse.ArgumentParser() # Initializes argparse

IP_Help = "Destination IP Address. E.g. 192.168.1.1 or 192.168.1.0/24"

parser.add_argument("-ip", type=str, required=True, help=IP_Help) # adds -ip arguments and sets it data type to string and set to mandatory
args = parser.parse_args()

# ===== Scan specific IP Address =====
def scanSpecificAdd(ip):
    arp = ARP(pdst=ip) # Creating an ARP Packet
    ether = Ether(dst="ff:ff:ff:ff:ff:ff") # Creating a broadcast Packet
    packet = ether/arp # Stacking the arp and ether Packets.

    result = srp(packet, timeout=3)[0]
    print(packet)


# ===== Scan for IP Address range =====
def scanSubnetAdd(ip):
    arp = ARP(pdst=ip) # Creating an ARP Packet
    ether = Ether(dst="ff:ff:ff:ff:ff:ff") # Creating a broadcast Packet
    packet = ether/arp # Stacking the arp and ether Packets.

    result = srp(packet, timeout=3)[0]

    clients = []

    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    print(clients)

def main(ip):
    ListedAddress = re.split(r"[.|/]", args.ip) # Splits the ip address into 4 or 5 elements in a list.

    # ===== check if the input is in IP address format or not
    for address in ListedAddress:
        if int(address) in range(0,256) and len(ListedAddress) == 4 or len(ListedAddress) == 5:
            continue
        else:
            print("Follow the IP Address format")
            sleep(5)
            exit()

    scanSpecificAdd(ip)

main(args.ip)
# try:
#     if len(ListedAddress) == 4:
#         scanSpecificAdd(args.ip) # if the input is in IP address format they it will start scanning it.
#     elif len(ListedAddress) == 5: 
#         scanSubnetAdd(args.ip)  
#     print(Fore.CYAN + "ONLINE" + Fore.WHITE)
# except:
#     print(Fore.RED + "OFFLINE" + Fore.WHITE)