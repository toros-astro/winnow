import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

# from django.contrib.auth.models import User
from broker.models import GWGCCatalog, Observatory, Alert, Assignment

from django.utils import timezone

# def create_user(last_user_id):
#     auser, created = User.objects.get_or_create(
#         username="populate%02d" % (last_user_id + 1))
#     if created:
#         auser.first_name = "Populate"
#         auser.last_name = "Anon%02d" % (last_user_id + 1)
#         auser.save()
#     myuser, created = UserProfile.objects.get_or_create(user=auser)
#     if created:
#         myuser.save()
#     return myuser


def populate():
    import random
    the_alert = Alert(datetime=timezone.now())
    the_alert.ligo_run = "O2"
    the_alert.alert_number = 1
    the_alert.save()
    print("Created Alert %s" % the_alert)

    all_observatories = create_observatories()
    all_objects = create_obects()

    for anobs in all_observatories:
        random.shuffle(all_objects)
        rand_objs = all_objects[:5]
        for obj in rand_objs:
            is_taken = random.random() > 0.5
            was_observed = random.random() > 0.5 if is_taken else False
            new_asg = Assignment(
                target=obj, observatory=anobs, alert=the_alert,
                datetime=timezone.now(), is_taken=is_taken,
                was_observed=was_observed)
            new_asg.save()
            print("Created Assignment for observatory %s and object %s"
                  % (anobs, obj))


def create_observatories():
    all_obs = []

    new_obs = Observatory(name="Mamalluca Observatory", country="Chile",
                          city="La Serena", short_name="Mamalluca")
    new_obs.longitude = -33.000
    new_obs.latitude = -71.516667
    new_obs.elevation = 709
    new_obs.save()
    all_obs.append(new_obs)

    new_obs = Observatory(name="Estacion Astrofisica de Bosque Alegre",
                          country="Argentina", city="Cordoba",
                          short_name="EABA")
    new_obs.longitude = -31.596339
    new_obs.latitude = -64.543219
    new_obs.elevation = 1350
    new_obs.save()
    all_obs.append(new_obs)

    new_obs = Observatory(name="Guillermo Haro Observatory",
                          country="Mexico", city="La Sonora",
                          short_name="G. Haro")
    new_obs.longitude = 31.052778
    new_obs.latitude = -110.384722
    new_obs.elevation = 2480
    new_obs.save()
    all_obs.append(new_obs)

    return all_obs


def create_obects():
    csv = ("""2 UGC12889 0.00047 47.27450 3.1 13.31 1.546 0.498 1.314 NaN 0.85 0.100 NaN -21.05 72.458 10.869 0.61 0.61 
4 PGC000004 0.00096 23.08764 5.0 15.39 0.851 0.078 0.186 NaN 0.219 0.015 NaN -18.68 63.264 13.918 0.39 0.40 
6 PGC000006 0.00058 15.88165 -1.0 15.23 0.457 0.169 0.324 NaN 0.708 0.082 NaN -19.46 84.181 18.520 0.34 0.35 
7 PGC000007 0.00122 -0.08326 -3.2 15.54 0.575 0.093 0.467 NaN 0.813 0.056 NaN -19.46 97.347 21.416 0.33 0.34 
10 PGC000010 0.00217 -0.04057 -3.2 15.56 0.562 0.078 0.446 NaN 0.794 0.037 NaN -19.46 98.250 21.615 0.29 0.31 
12 PGC000012 0.00240 -6.37390 1.1 14.05 1.045 0.336 0.199 NaN 0.19 0.022 NaN -20.79 92.153 13.823 0.36 0.37 
13 PGC000013 0.00370 33.13420 NaN 15.41 0.675 0.217 0.587 NaN 0.87 0.102 NaN -18.94 72.722 10.908 0.40 0.41 
16 PGC000016 0.00314 -5.15871 1.2 14.60 0.630 0.203 0.328 NaN 0.52 0.061 NaN -19.93 79.278 11.892 0.29 0.30 
18 PGC000018 0.00360 46.96508 NaN 14.25 0.869 0.280 0.791 NaN 0.91 0.107 NaN -20.25 77.306 11.596 0.31 0.32 
31 PGC000031 0.00657 -47.01893 0 14.67 0.740 0.238 0.466 NaN 0.63 0.074 NaN -19.91 85.389 12.808 0.34 0.35 
38 UGC12893 0.00792 17.22027 8.4 15.14 1.148 0.159 1.023 NaN 0.891 0.062 NaN -15.97 16.222 3.569 0.38 0.39 
43 ESO293-027 0.00819 -40.48439 3.9 13.27 1.443 0.465 0.375 NaN 0.26 0.031 NaN -19.87 43.069 6.460 0.28 0.29 
49 PGC000049 0.00931 22.77842 NaN 16.85 0.316 0.102 0.288 NaN 0.91 0.107 NaN -17.87 85.389 18.786 1.01 1.01 
53 UGC12895 0.01064 20.05896 7.6 16.46 0.617 0.099 0.457 NaN 0.741 0.051 NaN -18.48 94.819 20.860 0.49 0.50 
55 UGC12898 0.01039 33.60095 5.9 15.90 0.776 0.072 0.234 NaN 0.302 0.021 NaN -18.33 68.333 15.033 0.35 0.36 
65 ESO193-009 0.01479 -47.35683 -0.9 15.03 0.850 0.274 0.221 NaN 0.26 0.031 NaN -19.51 81.236 12.185 0.21 0.22 
70 UGC12900 0.01557 20.33792 5.8 13.82 1.778 0.123 0.258 NaN 0.145 0.010 NaN -21.14 95.583 21.028 0.29 0.31 
73 ESO349-017 0.01627 -33.61189 5.1 14.36 0.707 0.228 0.601 NaN 0.85 0.100 NaN -20.56 95.722 14.358 0.28 0.29 
76 UGC12901 0.01636 28.91169 3.0 13.99 1.094 0.352 0.416 NaN 0.38 0.045 NaN -21.01 98.278 14.742 0.33 0.34 
81 NGC7802 0.01677 6.24195 -2.0 14.35 0.811 0.261 0.406 NaN 0.50 0.059 NaN -20.06 74.750 11.213 0.32 0.33 
89 PGC000089 0.02039 13.14406 4.9 14.84 0.741 0.085 0.295 NaN 0.398 0.028 NaN -19.64 76.486 16.827 0.07 0.12 
92 PGC000092 0.02084 13.11290 5.5 15.66 0.513 0.083 0.186 NaN 0.363 0.025 NaN -18.87 78.278 17.221 0.19 0.21 
94 UGC12905 0.03358 80.64171 6.1 NaN 1.072 0.148 0.129 NaN 0.120 0.017 NaN NaN 60.833 13.383 NaN NaN 
101 NGC7803 0.02221 13.11128 0.0 13.56 0.500 0.161 0.295 NaN 0.59 0.069 NaN -20.88 76.528 11.479 0.11 0.13 
102 IC5376 0.02216 34.52572 2.0 13.78 1.443 0.465 0.245 NaN 0.17 0.020 NaN -20.57 72.472 10.871 0.32 0.33 
108 PGC000108 0.02386 13.11310 9.0 14.64 0.281 0.091 0.239 NaN 0.85 0.100 NaN -19.75 75.000 11.250 0.10 0.12 
109 NGC7805 0.02410 31.43378 -1.9 13.90 0.870 0.280 0.722 NaN 0.83 0.098 NaN -20.40 71.236 10.685 0.10 0.12 
110 UGC12910 0.02450 5.38890 9.0 NaN 0.912 0.210 0.912 NaN 1.000 0.138 NaN NaN 54.931 12.085 NaN NaN 
112 NGC7806 0.02503 31.44192 4.1 13.63 0.850 0.274 0.663 NaN 0.78 0.092 NaN -20.60 68.722 10.308 0.16 0.17 
113 PGC000113 0.02577 -33.75882 -1.0 16.03 0.525 0.073 0.372 NaN 0.708 0.033 NaN -18.89 93.472 20.564 0.30 0.31 
118 PGC000118 0.02610 15.08161 4.2 15.27 0.708 0.114 0.309 NaN 0.437 0.030 NaN -19.54 88.958 19.571 0.66 0.67 
120 UGC12914 0.02731 23.48359 5.6 12.57 1.546 0.498 0.866 NaN 0.56 0.066 NaN -21.46 63.028 9.454 0.38 0.39 
122 PGC000122 0.02531 -40.81977 NaN 14.95 0.891 0.082 0.589 NaN 0.661 0.030 NaN -19.97 93.736 20.622 0.33 0.34 
124 UGC12913 0.02684 3.50559 5.7 15.37 1.148 0.079 0.166 NaN 0.145 0.010 NaN -19.42 88.028 19.366 0.45 0.46 
129 UGC12915 0.02831 23.49582 5.3 12.74 1.021 0.329 0.337 NaN 0.33 0.039 NaN -21.27 62.542 9.381 0.28 0.29 
134 PGC000134 0.02923 13.10021 NaN 15.72 0.398 0.073 0.339 NaN 0.851 0.078 NaN -18.81 78.333 17.233 0.46 0.47 
143 PGC000143 0.03292 -15.46140 9.9 10.83 11.500 3.703 4.025 NaN 0.35 0.041 NaN -14.06 0.951 0.095 0.30 0.30 
146 UGC12916 0.03422 17.57394 7.6 NaN 0.813 0.225 0.563 NaN 0.692 0.112 NaN NaN 89.111 19.604 NaN NaN 
147 PGC000147 0.03274 21.62117 NaN 15.56 0.547 0.176 NaN NaN NaN NaN NaN -19.37 95.375 14.306 0.48 0.48 
156 IC5377 0.03483 16.59032 9.9 14.96 0.912 0.231 0.537 NaN 0.589 0.068 NaN -16.05 15.444 3.398 0.39 0.40 
163 NGC7810 0.03866 12.97156 -2.0 13.81 0.793 0.255 0.547 NaN 0.69 0.081 NaN -20.68 78.819 11.823 0.26 0.27 
171 UGC12921 0.03918 77.25686 2 13.90 0.774 0.249 0.588 NaN 0.76 0.089 NaN -19.05 38.500 5.775 0.29 0.30 
176 PGC000176 0.04301 -3.71081 4.1 13.93 0.890 0.286 0.561 NaN 0.63 0.074 NaN -20.89 91.153 13.673 0.28 0.29 
177 PGC000177 0.04387 16.64381 NaN 14.94 0.397 0.128 0.397 NaN 1.00 0.117 NaN -19.87 90.819 13.623 0.40 0.41 
178 PGC000178 0.04383 16.65170 5.7 16.56 0.603 0.097 0.525 NaN 0.871 0.060 NaN -18.07 81.889 18.016 0.49 0.50 
179 PGC000179 0.04443 8.73695 3.0 14.59 0.574 0.185 0.109 NaN 0.19 0.022 NaN -19.91 78.750 11.812 0.32 0.33 
181 ESO012-014 0.04511 -80.34825 9.0 13.37 1.657 0.534 0.845 NaN 0.51 0.060 NaN -18.33 21.878 3.282 0.30 0.31 
183 PGC000183 0.04404 -3.63106 NaN 15.83 0.813 0.112 0.257 NaN 0.316 0.022 NaN -18.92 86.569 19.045 0.29 0.31 
185 IC5379 0.04463 16.60028 5.4 15.41 0.550 0.076 0.251 NaN 0.457 0.032 NaN -19.37 88.069 19.375 0.65 0.66""")

    cat_keys = ["ra", "dec", "obj_type", "app_mag",
                "maj_diam_a", "err_maj_diam", "min_diam_b", "err_min_diam",
                "b_over_a", "err_b_over_a", "pa", "abs_mag", "dist",
                "err_dist", "err_app_mag", "err_abs_mag"]

    all_objs = []
    for aline in csv.split('\n'):
        cols = aline.split()
        obj_data = {akey: float(aval)
                    for akey, aval in zip(cat_keys, cols[2:])}
        obj_data["pgc"] = int(cols[0])
        obj_data["name"] = cols[1]
        new_obj = GWGCCatalog(**obj_data)
        new_obj.save()
        all_objs.append(new_obj)

    return all_objs


if __name__ == '__main__':
    print("Starting rbmamager population script...")
    populate()
