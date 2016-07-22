import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torosweb.settings')
import django
django.setup()

from winnow.models import Dataset

for ads in Dataset.objects.all():
    print(ads.name.upper())
    print("-" * len(ads.name))
    if ads.isCurrent:
        print("Note: {} is currently being classified.".format(ads.name))
    if ads.start_datetime:
        print("Start Date: {}".format(ads.start_datetime.date()))
    else:
        print("Start Date: unknown")
    if ads.end_datetime:
        print("End Date:   {}".format(ads.end_datetime.date()))
    else:
        print("End Date:   unknown")
    if ads.cadence_sec:
        print("Cadence:    {} s".format(ads.cadence_sec))
    else:
        print("Cadence:    unknown")
    if ads.subset_of:
        print("{} is a subset of {}".format(ads.name, ads.subset_of))
    if ads.number_of_files:
        print("Number of files: {}".format(ads.number_of_files))
    else:
        print("Number of files: unknown")
    if ads.description:
        print(ads.description)

    print("Dataset object statistics:")
    print("--------------------------")
    print("\tTotal number of objects: {}".format(ads.number_of_objects()))
    print("\tNumber of classified reals: {}".format(ads.number_of_reals()))
    print("\tNumber of classified bogus: {}".format(ads.number_of_bogus()))
    print("\tNumber of unclassified: {}".format(ads.number_of_unclassified()))
    print("\tNumber of not ranked: {}".format(ads.number_not_ranked()))
    print("\n")
