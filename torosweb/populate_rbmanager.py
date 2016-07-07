import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth.models import User
from rbmanager.models import Experiment, Dataset


def create_user(last_user_id):
    auser = User.objects.get_or_create(username="populate%02d" %
                                       (last_user_id + 1))[0]
    auser.first_name = "Populate"
    auser.last_name = "Anon%02d" % (last_user_id + 1)
    auser.save()
    return auser


def populate(num_users, num_exp_per_user):
    fake_dset = Dataset(name='fake_dataset')
    fake_dset.save()

    for userid in range(num_users):
        myuser = create_user(userid)
        for exp in range(num_exp_per_user):
            add_experiment(myuser, fake_dset)


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

    # Print out what we have added.
    print("This has been added to the database:")
    for u in User.objects.all():
        for e in Experiment.objects.filter(user=u):
            print "Experiment {0} done by user: {1}".format(e, u)
