#!/usr/bin/env python

from __future__ import print_function      # get latest print functionality
import logging
import sys
import time
from ConfigParser import RawConfigParser

cfg = RawConfigParser()

def currentDayStr():
    return time.strftime("%Y%m%d")

def currentTimeStr():
    return time.strftime("%H:%M:%S")

def initLog(rightNow):
    logger = logging.getLogger(cfg.get('logging', 'logName'))
    logPath=cfg.get('logging', 'logPath')
    logFilename=cfg.get('logging', 'logFileName')
    print(logPath)
    print(logFilename)    
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


def main(argv):
    p = getCmdLineParser()
    args = p.parse_args()
    cfg.read(args.config_file)
    rightNow = time.strftime("%Y%m%d%H%M%S")
    logger = initLog(rightNow)
    logger.info('Starting Run: '+currentDayStr()+'  ==============================')
    logger.info('Done! '+time.strftime("%Y%m%d%H%M%S")+'  ==============================')

if __name__ == "__main__":
    main(sys.argv[1:])
