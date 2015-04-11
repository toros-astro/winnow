from django.shortcuts import render
from django.http import HttpResponse
from winnow.forms import RankingForm
from django.contrib.auth.decorators import login_required
from winnow.models import TransientCandidate, Ranking, UserProfile

def index(request):
    return render(request, 'winnow/index.html', {'page_index': 'selected'})

def rank(request):
    if request.method == "POST":
        form = RankingForm(request.POST)
        
        if form.is_valid():
            if request.user.is_authenticated():
                r = form.save(commit=False)
                r.ranker = UserProfile.objects.get(user=request.user)
                tc_id = int(request.POST.get('tc_id'))
                r.trans_candidate = TransientCandidate.objects.get(pk=tc_id)
                r.save()
            return index(request)
        else:
            print form.errors
            tc_id = int(request.POST.get('tc_id'))
    else:
        
        
        try:
            #Fetch any tc not ranked yet
            tc = TransientCandidate.objects.exclude(ranking=Ranking.objects.all())[0]
        except IndexError:
            #Fetch any tc not ranked by the current user
            try:
                currentUser = UserProfile.objects.get(user=request.user)
                tc = TransientCandidate.objects.exclude(ranking=Ranking.objects.filter(ranker=currentUser))[0]
            except IndexError:
                tc = None
        
        if tc is None:
            tc_id = -1
        else:
            tc_id = tc.id
        
        form = RankingForm()
        
    return render(request, 'winnow/rank.html', {'form': form, 'page_rank': 'selected', 'tc_id' : tc_id})
    

def about(request):
    return render(request, 'winnow/about.html', {'page_about': 'selected'})
    
def thumb(request, trans_candidate_id):
    
    tc = TransientCandidate.objects.get(pk=trans_candidate_id)
    
    from astropy.io import fits
    from toros.settings import ASTRO_IMAGE_DIR
    from os import path
    image_data = fits.getdata(path.join(ASTRO_IMAGE_DIR, tc.filename))
    thumb_arr = image_data[tc.y_pix - tc.height: tc.y_pix + tc.height, tc.x_pix - tc.width: tc.x_pix + tc.width]

    #import numpy as np
    #thumb_arr = np.random.random((10,10))
    
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(5,5))
    plt.imshow(thumb_arr, interpolation='none')
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.close()
    return response
