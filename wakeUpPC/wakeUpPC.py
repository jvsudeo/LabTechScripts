#!/usr/bin/env python3


import socket
import struct
import os
import sys
import configparser
import re


myconfig = {}


def wake_on_lan(host):
    """ Switches on remote computers using WOL. """
    global myconfig

    try:
      macaddress = myconfig[host]['mac']

    except:
      return False

    # Check mac address format
    found = re.fullmatch('^([A-F0-9]{2}(([:][A-F0-9]{2}){5}|([-][A-F0-9]{2}){5})|([\s][A-F0-9]{2}){5})|([a-f0-9]{2}(([:][a-f0-9]{2}){5}|([-][a-f0-9]{2}){5}|([\s][a-f0-9]{2}){5}))$', macaddress)
    #We must found 1 match , or the MAC is invalid
    if found:
        #If the match is found, remove mac separator [:-\s]
        macaddress = macaddress.replace(macaddress[2], '')
    else:
        raise ValueError('Incorrect MAC address format')
        
    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = b''

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = b''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, (myconfig['General']['broadcast'], 7))
    return True


def loadConfig():
        """ Read in the Configuration file to get CDN specific settings

        """
        global mydir
        global myconfig
        Config = configparser.ConfigParser()
        Config.read(mydir+"/.wol_config.ini")
        sections = Config.sections()
        dict1 = {}
        for section in sections:
                options = Config.options(section)

                sectkey = section
                myconfig[sectkey] = {}


                for option in options:
                        myconfig[sectkey][option] = Config.get(section,option)


        return myconfig # Useful for testing

def usage():
        print(' Usage: wakeUpPC.py [hostname]\n Hostname examples: POD[]PC[] Eg: POD1PC1 \n To view a list of all hosts: wakeUpPC.py list\n To wake up all PCS: wakeUpPC.py PLSWAKEUP')


if __name__ == '__main__':
        mydir = os.path.dirname(os.path.abspath(__file__))
        hostList= [
                "POD1PC1",
                "POD1PC2",
                "POD2PC1",
                "POD2PC2",
                "POD3PC1",
                "POD3PC2",
                "POD4PC1",
                "POD4PC2",
                "POD5PC1",
                "POD5PC2",
                "POD6PC1",
                "POD6PC2",
                "POD7PC1",
                "POD7PC2",
                "POD8PC1",
                "POD8PC2",
                "POD9PC1",
                "POD9PC2",
                "POD10PC1",
                "POD10PC2",
                "POD11PC1",
                "POD11PC2",
                "POD12PC1",
                "POD12PC2",
                "POD13PC1",
                "POD13PC2",
                "POD14PC1",
                "POD14PC2",
                "POD15PC1",
                "POD15PC2",
                "POD16PC1",
                "POD16PC2"
                ]
        
        conf = loadConfig()

        try:

                if sys.argv[1] == "PLSWAKEUP":
                        for hostname in hostList:
                                if not wake_on_lan(hostname):
                                        print('Invalid Hostname specified')
                                else:
                                        print(hostname + ' has woken up')
                        quit()
            

        
                # Use macaddresses with any seperators.
                if sys.argv[1] == 'list':
                        print('Configured Hosts:')
                        for i in conf:
                                if i != 'General':
                                        print('\t',i)
                        print('\n')
                else:
                        if not wake_on_lan(sys.argv[1]):
                                print('Invalid Hostname specified')
                        else:
                                print('The entered PC has woken up')
        except:
                usage()




