from org.lsst.ccs.scripting import *
from java.lang import Exception

CCS.setThrowExceptions(False);
biassub = CCS.attachSubsystem("ts/Bias");
fp = open("/tmp/ccscmnd","r");
for line in fp:
    ccsline = str.split(line)
    cmnd = ccsline[0]
    if len(ccsline)>1 :
        arg = ccsline[1]
#        print "executing command ",cmnd," with argument ",arg;
        result = biassub.synchCommand(10,cmnd,arg);
    else :
#        print "executing command ",cmnd;
        result = biassub.synchCommand(10,cmnd);
    response = result.getResult();
    print "response = ",response

fp.close();
