#!/usr/bin/env python
import Tkinter
import glob
import shutil
import os
import matplotlib.pyplot as plt
import ccs_trending
import time
import subprocess

#raft_id = siteUtils.getLSSTId()
#run_number = siteUtils.getRunNumber()
raft_id = 'LCA-11021_RTM-008-Dev'
run_number = '5422D'
host = 'localhost'


cdir = os.getcwd()

rtmstatelist = [
"RTM_off_5min_stable__502",
"REB_quiescient_record__505",
"RTM_quies_5min_record__508",
"RTM_biases_5min_record__510",
"RTM_clears_5min_record__512",
"RSA_0_5min_record__514",
"RSA_50_5min_record__516",
"RSA_100_5min_record__518",
"RTM_quies_5min_record__520"
]

sectionlist = [
"Temp_a_to_d",
"Plate_Heaters",
"REB0_temperatures",
"REB0_powers",
"REB1_temperatures",
"REB1_powers",
"REB2_temperatures",
"REB2_powers"
]



tm = time.time()
#start = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm-300))
#end = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm))

for rtmstate in rtmstatelist :

    tempfile = "/home/ts8prod/jobHarness/jh_stage/LCA-11021_RTM/%s/%s/%s/v0/*/Temp_a_to_d_%s_%s.txt" % (raft_id,run_number,rtmstate,raft_id,run_number)
    rstart = subprocess.check_output('head -2 %s | tail -1' % tempfile, shell=True)
    rstop  = subprocess.check_output('cat %s | tail -1' % tempfile, shell=True)

    print "rstart",rstart
    print "rstop",rstop
    
    ristart = time.strptime(rstart.split('.')[0],'%Y-%m-%d %H:%M:%S')
    
#    start = time.strftime('%Y-%m-%dT%H:%M:%S',ristart)
    tm = time.mktime(ristart)
    start = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm-3600))

    ristop = time.strptime(rstop.split('.')[0],'%Y-%m-%d %H:%M:%S')
    end = time.strftime('%Y-%m-%dT%H:%M:%S',ristop)
    
    
    
#    milestones = ('2017-10-06T00:00:00', '2017-10-06T23:59:59')
    
    ccs_subsystem = 'ts'

    config_file = 'ts_quantities.cfg'
    
    time_axis = ccs_trending.TimeAxis(start=start, end=end, nbins=1)
    config = ccs_trending.ccs_trending_config(config_file)
    for section in config.sections():
        plotter = ccs_trending.TrendingPlotter(ccs_subsystem, host,
                                               time_axis=time_axis)
        plotter.read_config(config, section)
        title = "%s, %s, %s" % (raft_id, run_number, section)
        plotter.plot(title=title)
        plt.savefig('%s_%s_%s.png' % (section, raft_id, run_number))
        plotter.save_file('%s_%s_%s_%s.txt' % (rtmstate, section, raft_id, run_number))
    
    
    try:
    
        ccs_subsystem = 'ts8'
        
        config_file = 'ts8_quantities.cfg'
        
        time_axis = ccs_trending.TimeAxis(start=start, end=end, nbins=30)
        config = ccs_trending.ccs_trending_config(config_file)
        for section in config.sections():
            plotter = ccs_trending.TrendingPlotter(ccs_subsystem, host,
                                                   time_axis=time_axis)
            plotter.read_config(config, section)
            title = "%s, %s, %s" % (raft_id, run_number, section)
            plotter.plot(title=title)
            plt.savefig('%s_%s_%s.png' % (section, raft_id, run_number))
            plotter.save_file('%s_%s_%s_%s.txt' % (rtmstate,section, raft_id, run_number))
    except:
        pass

print
print " ----------------------------------------------------------------------------------------"
print

fp = open("%s/%s_raw_inputs.txt" % (cdir,raft_id),"w");

for rtmstate in rtmstatelist :
    fp.write("\n\n========== RTM state descriptor: %s =======\n" % rtmstate)
    for sec in sectionlist :
        statfile = '%s/%s_%s_%s_%s.txt' % (cdir,rtmstate,sec,raft_id,run_number)

        try :
            fp2 = open(statfile,"r")
            for line in fp2 :
                fp.write("%s %s" % (rtmstate,line))
            fp2.close()
        except :
            pass

fp.close()
