from django.shortcuts import render, redirect
from django.http import HttpResponse
from winnow.forms import RankingForm, UserForm, UserProfileForm
from winnow.models import TransientCandidate, Ranking, UserProfile, Dataset
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# For the comments
from django_comments.models import Comment
from django.contrib.sites.shortcuts import get_current_site


def index(request):
    return render(request, 'winnow/index.html', {'page_index': 'selected'})


def rank(request):
    if not request.user.is_authenticated():
        context = {}
        context['message'] = {
            'headline': "Access denied",
            'body': "You need to be logged in to view this page"}
        return render(request, 'winnow/message.html', context)

    if request.method == "POST":
        form = RankingForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.ranker = UserProfile.objects.get(user=request.user)
            tc_id = int(request.POST.get('tc_id'))
            tc = TransientCandidate.objects.get(pk=tc_id)
            r.trans_candidate = tc
            r.save()

            # Now save the comment if there is one.
            comment_text = request.POST.get('comment')
            if len(comment_text) > 0:
                # save the comment
                new_comment = Comment()
                new_comment.user = request.user
                new_comment.user_name = request.user.username
                new_comment.user_email = request.user.email
                new_comment.user_url = UserProfile.objects.\
                    get(user=request.user).website
                new_comment.comment = comment_text
                new_comment.site = get_current_site(request)
                new_comment.content_object = tc
                new_comment.save()

            return redirect('winnow:rank')
        else:
            tc_id = int(request.POST.get('tc_id'))
            tc = TransientCandidate.objects.get(pk=tc_id)
    else:
        try:
            # Fetch any tc not ranked yet
            ds = Dataset.objects.filter(isCurrent=True).reverse()[0]
            tc = TransientCandidate.objects.filter(dataset=ds).\
                exclude(ranking__in=Ranking.objects.all())[0]
        except IndexError:
            # Fetch any tc not ranked by the current user
            try:
                current_user = UserProfile.objects.get(user=request.user)
                ds = Dataset.objects.filter(isCurrent=True).reverse()[0]
                tc = TransientCandidate.objects.filter(dataset=ds)\
                    .exclude(
                        ranking__in=Ranking.objects.filter(ranker=current_user))[0]
            except IndexError:
                tc = None

        if tc is None:
            tc_id = -1
        else:
            tc_id = tc.id

        form = RankingForm()

    return render(request, 'winnow/rank.html',
                  {'form': form, 'page_rank': 'selected',
                   'tc_id': tc_id, 'object': tc})


def about(request):
    return render(request, 'winnow/about.html', {'page_about': 'selected'})


def object_detail(request, object_slug):
    trans_obj = TransientCandidate.objects.get(slug=object_slug)
    ranked_interesting = Ranking.objects\
        .filter(trans_candidate=trans_obj)\
        .filter(isInteresting=True)
    int_users_list = UserProfile.objects.filter(ranking=ranked_interesting)
    int_counts = len(int_users_list)

    if request.method == "POST":
        if request.user.is_authenticated():
            # Save the comment if there is one.
            comment_text = request.POST.get('comment')
            if len(comment_text) > 0:
                # save the comment
                new_comment = Comment()
                new_comment.user = request.user
                new_comment.user_name = request.user.username
                new_comment.user_email = request.user.email
                new_comment.user_url = \
                    UserProfile.objects.get(user=request.user).website
                new_comment.comment = comment_text
                new_comment.site = get_current_site(request)
                new_comment.content_object = trans_obj
                new_comment.save()

    return render(request, 'winnow/trans_detail.html',
                  {'object': trans_obj, 'interesting_count': str(int_counts),
                   'interesting_user_list': int_users_list})


def register(request):
    registered = False

    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False.
            # This delays saving the model until we're ready
            # to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form
            # and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was
            # successful.
            registered = True

            # Now the user has been created, log them in
            newusername = request.POST.get('username')
            newpassword = request.POST.get('password')
            newuser = authenticate(username=newusername, password=newpassword)
            if newuser:
                if newuser.is_active:
                    login(request, newuser)
                    return redirect('winnow:index')
                else:
                    context = {}
                    context['message'] = {
                        'headline': "Error loggin in",
                        'body': "Sorry, your account has been disabled."}
                    return render(request, 'winnow/message.html', context)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'winnow/register.html',
                  {'user_form': user_form, 'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)

                # This returns users to whatever page they were when logged in
                if request.POST['next']:
                    return redirect(request.POST['next'])
                else:
                    return redirect('winnow:index')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'winnow/login.html', {})


def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('winnow:index')


def show_profile(request, a_username):
    try:
        the_user = User.objects.get(username=a_username)
        the_userprofile = UserProfile.objects.get(user=the_user)
    except:
        the_userprofile = None
    return render(request, 'winnow/profile_detail.html',
                  {'the_userprofile': the_userprofile})


def data(request):
    if not request.user.is_superuser:
        context = {}
        context['message'] = {
            'headline': "Access denied",
            'body': "You need to be a logged in superuser to view this page"}
        return render(request, 'winnow/message.html', context)

    from django.db.models import Sum
    if request.method == 'POST':
        dataset = request.POST['dataset']
        alltc = TransientCandidate.objects.filter(dataset__name=dataset)

        from django.conf import settings
        import os
        from django.utils import timezone
        dumpfilename = os.path.join(settings.MEDIA_ROOT,
                                    'db_dumps/%s_dump.txt' % (dataset))
        dumpfile = open(dumpfilename, 'w')
        dumpfile.write("#" + str(timezone.now()) + "\n")
        dumpfile.write(
            "#unique_id, object id, dataset id, file name, x_pix, y_pix, "
            "RA, Dec, height, width, original magnitude, "
            "reference magnitude, subtraction magnitude, ranking\n")

        for atc in alltc:
            aline = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " % \
                (atc.slug, atc.object_id, dataset, atc.filename, atc.x_pix,
                 atc.y_pix, atc.ra, atc.dec, atc.height, atc.width,
                 atc.mag_orig, atc.mag_ref, atc.mag_subt)

            rbclass = atc.ranking_set.all().\
                aggregate(Sum('rank'))['rank__sum']
            rbclass = rbclass if rbclass is not None else 0
            aline += "%d\n" % (rbclass)
            dumpfile.write(aline)
        dumpfile.close()

        from django.core.servers.basehttp import FileWrapper
        wrapper = FileWrapper(file(dumpfilename))
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Length'] = os.path.getsize(dumpfilename)
        return response

    else:
        datasets = Dataset.objects.all()
        return render(request, 'winnow/data_interface.html',
                      {'page_data': 'selected', 'datasets': datasets})


# Completely deprecated, I leave it here just in case
# def thumb(request, trans_candidate_id):
#
#    tc = TransientCandidate.objects.get(pk=trans_candidate_id)
#
#    from astropy.io import fits
#    from toros.settings import ASTRO_IMAGE_DIR
#    from os import path
#    image_data = fits.getdata(path.join(ASTRO_IMAGE_DIR, tc.filename))
#    thumb_arr = image_data[tc.y_pix - tc.height: tc.y_pix + tc.height,
#                           tc.x_pix - tc.width: tc.x_pix + tc.width]
#
#    #import numpy as np
#    #thumb_arr = np.random.random((10,10))
#
#    import matplotlib
#    matplotlib.use("Agg")
#    import matplotlib.pyplot as plt
#    fig = plt.figure(figsize=(5,5))
#    plt.imshow(thumb_arr, interpolation='none', cmap='gray')
#    plt.xticks([]); plt.yticks([]) #Remove tick marks
#    plt.tight_layout()
#    from matplotlib.backends.backend_agg import FigureCanvasAgg
#    canvas = FigureCanvasAgg(fig)
#    response = HttpResponse(content_type='image/png')
#    canvas.print_png(response)
#    plt.close()
#    return response
