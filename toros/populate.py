import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toros.settings')

import django
django.setup()

import numpy as np

from winnow.models import TransientCandidate, Ranking, UserProfile

def createUser(lastUserID):
    from django.contrib.auth.models import User
    aUser = User.objects.get_or_create(username="populate%02d" % (lastUserID+1))[0]
    aUser.first_name = "Populate"
    aUser.last_name = "Anon%02d" % (lastUserID + 1)
    aUser.save()
    myUser = UserProfile.objects.get_or_create(user=aUser)[0]
    myUser.save()
    return myUser
    
def populate(xypos, radecpos):
    for transID in range(0,5):
        transient = add_transient(xypos[transID], radecpos[transID])    
        for lastID in range(0,3):
            myUser = createUser(lastID)
            add_ranking(transient, user=myUser)

def add_ranking(t, user):   
    r = Ranking()
    r.ranker = user
    r.trans_candidate = t
    rank_options = ['B','R','X']
    r.rank = rank_options[np.random.random_integers(0,2)]
    r.isInteresting = np.random.uniform(0.,1.) < 0.5
    r.save()
    return r

def add_transient(xy, radec):
    t = TransientCandidate()
    t.ra       = radec[0]
    t.dec      = radec[1]
    t.x_pix    = xy[0]
    t.y_pix    = xy[1]
    t.width    = 10
    t.height   = 10
    t.filename = "testFile.fits"
    t.save()
    return t
    
    
def findTransients():
    from toros.settings import ASTRO_IMAGE_DIR
    from astropy.io import fits

    subt_hdulist = fits.open(os.path.join(ASTRO_IMAGE_DIR, "testFile.fits"))
    data = np.ma.array(subt_hdulist[0].data, mask = subt_hdulist[0].data == -99999)
    
    from astropy.stats import median_absolute_deviation as mad
    image = data.filled(fill_value=0.)
    bkg_sigma = mad(image)
    import photutils
    sources = photutils.daofind(image, fwhm=4., threshold=3.*bkg_sigma)
    sources.sort('flux')
    
    from photutils import aperture_photometry, CircularAperture
    positions = (sources['xcentroid'], sources['ycentroid'])    
    apertures = CircularAperture(positions, r=4.)    
    phot_table = aperture_photometry(image, apertures)
    
    xypos = np.array([[x,y] for x,y in zip(sources[-100:]['xcentroid'], sources[-100:]['ycentroid'])])
    from astropy import wcs
    w = wcs.WCS(subt_hdulist[0].header)
    radecpos = w.wcs_pix2world(xypos, 1)
    return xypos, radecpos
    


# Start execution here!
if __name__ == '__main__':
    print "Starting winnow population script..."
    xypos, radecpos = findTransients()
    populate(xypos, radecpos)
    # Print out what we have added.
    for t in TransientCandidate.objects.all():
        for r in Ranking.objects.filter(trans_candidate=t):
            print "Transient {0} - Ranking {1} by User: {2}".format(str(t), str(r),str(r.ranker))
    
