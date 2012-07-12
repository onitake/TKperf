'''
Created on 27.06.2012

@author: gschoenb
'''


import argparse
import logging

from fio.FioJob import FioJob
from perfTest.SsdTest import SsdTest


if __name__ == '__main__':
    vTest = FioJob()
    fioVersion = vTest.__str__()#Fetch the fio version
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("mode", help="specify the test mode for the device", choices=["hdd","ssd"])
    parser.add_argument("testname",help="name of the fio job, corresponds to the result output file")
    parser.add_argument("filename",help="data file or device name to run fio test on")
    
    parser.add_argument("-v","--version", help="get the version information", action='version',version=fioVersion)
    parser.add_argument("-d","--debug", help="get detailed debug information",action ='store_true')
    parser.add_argument("-q","--quiet", help="turn off logging of info messages",action ='store_true')
    
    args = parser.parse_args()
    if args.debug == True:
        logging.basicConfig(filename=args.testname+'.log',level=logging.DEBUG)
    if args.quiet == True:
        logging.basicConfig(filename=args.testname+'.log',level=logging.WARNING)
    else:
        logging.basicConfig(filename=args.testname+'.log',level=logging.INFO)
    
    if args.mode == "hdd":
        print "hdd on"
    if args.mode == "ssd":
        myTest = SsdTest(args.testname,args.filename)
        if myTest.checkDevIsMounted() == True:
            print "!!!WARNING!!!"
            print "You are writing to a mounted device, this is highly dangerous!"
            exit(0)
        if myTest.checkDevIsAvbl() == True:
            print "!!!Attention!!!"
            print "All data on " + args.filename + " will be lost!"
            print "Are you sure you want to continue? (In case you really know what you are doing.)"
            print "Press 'y' to continue, any key to stop:"
            key = raw_input()
            if key != 'y':
                exit(0)
        else:
            print "You are not using a valid device or partition!"
            exit(1)        
        
        #myTest.runWriteSatTest()
        myTest.runTpTest()
        print myTest.getTestname()
        print myTest.getFilename()
