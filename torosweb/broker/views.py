from django.shortcuts import render, redirect
from .models import Assignment, Observatory, Alert, GWGCCatalog
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db.models import Q


def index(request):
    if not request.user.is_authenticated():
        return user_login(request)

    if not request.user.groups.filter(name='Telescope_operators').exists():
        request.message = \
            "You must be an approved telescope operator to log in."
        return user_login(request)

    context = {}
    current_alert = Alert.objects.order_by('-datetime').first()
    context['alert'] = current_alert
    context['all_assingments'] = Assignment.objects\
        .filter(alert=current_alert)\
        .filter(is_taken=True)\
        .order_by('target__name')

    selected_targets = Assignment.objects.filter(alert=current_alert)\
        .filter(is_taken=True).count()
    context['selected_targets'] = selected_targets

    observed_targets = Assignment.objects.filter(alert=current_alert)\
        .filter(was_observed=True).count()
    context['observed_targets'] = observed_targets

    assn_per_obs = []
    for obs in Observatory.objects.all():
        assn_per_obs.append([obs,
                            Assignment.objects.
                            filter(alert=current_alert).
                            filter(observatory=obs)])
    context['assn_per_obs'] = assn_per_obs
    context['is_admin'] = request.user.groups\
        .filter(name='broker_admins').exists()

    return render(request, 'broker/index.html', context)


def update(request):
    if request.method == "GET":
        return redirect("broker:index")

    current_alert = Alert.objects.order_by('-datetime').first()
    obs_id = int(request.POST['obs_id'])
    obs = Observatory.objects.get(pk=obs_id)

    obs_asg = Assignment.objects.filter(alert=current_alert)\
        .filter(observatory=obs)

    aretakenlist = [int(k) for k in request.POST.getlist('istaken[]')]
    areobservedlist = [int(k) for k in request.POST.getlist('wasobserved[]')]

    print(aretakenlist)

    def taken_by_others(asg):
        other_assng = Assignment.objects.filter(alert=current_alert)\
            .exclude(observatory=asg.observatory)\
            .filter(is_taken=True)\
            .filter(target=asg.target)
        return other_assng.exists()

    def turn_on_taken(asg):
        if asg.is_taken is False:
            asg.is_taken = True

    def turn_off_taken(asg):
        if asg.is_taken is True:
            asg.is_taken = False

    for asg in obs_asg:
        if asg.id in aretakenlist:
            if not taken_by_others(asg) \
                    or asg.id in areobservedlist:
                turn_on_taken(asg)
            else:
                turn_off_taken(asg)
                # Change mode to taken
        else:
            turn_off_taken(asg)
        if asg.id in areobservedlist:
            if asg.was_observed is False:
                asg.was_observed = True
        else:
            if asg.was_observed is True:
                asg.was_observed = False
        asg.save()

    return redirect("broker:index")


def upload(request):
    from django.utils import timezone

    if not request.user.is_authenticated():
        return user_login(request)

    if not request.user.groups.filter(name='broker_admins').exists():
        request.message = \
            "You must be an approved broker admin to upload targets."
        return user_login(request)

    context = {}
    context['alerts'] = Alert.objects.all()

    if request.method == 'POST':
        assgn_text = request.POST.get('assignments', '')
        alert_id = request.POST.get('alert', None)
        thealert = Alert.objects.get(pk=alert_id)

        was_error = False
        error_msg = []
        obss = filter(None, assgn_text.split(';'))
        for anobs_text in obss:
            split = anobs_text.split(':')
            try:
                obs, obj_text = split
            except:
                was_error = True
                error_msg.append("Error parsing line: {}".format(anobs_text))
                continue
            obs = obs.strip()
            name_lookup = Q(name__contains=obs) | Q(short_name__contains=obs)
            try:
                theobs = Observatory.objects.get(name_lookup)
            except:
                was_error = True
                error_msg.append("Could not find observatory {}".format(obs))
                continue
            objs = [obj.strip() for obj in filter(None, obj_text.split(','))]
            for obj_prob in objs:
                try:
                    obj_prob_split = filter(None, obj_prob.split())
                    if len(obj_prob_split) == 1:
                        obj = obj_prob_split[0]
                        prob = 0.0
                    else:
                        obj, prob = obj_prob_split
                        prob = float(prob)
                except:
                    was_error = True
                    error_msg.append("Could not parse '{}'".format(obj_prob))
                    continue
                try:
                    theobj = GWGCCatalog.objects.get(name=obj)
                except:
                    was_error = True
                    error_msg.append("Could not find object {}".format(obj))
                    continue
                new_assgn = Assignment(
                    target=theobj, observatory=theobs,
                    alert=thealert, datetime=timezone.now(), probability=prob)
                new_assgn.save()
        if was_error:
            context['errors'] = error_msg

    return render(request, 'broker/upload.html', context)


def circular(request):
    if not request.user.is_authenticated():
        return user_login(request)

    if not request.user.groups.filter(name='broker_admins').exists():
        request.message = \
            "You must be an approved telescope operator to see this page."
        return user_login(request)

    context = {}
    current_alert = Alert.objects.order_by('-datetime').first()
    context['alert'] = current_alert

    observed_per_obs = []
    for obs in Observatory.objects.all():
        observed_per_obs.append([obs,
                                 Assignment.objects.
                                 filter(alert=current_alert).
                                 filter(observatory=obs).
                                 filter(was_observed=True)])
    context['observed_per_obs'] = observed_per_obs
    return render(request, 'broker/circular.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('broker:index')
            else:
                return HttpResponse("<h1>Your account is disabled.</h1>")
        else:
            return HttpResponse("<h1>Invalid login details supplied.</h1>")

    else:
        context = {}
        try:
            context['message'] = request.message
        except AttributeError:
            context['message'] = None
        return render(request, 'broker/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('broker:login')
