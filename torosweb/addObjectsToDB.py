"""
Upload objects in a subtraction image to website database.
This should be used after running makepngs4db.py
   
   ### Usage: 
   
       python addObjectsToDB.py [options] -f <numpy object file> -p <images directory>
   
   ### Keywords:
   * -f:         The name of the numpy file that stores the objects 
   * -p, --path: The directory that contains the images

   ### Options:
   * -h, --help: Prints this help and exits.
   * -v, --version: Prints version information.

   Martin Beroiz - 2015
   
   email: <martinberoiz@phys.utb.edu>
   
   University of Texas at San Antonio
"""



__version__ = '0.1'


def version():
    print "Version %s" % (__version__)
    print "Martin Beroiz - 2015\nmartinberoiz@phys.utb.edu\nUniversity of Texas at San Antonio"


def add_transient(obj):
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torosweb.settings')
    import django
    django.setup()
    from winnow.models import TransientCandidate

    t = TransientCandidate()
    t.ra         = obj['ra']
    t.dec        = obj['dec']
    t.x_pix      = obj['x']
    t.y_pix      = obj['y']
    t.height     = obj['ymax'] - obj['ymin']
    t.width      = obj['xmax'] - obj['xmin']
    t.filename   = obj['filename']
    t.dataset_id = obj['dataset']
    try:
      lastTC = TransientCandidate.objects.filter(dataset_id=dataset).order_by('-object_id')[0]
      last_id = lastTC.object_id
    except IndexError:
      last_id = 0
    t.object_id = last_id + 1
    t.save()
    t.refImg  = 'object_images/%s_ref.png' % (t.slug)
    t.subtImg = 'object_images/%s_subt.png' % (t.slug)
    t.origImg = 'object_images/%s_orig.png' % (t.slug)
    t.save()

    return t

def addSEPInfo(obj, tc):
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torosweb.settings')
    import django
    django.setup()
    from winnow.models import SEPInfo

    newSEP = SEPInfo()
    newSEP.trans_candidate = tc
    newSEP.thresh   = obj['thresh']
    newSEP.npix     = obj['npix']
    newSEP.tnpix    = obj['tnpix']
    newSEP.xmin     = obj['xmin']
    newSEP.xmax     = obj['xmax']
    newSEP.ymin     = obj['ymin']
    newSEP.ymax     = obj['ymax']
    newSEP.x        = obj['x']
    newSEP.y        = obj['y']
    newSEP.x2       = obj['x2']
    newSEP.y2       = obj['y2']
    newSEP.xy       = obj['xy']
    newSEP.a        = obj['a']
    newSEP.b        = obj['b']
    newSEP.theta    = obj['theta']
    newSEP.cxx      = obj['cxx']
    newSEP.cyy      = obj['cyy']
    newSEP.cxy      = obj['cxy']
    newSEP.cflux    = obj['cflux']
    newSEP.flux     = obj['flux']
    newSEP.cpeak    = obj['cpeak']
    newSEP.peak     = obj['peak']
    newSEP.xcpeak   = obj['xcpeak']
    newSEP.ycpeak   = obj['ycpeak']
    newSEP.xpeak    = obj['xpeak']
    newSEP.ypeak    = obj['ypeak']
    newSEP.flag     = obj['flag']
    newSEP.ra       = obj['ra']
    newSEP.dec      = obj['dec']
    newSEP.save()

    return newSEP

if __name__ == '__main__':
    import sys
    import getopt
    import numpy as np
    import os
        
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvp:f:", ["help", "version", "path="])
    except getopt.GetoptError:
        print(__doc__)
        sys.exit(2)

    img_path = None
    numpyfile = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print __doc__
            sys.exit(2)
        if opt in ('-v', '--version'):
            version()
            sys.exit(2)
        if opt in ('-f',):
            numpyfile = arg
        if opt in ('-p', '--path'):
            img_path = arg

    object_list = np.load(numpyfile)

    for obj in object_list[:20]:
        #Save metadata to info file
        dataset = obj['dataset']
        obj_id  = obj['object_id']

        #Insert models in the database
        newTC = add_transient(obj)
        addSEPInfo(obj, newTC)

        #Do the copy to final destination
        from shutil import copyfile
        #Copy the subtraction images
        afile = os.path.join(img_path, "%s_%05d_%s" % (dataset, obj_id, "subt"))
        copyfile(afile + '.png',           newTC.subtImg.url[1:])
        copyfile(afile + '.thumbnail.png', newTC.subtImg.url[1:-4] + '.thumbnail.png')
        copyfile(afile + '.normal.png',    newTC.subtImg.url[1:-4] + '.normal.png')

        #Copy the reference images
        afile = os.path.join(img_path, "%s_%05d_%s" % (dataset, obj_id, "ref"))
        copyfile(afile + '.png',           newTC.refImg.url[1:])
        copyfile(afile + '.thumbnail.png', newTC.refImg.url[1:-4] + '.thumbnail.png')
        copyfile(afile + '.normal.png',    newTC.refImg.url[1:-4] + '.normal.png')

        #Copy the original images
        afile = os.path.join(img_path, "%s_%05d_%s" % (dataset, obj_id, "orig"))
        copyfile(afile + '.png',           newTC.origImg.url[1:])
        copyfile(afile + '.thumbnail.png', newTC.origImg.url[1:-4] + '.thumbnail.png')
        copyfile(afile + '.normal.png',    newTC.origImg.url[1:-4] + '.normal.png')

