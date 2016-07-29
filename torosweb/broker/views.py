from django.shortcuts import render, redirect
from .models import Assignment, Observatory, Alert


def index(request):
    context = {}
    current_alert, created = Alert.objects.get_or_create(pk=1)
    context['all_assingments'] = Assignment.objects.filter(alert=current_alert)

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

    return render(request, 'broker/index.html', context)


def update(request):
    if request.method == "GET":
        return redirect("broker:index")

    current_alert, created = Alert.objects.get_or_create(pk=1)
    obs_id = int(request.POST['obs_id'])
    obs = Observatory.objects.get(pk=obs_id)

    obs_asg = Assignment.objects.filter(alert=current_alert)\
        .filter(observatory=obs)

    aretakenlist = [int(k) for k in request.POST.getlist('istaken[]')]
    areobservedlist = [int(k) for k in request.POST.getlist('wasobserved[]')]

    for asg in obs_asg:
        if asg.id in aretakenlist:
            if asg.is_taken is False:
                asg.is_taken = True
        else:
            if asg.is_taken is True:
                asg.is_taken = False
        if asg.id in areobservedlist:
            if asg.was_observed is False:
                asg.was_observed = True
        else:
            if asg.was_observed is True:
                asg.was_observed = False
        asg.save()

    return redirect("broker:index")
