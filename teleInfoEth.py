#!/usr/bin/python2.7
# 
# Author: Laoranz <https://github.com/laoranz>
# Date: 03/04/2020
# Desc: Connexion a une sortie Teleinfo sous serveur tcp
#

import socket, threading
import time
from teleInfoProtocol import TeleInfoProtocol


class TeleInfoEth:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port  
        self.running = False
        self.teleInfoProtocol = TeleInfoProtocol()

    def mesures(self):
        return self.teleInfoProtocol.getMesures()
        
    def start(self):
        if self.running:
            print "Error: TeleInfoEth running"
            return
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon=True
        self.thread.start()
    
    def run(self):
        print "start thread"
        self.running = True
        
        while True:
            
            print("waiting for connection %s:%d" % (self.ip, self.port) )
            time.sleep(1)
            
            try:
                mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mSocket.connect((self.ip, self.port))
            except socket.error:
                print "Connexion echoue"
                time.sleep(5)
                continue
                
            print "Connexion etablie avec le serveur."             
            
            data = mSocket.recv(1024)
            # print "data0 %s" % data
            while data:
                self.teleInfoProtocol.addData ( data )

                try:
                    time.sleep(1)
                    data = mSocket.recv(1024)
                    # print "receive %d data" % len(data)
                except socket.error:
                    print "Reception error"
                    break
                    
                # print "data1 %s" % data
            
            mSocket.close()
           
    