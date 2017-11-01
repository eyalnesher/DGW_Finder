#!/usr/bin/python

from scapy.all import *

imap = {}   # Dictionary that maps between IP Addresses and MAC addresses
dmac = ""    # The MAC address of the Default Gateway
dip = ""     # The MAC address of the Default Gateway
packets = scapy.plist.PacketList()


def dgw_mac_finder(map):
    """
    Find the MAC address of the Default Gateway (if possible)
    :param map: Dictionary that maps between IP addresses and MAC addresses
    :type map: dict
    :return: The MAC address of the Default Gateway if possible. Otherwise, return an empty string
    :rtype: str
    """
    remap = {}  # Revers map
    for ip in map:
        if map[ip] in remap:
            return map[ip]
        else:
            remap.update({map[ip]: ip})
    else:
        return ""


def arp_checker(arp, mac):
    """
    Scanning the ARP packets
    :return: The IP address of the Default Gateway if possible. Otherwise, return an empty string
    :rtype: str
    """
    if arp.op == 2 and arp.hwsrc == mac:  # The ARP packet is a reply
        return arp.psrc
    else:
        return ""


def packet_actions(packet):
    """
    The actions that happening for every packet we sniffed.
    :param packet: A packet
    :return: None
    """
    global packets
    global dmac
    global dip
    global imap
    global log

    # Saving the packet
    packets.append(packet)

    arpackets = scapy.plist.PacketList()

    # Adding the packet source and destination addresses to the dictionary "imap"
    try:
        imap.update({packet[IP].src: packet[Ether].src, packet[IP].dst: packet[Ether].dst})
    except:
        pass

    # Checking the MAC address
    if dmac == "":  # If the MAC address of the default Gateway wasn't found yet
        dmac = dgw_mac_finder(imap)

        if dmac == "00:00:00:00:00:00":
            dmac = ""

        elif dmac != "":  # If the MAC address of the default Gateway was found right now
            log.write("The MAC address of the Default Gateway is " + dmac + "\n")

            # Checking for ARP and Revers ARP (RARP) packets:
            for p in packets:
                if ARP in p:
                    arpackets.append(p)
            for arpacket in arpackets:
                dip = arp_checker(arpacket, dmac)
            if dip != "":
                log.write("The IP address of the Default Gateway is " + dip)
                log.close()
                sys.exit()

    else:   # We are already know the MAC address

        sendp((Ether(dst=ETHER_BROADCAST) / ARP(op=3, hwsrc=dmac)), verbose=False)

        if ARP in packet:
            dip = arp_checker(packet, dmac)
            if dip != "":
                log.write("The IP address of the Default Gateway is " + dip)
                log.close()
                sys.exit()


def main():
    """
    The program find out who is the Default Gateway (DGW) of the subnet.
    By sniffing packets, the program can determinate two IP addresses which have the same MAC address.
    Because every IP address has one MAC address, clearly one of the IP addresses isn't from our subnet, and the
    MAC address is the MAC address of the Default Gateway (because the network shows us the MAC address of the Default
    Gateway as the MAC address of IP addresses that isn't from the subnet).
    After we have the MAC address in our hand, our program is searching for ARP reply packets, and check the source.
    If the MAC address of the source is the Default Gateway MAC address, the IP address of the source is the IP address
    of the Default Gateway.
    At the same time, the program is sending reverse ARP (RARP) packets, and in this action increas the chance a reply
    ARP packet will be send to us.
    :return: None
    :rtype: None
    """
    global log

    log = open(r"result.log", "w")

    sniff(prn=packet_actions)

if __name__ == '__main__':
    main()
