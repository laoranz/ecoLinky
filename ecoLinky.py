#!/usr/bin/python2.7
# 
# Author: Laoranz <https://github.com/laoranz>
# Date: 03/04/2020
# Desc: Emulation d'un EcoDevice avec retour des informations de Teleinfo
#

from flask import Flask, request, Response
from flask_restful import Resource, Api
import socket, threading
import time
import sys, getopt
from teleInfoEth import TeleInfoEth

IP = "192.168.1.32"
PORT = 4444

app = Flask(__name__)
api = Api(app)

def parameter(mesures, par, seg, default):
    str = '<{}>'.format(seg)
    if par in mesures:
        str += '{}'.format(mesures[par])
    else:
        str += '{}'.format(default)
    str += '</{}>'.format(seg)
    
    return str

class Status(Resource):
    def gen(self):
        
        mesures = mTeleInfoEth.mesures()
        print "Status ", mesures
        
        yield '<?xml version="1.0" encoding="ISO-8859-1"?>'
        yield '<response>'
        # yield '<date>52902</date>'
        # yield '<time0>15:09</time0>'
        yield '<config_hostname>ecoLinky</config_hostname>'
        # yield '<config_mac>00:05:A3:A2:58:14</config_mac>'
        yield '<http_port>4000</http_port>'
        yield parameter(mesures, "PPAP", "T1_PPAP", 0)
        yield '<T2_PPAP>0</T2_PPAP>'
        yield parameter(mesures, "PAPP", "T1_PAPP", 0)
        yield '<T2_PAPP>0</T2_PAPP>'
        yield parameter(mesures, "PTEC", "T1_PTEC", "")
        yield '<T2_PTEC>----</T2_PTEC>'
        yield parameter(mesures, "ISOUSC", "T1_ISOUSC", 0)
        yield '<T2_ISOUSC>0</T2_ISOUSC>'
        yield parameter(mesures, "IMAX", "T1_IMAX", 0)
        yield parameter(mesures, "IMAX1", "T1_IMAX1", 0)
        yield parameter(mesures, "IMAX2", "T1_IMAX2", 0)
        yield parameter(mesures, "IMAX3", "T1_IMAX3", 0)
        yield '<T2_IMAX>0</T2_IMAX>'
        yield '<T2_IMAX1>0</T2_IMAX1>'
        yield '<T2_IMAX2>0</T2_IMAX2>'
        yield '<T2_IMAX3>0</T2_IMAX3>'
        yield '<meter0></meter0>'
        yield '<meter1></meter1>'
        yield '<meter2></meter2>'
        yield '<meter3></meter3>'
        yield '<count0></count0>'
        yield '<count1></count1>'
        yield '<c0day></c0day>'
        yield '<c1day></c1day>'
        yield '<c0_fuel/>'
        yield '<c1_fuel/>'
        yield '<dnsstatus>0</dnsstatus>'
        yield '<version>1.05.25</version>'
        yield '<salr>175:31:44</salr>'
        yield '</response>'
    
    def get(self):
        return Response(self.gen(), mimetype='text/xml')
        
class Teleinfo(Resource):
        
    def gen(self):
        mesures = mTeleInfoEth.mesures()
        yield '<?xml version="1.0" encoding="ISO-8859-1"?>'
        yield '<response>'
        yield parameter(mesures, "ADCO", "T1_ADCO", 0)
        yield parameter(mesures, "OPTARIF", "T1_OPTARIF", "")
        yield parameter(mesures, "ISOUSC", "T1_ISOUSC", 0)
        yield parameter(mesures, "BASE", "T1_BASE", 0)
        yield parameter(mesures, "HCHC", "T1_HCHC", 0)
        yield parameter(mesures, "HCHP", "T1_HCHP", 0)
        yield parameter(mesures, "EJPHN", "T1_EJPHN", 0)
        yield parameter(mesures, "EJPHPM", "T1_EJPHPM", 0)
        yield parameter(mesures, "BBRHCJB", "T1_BBRHCJB", 0)
        yield parameter(mesures, "BBRHPJB", "T1_BBRHPJB", 0)
        yield parameter(mesures, "BBRHCJW", "T1_BBRHCJW", 0)
        yield parameter(mesures, "BBRHPJW", "T1_BBRHPJW", 0)
        yield parameter(mesures, "BBRHCJR", "T1_BBRHCJR", 0)
        yield parameter(mesures, "BBRHPJR", "T1_BBRHPJR", 0)
        yield parameter(mesures, "PEJP", "T1_PEJP", 0)
        yield parameter(mesures, "PTEC", "T1_PTEC", "")
        yield parameter(mesures, "DEMAIN", "T1_DEMAIN", "----")
        yield parameter(mesures, "IINST", "T1_IINST", 0)
        yield parameter(mesures, "IINST1", "T1_IINST1", 0)
        yield parameter(mesures, "IINST2", "T1_IINST2", 0)
        yield parameter(mesures, "IINST3", "T1_IINST3", 0)
        yield parameter(mesures, "ADPS", "T1_ADPS", 0)
        yield parameter(mesures, "IMAX", "T1_IMAX", 0)
        yield parameter(mesures, "IMAX1", "T1_IMAX1", 0)
        yield parameter(mesures, "IMAX2", "T1_IMAX2", 0)
        yield parameter(mesures, "IMAX3", "T1_IMAX3", 0)
        yield parameter(mesures, "PAPP", "T1_PAPP", 0)
        yield parameter(mesures, "PPAP", "T1_PPAP", 0)
        yield parameter(mesures, "HHPHC", "T1_HHPHC", "A")
        yield parameter(mesures, "MOTDETAT", "T1_MOTDETAT", "000000")
        yield parameter(mesures, "PPOT", "T1_PPOT", "-")
        yield '</response>'
    
    def get(self):
        return Response(self.gen(), mimetype='text/xml')
        
api.add_resource(Status, '/status.xml')
api.add_resource(Teleinfo, '/protect/settings/teleinfo1.xml')


mTeleInfoEth = TeleInfoEth ( IP, PORT )
mTeleInfoEth.start()

