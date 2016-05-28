#!/usr/bin/env python

import logging
import sys
import time
import socket
import base64
from ConfigParser import RawConfigParser
from datetime import datetime

cfg = RawConfigParser()

def currentDayStr():
    return time.strftime("%Y%m%d")

def currentTimeStr():
    return time.strftime("%H:%M:%S")

def initLog(rightNow):
    logger = logging.getLogger(cfg.get('logging', 'logName'))
    logPath=cfg.get('logging', 'logPath')
    logFilename=cfg.get('logging', 'logFileName')  
    hdlr = logging.FileHandler(logPath+rightNow+logFilename)
    formatter = logging.Formatter(cfg.get('logging', 'logFormat'),cfg.get('logging', 'logTimeFormat'))
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)
    return logger

def getCmdLineParser():
    import argparse
    desc = 'Execute Morey simulator'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-c', '--config_file', default='../config/morey.conf',
                        help='configuration file name (*.ini format)')
    parser.add_argument('-s', '--scenario_file', default='../data/trip1.txt',
                        help='scenario file name')

    return parser

# Convert the text time stamp to a timestamp
def getDate(line):
    if "-" in line:
        return datetime.strptime(line[2:line.index("-")-1].rstrip(),'%a %b %d %I:%M:%S %Y')
    else:
        return datetime.strptime(line[2:].rstrip(),'%a %b %d %I:%M:%S %Y')

# This replaces the original timestamp in the data with the current one.
def useCurrentDate(line, mask):
    done = False
    currentPos = 0
    while not done:
        start=line.find(mask, currentPos)
        if start < 0:
            done = True
        else:
            # Going to replace 1001 xx yy zz ww
            current=line[start:start+12]
            line=line.replace(current,'1001'+str(hex(int(round(time.time()))))[2:])
            currentPos = start + 1
    return(line)

# This is the logic to figure out the original timestamp of the data in the scenario file.
def getOriginalTime(line):
    start = 48
    if "|" in line:
        start = start +1
    return(line[20+start:20+start+4])
        
# Iterate through the scenario file, replace the old timestamps with the current one, and transmit.
def executeScenario(scenarioFile, sock, logger):
    file = open(scenarioFile, 'r')
    currentTime = None
    lastTime = None
    waitTime = 0
    for line in file:
        if line[0]=="#":
            lastTime = currentTime
            currentTime = getDate(line)
            if lastTime == None:
                waitTime = 0
            else:
                waitTime = (currentTime - lastTime).total_seconds()
        elif len(line)>100:
            time.sleep(waitTime)
            textPackage = useCurrentDate(line.replace("|",""),"1001").rstrip()
            logger.info("Xmit: "+textPackage) 
            package = textPackage.decode("hex")
            #sock.sendto(package, (cfg.get('listener', 'UDP_IP'), cfg.getint('listener', 'UDP_PORT')))
    # Fix this. Not critical.
    file.close()     

def main(argv):

    # Overhead to manage command line opts and config file
    p = getCmdLineParser()
    args = p.parse_args()
    cfg.read(args.config_file)

    # Get the logger going
    rightNow = time.strftime("%Y%m%d%H%M%S")
    logger = initLog(rightNow)
    logger.info('Starting Run: '+time.strftime("%Y%m%d%H%M%S")+'  ==============================')
   
    # Set up the sockets
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # Execute the scenario file
    executeScenario(args.scenario_file, sock, logger)

    # Clean up
    logger.info('Done! '+time.strftime("%Y%m%d%H%M%S")+'  ==============================')

if __name__ == "__main__":
    main(sys.argv[1:])
