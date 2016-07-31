import numpy as np

def load(filename):
    from astropy.io import ascii
    cstar_june02_pr_data = np.array(ascii.read(filename))
    objects = np.zeros(cstar_june02_pr_data.shape, dtype=[('object_id', '<i8'),
                                                          ('filename', 'S50'), 
                                                          ('dataset', 'S50'),
                                                          ('thresh', '<f8'), 
                                                          ('npix', '<i8'), 
                                                          ('tnpix', '<i8'), 
                                                          ('xmin', '<i8'), 
                                                          ('xmax', '<i8'), 
                                                          ('ymin', '<i8'), 
                                                          ('ymax', '<i8'), 
                                                          ('x', '<f8'), 
                                                          ('y', '<f8'), 
                                                          ('x2', '<f8'), 
                                                          ('y2', '<f8'), 
                                                          ('xy', '<f8'), 
                                                          ('a', '<f8'), 
                                                          ('b', '<f8'), 
                                                          ('theta', '<f8'), 
                                                          ('cxx', '<f8'), 
                                                          ('cyy', '<f8'), 
                                                          ('cxy', '<f8'), 
                                                          ('cflux', '<f8'), 
                                                          ('flux', '<f8'), 
                                                          ('cpeak', '<f8'), 
                                                          ('peak', '<f8'), 
                                                          ('xcpeak', '<i8'), 
                                                          ('ycpeak', '<i8'), 
                                                          ('xpeak', '<i8'), 
                                                          ('ypeak', '<i8'), 
                                                          ('flag', '<i8'), 
                                                          ('ra', '<f8'), 
                                                          ('dec', '<f8'),
                                                          ])

    objects['dataset']   = cstar_june02_pr_data['DATASET']
    objects['object_id'] = cstar_june02_pr_data['OBJECT_ID']
    objects['filename']  = cstar_june02_pr_data['FILENAME']
    try:
      objects['xmin']   = cstar_june02_pr_data['XMIN_IMAGE']
      objects['xmax']   = cstar_june02_pr_data['XMAX_IMAGE']
      objects['ymin']   = cstar_june02_pr_data['YMIN_IMAGE']
      objects['ymax']   = cstar_june02_pr_data['YMAX_IMAGE']
      objects['x']      = cstar_june02_pr_data['X_IMAGE']
      objects['y']      = cstar_june02_pr_data['Y_IMAGE']
      objects['x2']     = cstar_june02_pr_data['X2_IMAGE']
      objects['y2']     = cstar_june02_pr_data['Y2_IMAGE']
      objects['xy']     = cstar_june02_pr_data['XY_IMAGE']
      objects['a']      = cstar_june02_pr_data['A_IMAGE']
      objects['b']      = cstar_june02_pr_data['B_IMAGE']
      objects['theta']  = cstar_june02_pr_data['THETA_IMAGE']
      objects['cxx']    = cstar_june02_pr_data['CXX_IMAGE']
      objects['cyy']    = cstar_june02_pr_data['CYY_IMAGE']
      objects['cxy']    = cstar_june02_pr_data['CXY_IMAGE']
      objects['cflux']  = cstar_june02_pr_data['FLUX_APER']
      objects['flux']   = cstar_june02_pr_data['FLUX_APER']
      objects['cpeak']  = cstar_june02_pr_data['FLUX_MAX']
      objects['peak']   = cstar_june02_pr_data['FLUX_MAX']
      objects['xcpeak'] = cstar_june02_pr_data['XPEAK_IMAGE']
      objects['ycpeak'] = cstar_june02_pr_data['YPEAK_IMAGE']
      objects['xpeak']  = cstar_june02_pr_data['XPEAK_IMAGE']
      objects['ypeak']  = cstar_june02_pr_data['YPEAK_IMAGE']
      objects['flag']   = cstar_june02_pr_data['FLAGS']
      objects['ra']     = cstar_june02_pr_data['RA']
      objects['dec']    = cstar_june02_pr_data['Dec']
    except:
      pass

    return objects


