import numpy as np


# can we use an astrometry.net-like algorithm to automatically figure out wavelength
#   identification and wavelength solution?
#  -instead of basically using "asterisms" what if we use patterns of lines and maybe
#   even patterns in flux?
#  -since an arc lamp can have multiple elements (e.g., HeNeAr), the patterns wouldn't
#   need to include "all" lines in a "group" of lines.
#  -the problem is that the "space" is "curves", i.e. if the group of 3-4 lines covers
#   a decent number of pixels, then you might not be able to assume that the wavelength
#   solution is linear.
#  -Dustin used 3/4 stars and measured the angles between the stars, he looked for unique
#   sets of angles, he did searches in healpix


def identify(data,linelist):
    """
    Identify emission lines in an arc spectrum in a linelist using
    patterns in the lines.
    """

    # 109 lines
    #lines=Table.read('/Users/nidever/sdss5/lvm/commissioning/data/60010/zband_neon.csv')
    #lines['obs_wl_air(A)'].name = 'wave'
    #gd, = np.where(lines['intens'] > 10)
    ## 70
    #lines = lines[gd]

    wlist = []
    for i in range(len(lines)-2):
        lines3 = linelist[i:i+3]   # get three neighboring lines in linelist
        w = lines3['wave'].data
        flux = lines3['intens'].data
        dw1 = (w[1]-w[0])/w[1]
        dw2 = (w[2]-w[1])/w[1]
        dflux1 = flux[0]/flux[1]
        dflux2 = flux[2]/flux[1]
        fratio = dflux1/dflux2
        if fratio < 1:
            fratio = 1/fratio
        if dw1>dw2:
            wratio = dw1/dw2
        else:
            wratio = dw2/dw1
        print(wratio)
        if wratio > 1.5 and wratio < 4:
            wdict = {'wave':w,'dw1':dw1,'dw2':dw2,'wratio12':dw1/dw2,'wratio':wratio,
                     'flux':flux,'dflux1':dflux1,'dflux2':dflux2,'fratio':fratio}
            wlist.append(wdict)

    # Now check the observed peaks

    rim,head = fits.getdata('/Users/nidever/sdss5/lvm/commissioning/data/60010/sdR-s-z1-00000082.fits.gz',header=True)
    #im=subtract_overscan(rim)
    im = subtract_overscan_new(rim)
    flux = np.sum(im[2058:2065,:],axis=0).astype(float)
    ptab = peakfit.peakfit(flux)
    ptab = Table(ptab)
    ptab['x'] = ptab['pars'][:,1]
    ptab['sigx'] = ptab['pars'][:,2]
    ptab['height'] = ptab['pars'][:,0]
    # 69

    # 58
    gd, = np.where(np.isfinite(ptab['height']))
    ptab = ptab[gd]

    obslist = []
    for i in range(len(ptab)-2):
        ptab3 = ptab[i:i+3]
        w = ptab3['x'].data
        flux = ptab3['height'].data
        dw1 = (w[1]-w[0])/w[1]
        dw2 = (w[2]-w[1])/w[1]
        dflux1 = flux[0]/flux[1]
        dflux2 = flux[2]/flux[1]
        fratio = dflux1/dflux2
        if fratio < 1:
            fratio = 1/fratio
        if dw1>dw2:
            wratio = dw1/dw2
        else:
            wratio = dw2/dw1
        print(wratio)
        if wratio > 1.5 and wratio < 4:
            wdict = {'wave':w,'dw1':dw1,'dw2':dw2,'wratio12':dw1/dw2,'wratio':wratio,
                     'flux':flux,'dflux1':dflux1,'dflux2':dflux2,'fratio':fratio}
            obslist.append(wdict)

    # Now match the two lists
    for i in range(len(obslist)):
        obslist1 = obslist[i]
        obs_wratio = obslist1['wratio']
        obs_fratio = obslist1['fratio']
        for j in range(len(wlist)):
            print(obslist1['wratio12'],wlist[j]['wratio12'])
	    wratio = wlist[j]['wratio']
	    fratio = wlist[j]['fratio']	
	    if np.abs((obs_wratio-wratio)/wratio) < 0.02:
	        print('match ',obs_wratio,wratio)


    # could call it wavefinder or waverider

            
    return wlist
