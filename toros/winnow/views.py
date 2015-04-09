from django.shortcuts import render
from django.http import HttpResponse
from winnow.forms import RankingForm
from django.contrib.auth.decorators import login_required
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt

import numpy as np

def index(request):
    return render(request, 'winnow/index.html', {'page_index': 'selected'})

def rank(request):
    if request.method == "POST":
        form = RankingForm(request.POST)
        
        if form.is_valid():
            if request.user.is_authenticated():
                r = form.save(commit=False)
                r.ranker = request.user
                r.save()
            return index(request)
        else:
            print form.errors
    else:
        form = RankingForm()
    return render(request, 'winnow/rank.html', {'form': form, 'page_rank': 'selected'})

def about(request):
    return render(request, 'winnow/about.html', {'page_about': 'selected'})
    
def generateTransientThumbnail(request):
    thumb_arr = np.random.random((10,10))
    fig = plt.figure(figsize=(5,5))
    plt.imshow(thumb_arr, interpolation='none')

    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.close()
    return response
