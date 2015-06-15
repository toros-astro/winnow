import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toros.settings')
import django
django.setup()
import numpy as np
from winnow.models import TransientCandidate, Ranking, UserProfile

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

if __name__ == '__main__':
    print("Adding columns to table manually.")
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE winnow_transientcandidate ADD COLUMN refImg varchar(100)")
    cursor.execute("ALTER TABLE winnow_transientcandidate ADD COLUMN origImg varchar(100)")
    cursor.execute("ALTER TABLE winnow_transientcandidate ADD COLUMN subtImg varchar(100)")

    for obj in TransientCandidate.objects.filter(dataset_id="DBG_DJANGO"):
        thumb(obj.x_pix, obj.y_pix, obj.filename, obj.slug)
        obj.refImg  = 'object_images/%s_ref.png' % (obj.slug)
        obj.subtImg = 'object_images/%s_subt.png' % (obj.slug)
        obj.origImg = 'object_images/%s_orig.png' % (obj.slug)
        obj.save()
        print("Object %s, done" % (obj.slug))
