import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torosweb.settings')

import django
django.setup()

import numpy as np

from winnow.models import TransientCandidate, Ranking, UserProfile, Dataset, SEPInfo

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
    for transID in range(len(xypos)):
        transient = add_transient(xypos[transID], radecpos[transID])    
        for lastID in range(0,3):
            myUser = createUser(lastID)
            add_ranking(transient, user=myUser)

def add_ranking(t, user):   
    r = Ranking()
    r.ranker = user
    r.trans_candidate = t
    r.rank = np.random.random_integers(-1,1)
    r.isInteresting = np.random.uniform(0.,1.) < 0.5
    r.save()
    return r

def add_transient(xy, radec):
    ds = Dataset.objects.get_or_create(name="DBG_DJANGO")[0]
    t = TransientCandidate()
    t.ra         = radec[0]
    t.dec        = radec[1]
    t.x_pix      = xy[0]
    t.y_pix      = xy[1]
    t.width      = 10
    t.height     = 10
    t.filename   = "testFile.fits"
    t.dataset = ds
    try:
      lastTC = TransientCandidate.objects.filter(dataset=ds).order_by('-object_id')[0]
      last_id = lastTC.object_id
    except IndexError:
      last_id = 0
    t.object_id = last_id + 1
    t.save()
    t.refImg  = 'object_images/no_image.png'
    t.subtImg = 'object_images/no_image.png'
    t.origImg = 'object_images/no_image.png'
    t.save()
    addSEPInfo(t)
    return t

def addSEPInfo(tc):
    sep = SEPInfo()
    sep.trans_candidate = tc
    sep.thresh = 1.0
    sep.npix   = 1
    sep.tnpix  = 1
    sep.xmin   = 1
    sep.xmax   = 1
    sep.ymin   = 1
    sep.ymax   = 1
    sep.x      = 1.0
    sep.y      = 1.0
    sep.x2     = 1.0
    sep.y2     = 1.0
    sep.xy     = 1.0
    sep.a      = 1.0
    sep.b      = 1.0
    sep.theta  = 1.0
    sep.cxx    = 1.0
    sep.cyy    = 1.0
    sep.cxy    = 1.0
    sep.cflux  = 1.0
    sep.flux   = 1.0
    sep.cpeak  = 1.0
    sep.peak   = 1.0
    sep.xcpeak = 1
    sep.ycpeak = 1
    sep.xpeak  = 1
    sep.ypeak  = 1
    sep.flag   = 1
    sep.isDeleted = 0
    sep.save()

# Start execution here!
if __name__ == '__main__':
    print("Starting winnow population script...")
    xypos = np.array([[363, 72],
                      [871, 610],
                      [473, 940],
                      [331, 832],
                      [955, 829],
                      [578, 709],
                      [820, 765],
                      [970, 819],
                      [1016, 782],
                      [73, 799]])
    radecpos = np.array([[74.03852734,  -87.89001901],
                         [ 198.75514552,  -88.48581972],
                         [ 283.0185146,   -88.1738623 ],
                         [ 308.17223923,  -88.40106574],
                         [ 220.51342198,  -87.73948239],
                         [ 261.10420734,  -89.17853841],
                         [ 224.57000915,  -88.37388738],
                         [ 218.66990854,  -87.70653163],
                         [ 212.78004925,  -87.620442  ],
                         [ 333.98498108,  -87.66825998]])
    
    print("Downloadind and saving test file...")
    #try:
    #    downloadAndSaveTestFile()
    #    print("File saved to astro_images/")
    #except:
    #    print("Problem downloading and saving test file.")

    populate(xypos, radecpos)
        
    # Print out what we have added.
    print("This has been added to the database:")
    for t in TransientCandidate.objects.all():
        for r in Ranking.objects.filter(trans_candidate=t):
            print "Transient {0} - Ranking {1} by User: {2}".format(str(t), str(r),str(r.ranker))
    
