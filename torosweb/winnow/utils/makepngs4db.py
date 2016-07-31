"""
Creates object image files (png) from a subtraction image, to upload later to the database

   ### Usage: 
   
       python makepngs4db.py [options] -d,--dataset= <dataSetName> 
                             -p,--path= <directory with FITS files> inputfile
   
   ### Keywords:
   * -d, --dataset: The name of the data set to upload to the database
   * -p, --path:    The path to directory with the FITS files
   * inputfile:     Catalog file with object metadata to be read by load module

   ### Options:
   * -h, --help: Prints this help and exits.
   * -v, --version: Prints version information.

   Martin Beroiz - 2014
   
   email: <martinberoiz@phys.utb.edu>
   
   University of Texas at San Antonio
"""



__version__ = '0.1'


def version():
    print "Version %s" % (__version__)
    print "Martin Beroiz - 2015\nmartinberoiz@phys.utb.edu\nUniversity of Texas at San Antonio"


def makePNGs(obj, refFITSFile, imgFITSFile, subtFITSFile, slug):
    import matplotlib
    matplotlib.use('Agg')
    import aplpy
    import matplotlib.pyplot as plt
    from astropy.io import fits

    def plot_obj_png(image_file_name, obj, out_filename):
        x, y = obj['x'], obj['y']

        image_data = fits.getdata(image_file_name)
        semih, semiw = 15, 15
        xmin, xmax = max(0, int(x) - semiw), min(image_data.shape[1], int(x) + semiw)
        ymin, ymax = max(0, int(y) - semih), min(image_data.shape[0], int(y) + semih)
        
        image_thumb = image_data[ymin: ymax, xmin: xmax]
        fig = plt.figure(figsize=(5,5))
        plt.imshow(image_thumb, interpolation='none', cmap='gray')
        plt.xticks([]); plt.yticks([]) #Remove tick marks
        border_x, border_y = 1, 1
        xobj_i = obj['xmin'] - xmin + 0.5 - border_x
        yobj_i = obj['ymin'] - ymin - 0.5 - 1
        obj_w = obj['xmax'] - obj['xmin'] + 2*border_x
        obj_h = obj['ymax'] - obj['ymin'] + 2*border_y

        #Get the mask, if any
        hdulist = fits.open(image_file_name)
        has_mask = False
        mask = np.zeros(image_thumb.shape, dtype='bool')
        for anhdu in hdulist:
            try:
                ext = anhdu.header['extname'].lower()
            except KeyError:
                ext = ""
            if 'bad' in ext or 'mask' in ext or 'bled' in ext:
                hdumask = anhdu.data.astype('bool')[ymin: ymax, xmin: xmax]
                if hdumask.any():
                    has_mask = True
                    mask = mask | hdumask

        if has_mask:
            rows, cols = np.indices(mask.shape)
            for x_row, y_row in zip(*np.indices(mask.shape)):
                for x, y in zip(x_row, y_row):
                    if mask[x,y]:
                        plt.gca().add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, fill=True, color='red', alpha=0.1))
        
        plt.gca().add_patch(plt.Rectangle((xobj_i, yobj_i), 
                                          obj_w, obj_h, 
                                          fill=False, 
                                          ec='green'))

        plt.tight_layout()
        
        h_in, w_in = fig.get_size_inches()
        plt.savefig(out_filename + ".png")

        h_px, w_px = 400, 400
        plt.savefig(out_filename + ".normal.png", dpi=(w_px/w_in))
        h_px, w_px = 50, 50
        plt.savefig(out_filename + ".thumbnail.png", dpi=(w_px/w_in))
        plt.close(fig)

    #def plot_obj_png(image_file_name, x, y, out_filename):
    #    mpfig = plt.figure(figsize=(5,5))
    #    mpfig.set_tight_layout(True)
    #    fig = aplpy.FITSFigure(image_file_name, figure=mpfig)
    #    fig.recenter(*fig.pixel2world(x,y), radius=0.05)
    #    fig.show_grayscale()
    #    fig.hide_axis_labels()
    #    fig.hide_tick_labels()
    #    fig.set_theme('publication')
    #    #fig.show_colorbar()
    #    fig.show_scalebar(1./60., label="1 arcsec", corner="top right")
    #
    #    h_in, w_in = mpfig.get_size_inches()
    #    mpfig.savefig(out_filename + ".png")
    #    h_px, w_px = 400, 400
    #    mpfig.savefig(out_filename + ".normal.png",    dpi=(w_px/w_in))
    #    h_px, w_px = 50, 50
    #    #fig.colorbar.hide()
    #    fig.scalebar.hide()
    #    mpfig.savefig(out_filename + ".thumbnail.png", dpi=(w_px/w_in))
    #
    #    fig.close()

    img_dir = "media/object_images"
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    plot_obj_png(subtFITSFile, obj, os.path.join(img_dir, slug + "_subt"))
    plot_obj_png(imgFITSFile,  obj, os.path.join(img_dir, slug + "_orig"))
    plot_obj_png(refFITSFile,  obj, os.path.join(img_dir, slug + "_ref"))
    return

if __name__ == '__main__':
    import sys
    import getopt
    import numpy as np
    import os
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvd:r:p:", ["help", "version", "dataset=", "path="])
    except getopt.GetoptError:
        print(__doc__)
        sys.exit(2)

    dataset   = None
    refFile   = None
    files_path = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(__doc__)
            sys.exit(2)
        if opt in ('-v', '--version'):
            version()
            sys.exit(2)
        if opt in ('-d', '--dataset'):
            dataset = arg
        if opt in ('-p', '--path'):
            files_path = arg

    if dataset is None:
        print("You need to specify a dataset name with keyword -d")
        print("Run addOjectsToDB --help for more help")
        sys.exit(2)

    if files_path is None:
        print("You need to specify a path for the FITS files with keyword -p")
        print("Run addOjectsToDB --help for more help")
        sys.exit(2)

    inputfile = args[:][0]

    loader_module = __import__("load_" + dataset)
    object_list = loader_module.load(inputfile)
    ntotal_objs = len(object_list)
    for nobj, anobj in enumerate(object_list):
        print("Making object %d of %d" % (nobj + 1, ntotal_objs))

        # Get the path for all the files
        diff_filename = anobj['filename']
        base, ext = diff_filename.split(".fits")
        ext = ".fits" + ext
        orig_filename = base.replace("_diff", "") + ext
        ref_filename = base.replace("_diff", "_ref") + ext

        import shlex
        from subprocess import check_output
        cmd = "find %s -name %s" % (files_path, diff_filename)
        diff_path = check_output(shlex.split(cmd)).strip().split()[0]
        cmd = "find %s -name %s" % (files_path, orig_filename)
        orig_path = check_output(shlex.split(cmd)).strip().split()[0]
        cmd = "find %s -name %s" % (files_path, ref_filename)
        ref_path = check_output(shlex.split(cmd)).strip().split()[0]

        # Make all png's for this object
        slug = '%s_%05d' % (dataset, anobj['object_id'])
        makePNGs(anobj, ref_path, orig_path, diff_path, slug)
