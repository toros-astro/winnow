from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Experiment
from .forms import ExperimentForm

from winnow.models import UserProfile


def index(request):
    if request.method == "POST":
        notification_failed = {'value': True, 'type': 'danger',
                               'message': 'The experiment could not be saved'}
        notification_passed = {'value': True, 'type': 'success',
                               'message': 'The experiment has been saved.'}
        exp_form = ExperimentForm(request.POST)
        if exp_form.is_valid():
            # Process form
            if request.user.is_authenticated():
                new_exp = exp_form.instance
                try:
                    user_prof = request.user.userprofile
                except ObjectDoesNotExist:
                    user_prof = UserProfile(user=request.user)
                    user_prof.save()
                    notification_passed['message'] += \
                        " A new profile has been created for the user."
                new_exp.user = user_prof

                print("DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG ")
                print(exp_form['features'])
                print("DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG ")

                new_exp.save()
                notification = notification_passed
                exp_form = ExperimentForm()
            else:  # if user is not authenticated
                notification_failed['message'] = "You need to be logged in " \
                    "to upload an experiment."
                notification = notification_failed

        else:  # if form is not valid:
            notification = notification_failed

    else:  # if request.method == "GET" or otherwise
        exp_form = ExperimentForm()
        notification = {'value': False, 'type': '', 'message': ''}

    return render(request, 'rbmanager/index.html',
                  {'exp_form': exp_form,
                   'experiment_list': Experiment.objects.all(),
                   'notification': notification})
