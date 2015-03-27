#Project Co-Conspirators: Zach Abt and Cory Nettnin

#!/usr/bin/env python3


'''
Basic IPv4 router (static routing) in Python.
'''

import sys
import os
import time
from switchyard.lib.packet import *
from switchyard.lib.address import *
from switchyard.lib.common import *

class Router(object):
    def __init__(self, net):
        self.net = net
        self.interfaces = net.interfaces()
        
        


    def router_main(self):    
        '''
        Main method for router; we stay in a loop in this method, receiving
        packets until the end of time.
        '''
        while True:
            pkttype = ""
            gotpkt = True
            try:
                dev,pkt = self.net.recv_packet(timeout=1.0)
            except NoPackets:
                log_debug("No packets available in recv_packet")
                gotpkt = False
            except Shutdown:
                log_debug("Got shutdown signal")
                break

            if gotpkt:
                log_debug("Got a packet: {}".format(str(pkt)))
                arp = pkt.get_header(Arp)
                if arp is not None:
                    pkttype = "arp"

            if pkttype == "arp":
                #print("Are we in the last if?")
                for interface in self.interfaces:
                    #print("Do we get into the for loop?")
                    if arp.targetprotoaddr == interface.ipaddr:
                        #print("Does it detect correctly?")
                        #arpheader = create_ip_arp_reply(interface.ethaddr, arp.senderhwaddr, interface.ipaddr, arp.senderprotoaddr)
                        arpreply = packet.Packet()
                        
                        ethheader = ethernet.Ethernet()
                        ethheader.src = interface.ethaddr
                        ethheader.dst = arp.senderhwaddr
                        ethheader.ethertype = EtherType.ARP
                        arpreply += ethheader

                        arpheader = ethernet.Arp()
                        arpheader.operation = ArpOperation.Reply
                        arpheader.senderhwaddr = interface.ethaddr
                        arpheader.targethwaddr = arp.senderhwaddr
                        arpheader.senderprotoaddr = interface.ipaddr
                        arpheader.targetprotoaddr = arp.senderprotoaddr
                        arpreply += arpheader

                        self.net.send_packet(dev, arpreply)
                        #print("Does it reply?")

def switchy_main(net):
    '''
    Main entry point for router.  Just create Router
    object and get it going.
    '''
    r = Router(net)
    r.router_main()
    net.shutdown()
