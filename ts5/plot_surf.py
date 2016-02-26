#!/usr/bin/env python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import lsst.afw.math as afwMath
import pylab
import sys

xin=[]
yin=[]
zin=[]
idx = 0
#fln = 'ttc10pp'
#infile = "%s.csv" % fln
infile = sys.argv[1]

input = open(infile, 'r')

for line in input :
    print "line = %s" % line
    xin.append(float(line.split(",")[0]))
    yin.append(float(line.split(",")[1]))
    zin.append(float(line.split(",")[2]))
input.close()

size = 'medium'
fig = plt.figure()
colors = ['k', "#B3C95A", 'b', '#63B8FF', 'g', "#FF3300",
          'r', 'k']

ax = fig.gca(projection='3d')
ax.scatter(xin, yin, zin)

ax.set_xlabel('Aerotech X (mm)')
#ax.set_xlim(-x_dim/2-1, x_dim/2+1)
ax.set_ylabel('Aerotech Y (mm)')
#ax.set_ylim(-y_dim/2-1, y_dim/2+1)
ax.set_zlabel('Displacement (mm)')
#ax.set_zlim(v_min, v_max)

plt.draw()
plt.show()

#plt.savefig('surface_plot.png')
