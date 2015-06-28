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
    for transID in range(len(xypos)):
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
    t.ra         = radec[0]
    t.dec        = radec[1]
    t.x_pix      = xy[0]
    t.y_pix      = xy[1]
    t.width      = 10
    t.height     = 10
    t.filename   = "testFile.fits"
    t.dataset_id = "DBG_DJANGO"
    try:
      lastTC = TransientCandidate.objects.filter(dataset_id="DBG_DJANGO").order_by('-object_id')[0]
      last_id = lastTC.object_id
    except IndexError:
      last_id = 0
    t.object_id = last_id + 1
    t.save()
    t.refImg  = 'object_images/%s_ref.png' % (t.slug)
    t.subtImg = 'object_images/%s_subt.png' % (t.slug)
    t.origImg = 'object_images/%s_orig.png' % (t.slug)
    t.save()
    
    #Make all plots for this object
    thumb(xy[0], xy[1], t.filename, t.slug)
    return t

def downloadAndSaveTestFile():
    import urllib2
    url = "https://mega.co.nz/#!GNZWDToZ!nubGyQf6OrOEQFs9Gn48-3WDw7Z1pXP1mE6evo2vc5s"
    hdr = {'User-Agent':'Mozilla/5.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',}
    req = urllib2.Request(url, None, hdr)
    test_file = urllib2.urlopen(req)
    test_out = open("astro_images/testFile.fits", 'wb')
    test_out.write(test_file.read())
    test_out.close()

def thumb(x, y, filename, slug):
    semi_h = 20
    semi_w = 20
    
    from astropy.io import fits
    from toros.settings import ASTRO_IMAGE_DIR
    from os import path

    image_data = fits.getdata(path.join(ASTRO_IMAGE_DIR, filename))
    thumb_arr = image_data[y - semi_h: y + semi_h, x - semi_w: x + semi_w]

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(5,5))
    plt.imshow(thumb_arr, interpolation='none', cmap='gray')
    plt.xticks([]); plt.yticks([]) #Remove tick marks
    plt.tight_layout()

    img_dir = "media/object_images"
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    plt.savefig("%s/%s_subt.png" % (img_dir, slug))
    plt.savefig("%s/%s_orig.png" % (img_dir, slug))
    plt.savefig("%s/%s_ref.png" % (img_dir, slug))

    h_in, w_in = fig.get_size_inches()
    h_px, w_px = 400, 400
    plt.savefig("%s/%s_subt.normal.png" % (img_dir, slug), dpi=(h_px/h_in))
    plt.savefig("%s/%s_orig.normal.png" % (img_dir, slug), dpi=(h_px/h_in))
    plt.savefig("%s/%s_ref.normal.png" % (img_dir, slug), dpi=(h_px/h_in))
    h_px, w_px = 50, 50
    plt.savefig("%s/%s_subt.thumbnail.png" % (img_dir, slug), dpi=(h_px/h_in))
    plt.savefig("%s/%s_orig.thumbnail.png" % (img_dir, slug), dpi=(h_px/h_in))
    plt.savefig("%s/%s_ref.thumbnail.png" % (img_dir, slug), dpi=(h_px/h_in))

    plt.close()
    return

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
    
