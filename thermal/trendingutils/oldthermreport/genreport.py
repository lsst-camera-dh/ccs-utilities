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
#raft_id = 'LCA-11021_RTM-005-Dev'
#run_number = '5030D'
#raft_id = 'LCA-11021_RTM-006-Dev'
#run_number = '5307D'
raft_id = 'LCA-11021_RTM-007-Dev'
run_number = '5171D'
host = 'localhost'


cdir = os.getcwd()


rtmstatelist = [
"RTM_thermal_low_t_minimum_power__10",
"RTM_thermal_REB_monitoring__11",
"REB_thermal_min_pwr_htr_0__20",
"REB_thermal_min_pwr_htr_0_stable__21",
"REB_thermal_bias_htr_0__100",
"REB_thermal_stableafterbias__101",
"REB_thermal_readout15s_htr_0__102",
"REB_thermal_clear_htr_0__103",
"REB_thermal_biases_htr_0__104"
]

#rtmstatelist = [
#"REB_thermal_min_pwr_htr_0__20",
#"REB_thermal_min_pwr_htr_0_stable__21",
#"REB_thermal_bias_htr_0__100",
#"REB_thermal_stableafterbias__101",
#"REB_thermal_readout15s_htr_0__102",
#"REB_thermal_clear_htr_0__103",
#"REB_thermal_biases_htr_0__104"
#]

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

#    tempfile = "/home/ts8prod/jobHarness/jh_stage/LCA-11021_RTM/%s/%s/%s/v0/*/Temp_a_to_d_%s_%s.txt" % (raft_id,run_number,rtmstate,raft_id,run_number)
#    tempfile = "/home/ts8prod/jobHarness/jh_stage/LCA-11021_RTM/%s/%s/%s/v0/*/2*.log" % (raft_id,run_number,rtmstate)
    tempfile = "/home/ts8prod/trendingutils/oldthermreport/%s/%s/%s/v0/*/2*.log" % (raft_id,run_number,rtmstate)
    print "test - ",subprocess.check_output('egrep \"step \\"produce\" %s ' % tempfile, shell=True)
    rstart = subprocess.check_output('egrep "step \\"produce" %s | awk \'{print $1,substr($2,1,index($2,",")-1)}\'' % tempfile, shell=True)
    rstop = subprocess.check_output('egrep "produce completed" %s | awk \'{print $1,substr($2,1,index($2,",")-1)}\'' % tempfile, shell=True)

    print "rstart",rstart
    print "rstop",rstop
    
#    ristart = time.strptime(rstart.split('.')[0],'%Y-%m-%d %H:%M:%S')
    ristart = time.strptime(rstart.strip(),'%Y-%m-%d %H:%M:%S')
    
#    start = time.strftime('%Y-%m-%dT%H:%M:%S',ristart)
    tm = time.mktime(ristart)
    start = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(tm-3600))

    ristop = time.strptime(rstop.strip(),'%Y-%m-%d %H:%M:%S')
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
        
        time_axis = ccs_trending.TimeAxis(start=start, end=end, nbins=1)
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
