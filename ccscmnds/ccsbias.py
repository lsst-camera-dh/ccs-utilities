#!/usr/bin/env python
from PythonBinding import *
import os
#import lsst.eotest.sensor as sensorTest
import sys
#from lcatr.harness.helpers import dependency_glob

fileName = "/tmp/ccscmnd"
fo = open(fileName,"w");
#print "Number of arguments = ", len(sys.argv)
if (len(sys.argv)==2) :
    fo.write(sys.argv[1]);
else :
    line = sys.argv[1]+" "+sys.argv[2]
    fo.write(line);
fo.close();

fileName = "biascmnd.py"
fo = open(fileName, "r");
content = fo.read();
fo.close();

try:
#Create an instance of the python binding
    ccs1 = CcsJythonInterpreter();
 
 
#    print 'starting synch execution'
    result1 = ccs1.syncExecution(content);
    print result1.getOutput();    
 
 
except CcsException as ex:
    print 'Failure', ex

