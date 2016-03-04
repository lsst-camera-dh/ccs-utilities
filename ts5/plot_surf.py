#!/usr/bin/env python
####################################################################
# plot_surf.py
#
# created for LSST TS5 Metrology Operations
#
# original version by Homer Neal on 20160303
#
####################################################################
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
import matplotlib.mlab as mlab

import numpy as np
import lsst.afw.math as afwMath
import pylab
import sys

xin=[]
yin=[]
zin=[]
xdif=[]
ydif=[]
idx = 0

infile = sys.argv[1]

input = open(infile, 'r')

size = 'medium'

#fig, axes = plt.subplots(ncols=2, nrows=1)
#ax, ax4 = axes.ravel()

fig1 = plt.figure()
fig = plt.figure()
colors = ['k', "#B3C95A", 'b', '#63B8FF', 'g', "#FF3300",
          'r', 'k']

ax = fig1.gca(projection='3d')
ax4 = fig.gca()

xprev = -999.
yprev = -999.
first = True
for line in input :
#    print "line = %s" % line
    xl = float(line.split(",")[0])
    yl = float(line.split(",")[1])
    zl = float(line.split(",")[2])
    xin.append(xl)
    yin.append(yl)
    zin.append(zl)
    if (not first) :
        xd = abs(xl - xprev)
        yd = abs(yl - yprev)
        if (xd > 0.0) :
            xdif.append(xd)
        if (yd > 0.0) :
            ydif.append(yd)
    first = False
    xprev = xl
    yprev = yl

#    zmin = 10.0
#    zmax = 15.0

xi = np.asarray(xin)
yi = np.asarray(yin)
zi = np.asarray(zin)


csizex = min(xdif) / 2.0
csizey = min(ydif) / 2.0
csize = min([csizex, csizey])

xmin = np.amin(xi) - csize
xmax = np.amax(xi) + csize

ymin = np.amin(yi) - csize
ymax = np.amax(yi) + csize

print "circle size will be %f" % csize

stdz = np.std(zi)
meanz = np.median(zi)

zmin = meanz - 0.5*stdz
zmax = meanz + 0.5*stdz

for xp,yp,zp in zip(xin,yin,zin):
    xy = [xp,yp]
    if (zp>zmin and zp<zmax) :

#        val = (zl-zmin)/(zmax-zmin) * 16777214.0 + 1.0
#        r = int(val / 65536)
#        val = val - (r*65536)
#        g = int(val/256)
#        val = val - (g*256)
#        b = int(val)

        val = (zp-zmin)/(zmax-zmin) * 254.0 + 1.0
        r = int(val)
        b = int(256.0-val)
        g = int(128.0-abs(128.0-val))

        rgb = "#%2.2X%2.2X%2.2X" % (r,g,b)
#        print "rgb = %s" % rgb

        ax4.add_patch(plt.Circle(xy, radius=csize, color=rgb))

input.close()

ax.scatter(xin, yin, zin)

ngridx = 100
ngridy = 200
xg = np.linspace(-20.1, 100.1, ngridx)
yg = np.linspace(-120.1, 10.1, ngridy)

#fig.colorbar(surf, shrink=0.5, aspect=5)

ax.set_xlabel('Aerotech X (mm)')
ax.set_ylabel('Aerotech Y (mm)')
ax.set_zlabel('Displacement (mm)')

ax4.set_xlabel('Aerotech X (mm)   -  blue = %8.3f , red - %8.3f' % (zmin,zmax))
ax4.set_ylabel('Aerotech Y (mm)')
#ax.set_zlabel('Displacement (mm)')

#ax4.set_xlim(-20., 100.)
#ax4.set_ylim(-120., 10.)
ax4.set_xlim(xmin, xmax)
ax4.set_ylim(ymin, ymax)
#ax.set_zlim(v_min, v_max)

plt.draw()
plt.show()

#plt.savefig('surface_plot.png')
##########################################################################
# attic:
#X = np.arange(-5, 5, 0.25)
#Y = np.arange(-5, 5, 0.25)
#X, Y = np.meshgrid(X, Y)
#R = np.sqrt(X**2 + Y**2)
#Z = np.sin(R)

#surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
#                       linewidth=0, antialiased=False)
#ax.set_zlim(10., 12.)

#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#zg = mlab.griddata(xi, yi, zi, xg, yg, interp='linear')
#plt.contour(xg, yg, zg, 15, linewidths=0.5, colors='k')
#plt.contourf(xg, yg, zg, 15, cmap=plt.cm.rainbow,
#             norm=plt.Normalize(vmax=abs(zg).max(), vmin=-abs(zg).max()))

#surf = ax.plot_surface(xg, yg, zg, rstride=1, cstride=1, cmap=cm.coolwarm,
#                       linewidth=0, antialiased=False)
