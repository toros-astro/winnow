from django.shortcuts import render, redirect
from .models import Assignment, Observatory, Alert, GWGCCatalog
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def index(request, the_alert=None):
    if not request.user.is_authenticated():
        return user_login(request)

    if not request.user.groups.filter(name='Telescope_operators').exists():
        request.message = \
            "You must be an approved telescope operator to log in."
        return user_login(request)

    if request.method == 'POST':
        the_alert = Alert.objects.filter(pk=request.POST['alert_id']).get()
        obs_id = int(request.POST['obs_id'])
        obs = Observatory.objects.get(pk=obs_id)

        obs_asg = Assignment.objects.filter(alert=the_alert)\
            .filter(observatory=obs)

        aretakenlist = [int(k) for k in request.POST.getlist('istaken[]')]
        areobservedlist = [int(k)
                           for k in request.POST.getlist('wasobserved[]')]

        print(aretakenlist)

        def taken_by_others(asg):
            other_assng = Assignment.objects.filter(alert=the_alert)\
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

    context = {}
    context['alerts'] = Alert.objects.order_by('-datetime')

    if the_alert is None:
        the_alert = Alert.objects.order_by('-datetime').first()
    context['the_alert'] = the_alert

    context['all_assingments'] = Assignment.objects\
        .filter(alert=the_alert)\
        .filter(is_taken=True)\
        .order_by('target__name')

    selected_targets = Assignment.objects.filter(alert=the_alert)\
        .filter(is_taken=True).count()
    context['selected_targets'] = selected_targets

    observed_targets = Assignment.objects.filter(alert=the_alert)\
        .filter(was_observed=True).count()
    context['observed_targets'] = observed_targets

    def taken_by_others(asg):
        other_assng = Assignment.objects.filter(alert=the_alert)\
            .exclude(observatory=asg.observatory)\
            .filter(is_taken=True)\
            .filter(target=asg.target)
        return other_assng.exists()

    assn_per_obs = []
    for obs in Observatory.objects.all():
        assgnms = Assignment.objects.filter(alert=the_alert)\
                                    .filter(observatory=obs)
        for asg in assgnms:
            if (not asg.is_taken) and taken_by_others(asg):
                asg.flag_unavailable = True
            else:
                asg.flag_unavailable = False
        assn_per_obs.append([obs, assgnms])
    context['assn_per_obs'] = assn_per_obs
    context['is_admin'] = request.user.groups\
        .filter(name='broker_admins').exists()

    return render(request, 'broker/index.html', context)


def alert_detail(request, alert_name):
    the_alert = Alert.objects.filter(grace_id=alert_name).first()
    return index(request, the_alert)


def upload(request):
    from django.utils import timezone

    if not request.user.is_authenticated():
        return user_login(request)

    if not request.user.groups.filter(name='broker_admins').exists():
        request.message = \
            "You must be an approved broker admin to upload targets."
        return user_login(request)

    context = {}
    context['alerts'] = Alert.objects.order_by('-datetime')

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


@require_POST
@csrf_exempt
def uploadjson(request):
    import json
    import datetime as d
    import pytz
    from django.utils import timezone
    try:
        # Parse alert
        alert = json.loads(request.POST["targets.json"])
        dt = d.datetime.strptime(alert["datetime"], "%Y-%m-%dT%H:%M:%S.%f")
        dt = pytz.utc.localize(dt)
        thealert = Alert(grace_id=alert["graceid"], datetime=dt)
        thealert.save()
        for obs_name, obs_assgn in alert["assignments"].iteritems():
            name_lookup = (Q(name__contains=obs_name) |
                           Q(short_name__contains=obs_name))
            try:
                theobs = Observatory.objects.get(name_lookup)
            except:
                continue
            for obj, prob in obs_assgn.iteritems():
                try:
                    theobj = GWGCCatalog.objects.get(name=obj)
                except:
                    continue
                new_assgn = Assignment(
                    target=theobj, observatory=theobs,
                    alert=thealert, datetime=timezone.now(), probability=prob)
                new_assgn.save()
    except:
        return HttpResponseBadRequest()

    return HttpResponse()


def circular(request, alert_name=None):
    if not request.user.is_authenticated():
        return user_login(request)

    if not request.user.groups.filter(name='broker_admins').exists():
        request.message = \
            "You must be an approved telescope operator to see this page."
        return user_login(request)

    context = {}

    the_alert = Alert.objects.filter(grace_id=alert_name).first()
    if the_alert is None:
        the_alert = Alert.objects.order_by('-datetime').first()
    context['alert'] = the_alert

    observed_per_obs = []
    for obs in Observatory.objects.all():
        observed_per_obs.append([obs,
                                 Assignment.objects.
                                 filter(alert=the_alert).
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
