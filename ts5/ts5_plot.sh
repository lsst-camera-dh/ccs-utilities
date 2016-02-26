#!/bin/bash
#pkill -f "python ./lcatr-launcher"
source /opt/lsst/redhat6-x86_64-64bit-gcc44/test/lsst-jh/setup.sh
export CCS_BIN_DIR=/opt/lsst/redhat6-x86_64-64bit-gcc44/test/lsst-ccs/bin
cd /opt/lsst/redhat6-x86_64-64bit-gcc44/lsst-utils/ts5/
export EO_SCRIPTS_HOME=/opt/lsst/redhat6-x86_64-64bit-gcc44/test/lsst-jh/
./plot_surf.py $1
#/home/ts5prod/Metrology_Scan_Data.csv
#gnome-terminal --command="./plot_surf.py /home/ts5prod/Metrology_Scan_Data.csv"
