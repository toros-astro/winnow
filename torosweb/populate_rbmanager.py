import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torosweb.settings')

import django
django.setup()

from django.contrib.auth.models import User
from rbmanager.models import Experiment, Feature
from winnow.models import UserProfile, Dataset


def create_user(last_user_id):
    auser, created = User.objects.get_or_create(
        username="populate%02d" % (last_user_id + 1))
    if created:
        auser.first_name = "Populate"
        auser.last_name = "Anon%02d" % (last_user_id + 1)
        auser.save()
    myuser, created = UserProfile.objects.get_or_create(user=auser)
    if created:
        myuser.save()
    return myuser


def populate(num_users, num_exp_per_user):
    dbg_dataset, created = Dataset.objects.get_or_create(name='DBG_DJANGO')
    if created:
        dbg_dataset.isCurrent = False
        dbg_dataset.save()
    print("Saved Dataset {}.".format(dbg_dataset))

    for userid in range(num_users):
        myuser = create_user(userid)
        for exp_counter in range(num_exp_per_user):
            exp = add_experiment(myuser, dbg_dataset)
            print("Saved experiment {} for user {}".format(exp, myuser))
            for name, description in get_features():
                feat, created = Feature.objects.get_or_create(name=name)
                if created:
                    feat.description = description
                    feat.save()
                exp.features.add(feat)
                print("Saved feature {} for experiment {}".format(feat, exp))
            print("")


def get_features():
    import random
    feat_all = [('num_neg_pix', 'number of negative pixels'),
                ('roundness', 'a/b major over minor semiaxis'),
                ('width', ''),
                ('height', ''),
                ('sep_flags', 'flags returned by SExtractor'),
                ('close_to_boundary', "boolean if it's close to image bounds"),
                ('fwhm_x', 'Full width half maximum in x direction'),
                ('fwhm_y', 'Full width half maximum in y direction')]
    random.shuffle(feat_all)
    return feat_all[:3]


def add_experiment(user, dataset):
    import datetime as d
    import random
    exp = Experiment()
    exp.user = user
    exp.dataset = dataset
    exp.date = d.datetime.now()
    exp.platform = str(random.randint(0, 3))
    if exp.platform == '3':
        exp.other_platform_name = "Mystery ML"
    exp.alg_name = "Random Forest"
    exp.params_file = "params_01.txt"
    exp.labels_file = "labels_01.txt"
    exp.featureset_infofile = "feat_01.txt"
    exp.featuretable_datafile = "all_feat.txt"

    exp.conf_mat_rr = random.randint(10, 100)
    exp.conf_mat_rb = random.randint(10, 100)
    exp.conf_mat_br = random.randint(10, 100)
    exp.conf_mat_bb = random.randint(10, 100)
    exp.confusion_table_file = "weka_results.weka"

    exp.description = "Mock Data in populate script. "
    "Meant for debugging purposes."
    exp.save()
    return exp


if __name__ == '__main__':
    print("Starting rbmamager population script...")
    populate(3, 5)

