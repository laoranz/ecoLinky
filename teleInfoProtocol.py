#!/usr/bin/python2.7
# 
# Author: Laoranz <https://github.com/laoranz>
# Date: 03/04/2020
# Desc: Decodage de le sortie Teleinfo
#

import time

STX = '\x02'
ETX = '\x03'
LF = '\n'
CR = '\r'

class TeleInfoProtocol:
    def __init__(self):
        self.running = False
        self.asSTX = False
        self.frame = []
        self.mesures = {}
    
    def getMesures(self):
        return self.mesures
        
    def addData(self, data):
        data_length = len(data)
        data_idx = 0
        while data_idx<data_length:
            if not self.asSTX:
                while data_idx<data_length:
                    car = data[data_idx]
                    data_idx += 1
                    if car == STX:
                        self.asSTX = True
                        break
            
            if self.asSTX:
                while data_idx<data_length:
                    car = data[data_idx]
                    data_idx += 1
                    if car == ETX:
                        self.asSTX = False
                        self.parseFrame()
                        self.frame = []
                        break
                    self.frame.append(car)
         
        return not self.asSTX
        
    def parseFrame(self):
        
        if self.frame[0] == LF:
            del self.frame[0]
        if self.frame[-1] == CR:
            del self.frame[-1]
    
        data = {}
        for line in "".join(self.frame).split(CR+LF):
            if not self.parseLine(data, line):
                return
        
        data['time'] = time.time()
        data['date'] = time.strftime("%d-%m-%Y", time.localtime())
        data['heure'] = time.strftime("%H:%M:%S", time.localtime())
        self.mesures = data
        print "mesures ", self.mesures
        
    def parseLine(self, data, line):

        if not self.checkCrc (line):
            return False
        
        ht = line[-2]
        pameters = "".join(line).split(ht)
        
        # delete CRC
        del pameters[-1]
        # delete SPACE
        while not pameters[-1]:
            del pameters[-1]
        
        data[pameters[0]] = pameters[-1]
        
        return True
    
    def checkCrc(self, pameters):
    
        if len(pameters) < 3:
            print "len(pameters) < 3"
            return False
            
        sum = 0
        for c in bytearray(pameters):
            sum += c
        
        crc = ord(pameters[-1])
        ht = ord(pameters[-2])
        
        sum -= crc
        crc1 = ((sum - ht) & 0x3F) + 0x20
        crc2 = ((sum - 0) & 0x3F) + 0x20
        
        return ((crc == crc1) or (crc == crc2))
        
    