#!/usr/bin/python

from scapy.all import *
import time

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
    global starting_time
    global run_time
    global log

    # Running time checking
    current_time = time.time()
    if current_time - starting_time > run_time:
        if dmac == "":
            log.write("The Default Gateway could not be found")
        else:
            log.write("The IP address of the Default Gateway could not be found")
        sys.exit()

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
            log.write("The MAC address of the Default Gateway is " + dmac)

            # Checking for ARP and Revers ARP (RARP) packets:
            for p in packets:
                if ARP in p:
                    arpackets.append(p)
            for arpacket in arpackets:
                dip = arp_checker(arpacket, dmac)
            if dip != "":
                log.write("The IP address of the Default Gateway is " + dip)
                sys.exit()

    else:

        sendp((Ether(dst=ETHER_BROADCAST) / ARP(op=3, hwsrc=dmac)), verbose=False)

        if ARP in packet:
            dip = arp_checker(packet, dmac)
            if dip != "":
                print "The IP address of the Default Gateway is " + dip
                sys.exit()


def main(running_time=float("inf")):
    """

    :return:
    """
    global starting_time
    global run_time
    global log

    log = open(r"result.log", "w")
    run_time = running_time
    starting_time = time.time()

    sniff(prn=packet_actions)

if __name__ == '__main__':
    main()
