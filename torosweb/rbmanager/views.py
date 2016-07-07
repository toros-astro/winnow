from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Experiment
from .forms import ExperimentForm


def index(request):
    if request.method == "POST":
        exp_form = ExperimentForm(request.POST)
        if exp_form.is_valid():
            # Process form
            new_exp = exp_form.instance
            new_exp.user = User.objects.get(pk=1)
            new_exp.save()
            notification = {'value': True, 'type': 'success',
                            'message': 'The experiment has been saved'}
            exp_form = ExperimentForm()
        else:
            notification = {'value': True, 'type': 'danger',
                            'message': 'The experiment could not be saved'}

    if request.method == "GET":
        exp_form = ExperimentForm()
        notification = {'value': False, 'type': '', 'message': ''}

    return render(request, 'rbmanager/index.html',
                  {'exp_form': exp_form,
                   'experiment_list': Experiment.objects.all(),
                   'notification': notification})
