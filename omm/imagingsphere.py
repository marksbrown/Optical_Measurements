'''
Functions used to process Imaging Sphere Data

Author : Mark S. Brown
Started : Thursday 16th January 2014
'''

from __future__ import division, print_function
from numpy import linspace, loadtxt, meshgrid
from matplotlib.pyplot import cm


def plotdata(df, ax, fig, plottype, **kwargs):
    nangle = kwargs.get('nangle', 181)
    N = kwargs.get('N', 100)
    ymax = kwargs.get('ymax', 1)
    lbl = kwargs.get('label', "")

    I = linspace(0, 180, nangle)
    
    data = loadtxt(df['fileloc'], skiprows=9)
    
    if plottype == 'slicex':    
        dataslice = data[int(nangle / 2), ...]
    if plottype == 'slicey':
        dataslice = data[..., int(nangle / 2)]
    if plottype == 'slicex' or plottype == 'slicey':
        ax.grid(True)
        ax.plot(I, dataslice, label=lbl)
        ax.set_ylim(0, ymax)
    if plottype == 'layer':
        ctf = ax.contourf(I, I, data, N, cmap=cm.hot, levels=linspace(0, ymax, N))
        cb = fig.colorbar(ctf, ax=ax, use_gridspec=True, shrink=0.7)
        cb.set_label("Intensity per unit area")
        cb.set_ticks(linspace(0, ymax, 5))
    if plottype == 'layer3D':
        Ix, Iy = meshgrid(I, I)
        surf = ax.plot_surface(Ix, Iy, data, rstride=5, cstride=5, vmax=ymax, 
                                cmap=cm.hot, linewidth=0, antialiased=False)
        ax.set_zlim(0, ymax)

        cb = fig.colorbar(surf, ax=ax, use_gridspec=True, shrink=0.5)
        cb.set_label("Intensity per unit area")
        cb.set_ticks(linspace(0, ymax, 5))
