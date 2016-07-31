import numpy as np


def load(filename):
    from astropy.io import ascii
    cstar_june01_data = np.array(ascii.read(filename))
    objects = np.zeros(cstar_june01_data.shape, dtype=[('object_id', '<i8'),
                                                       ('filename', 'S18'),
                                                       ('dataset', 'S13'),
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

    objects['dataset']   = cstar_june01_data['sample_name']
    objects['object_id'] = cstar_june01_data['sourceid']
    objects['filename']  = cstar_june01_data['source_file']
    try:
        objects['xmin']   = cstar_june01_data['xmin_image']
        objects['xmax']   = cstar_june01_data['xmax_image']
        objects['ymin']   = cstar_june01_data['ymin_image']
        objects['ymax']   = cstar_june01_data['ymax_image']
        objects['x']      = cstar_june01_data['x_image']
        objects['y']      = cstar_june01_data['y_image']
        objects['x2']     = cstar_june01_data['x2_image']
        objects['y2']     = cstar_june01_data['y2_image']
        objects['xy']     = cstar_june01_data['xy_image']
        objects['a']      = cstar_june01_data['a_image']
        objects['b']      = cstar_june01_data['b_image']
        objects['theta']  = cstar_june01_data['theta_image']
        objects['cxx']    = cstar_june01_data['cxx_image']
        objects['cyy']    = cstar_june01_data['cyy_image']
        objects['cxy']    = cstar_june01_data['cxy_image']
        objects['cflux']  = cstar_june01_data['flux_aper']
        objects['flux']   = cstar_june01_data['flux_aper']
        objects['cpeak']  = cstar_june01_data['flux_max']
        objects['peak']   = cstar_june01_data['flux_max']
        objects['xcpeak'] = cstar_june01_data['xpeak_image']
        objects['ycpeak'] = cstar_june01_data['ypeak_image']
        objects['xpeak']  = cstar_june01_data['xpeak_image']
        objects['ypeak']  = cstar_june01_data['ypeak_image']
        objects['flag']   = cstar_june01_data['flags']
        objects['ra']     = cstar_june01_data['alpha_sky']
        objects['dec']    = cstar_june01_data['delta_sky']
    except:
        pass

    return objects
