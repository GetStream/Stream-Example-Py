from core import forms
from core.models import Item
from core.models import Pin
from django.contrib.auth import authenticate, get_user_model, \
    login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django_stream.feed_managers import feed_manager
import json


def trending(request):
    '''
    The most popular items
    '''
    if not request.user.is_authenticated():
        # hack to log you in automatically for the demo app
        admin_user = authenticate(username='admin', password='admin')
        auth_login(request, admin_user)

    # show a few items
    context = RequestContext(request)
    popular = Item.objects.all()[:50]
    context['popular'] = popular
    response = render_to_response('core/trending.html', context)
    return response


@login_required
def feed(request):
    '''
    Items pinned by the people you follow
    '''
    context = RequestContext(request)
    feed = feed_manager.get_feeds(request.user.id)['flat']
    if request.REQUEST.get('delete'):
        feed.delete()
    activities = feed.get(limit=25)['results']
    context['feed_pins'] = enrich_activities(activities)
    response = render_to_response('core/feed.html', context)
    return response


@login_required
def aggregated_feed(request):
    '''
    Items pinned by the people you follow
    '''
    context = RequestContext(request)
    feed = feed_manager.get_feeds(request.user.id)['aggregated']
    if request.REQUEST.get('delete'):
        feed.delete()
    activities = feed.get(limit=25)['results']
    context['feed_pins'] = enrich_aggregated_activities(activities)
    response = render_to_response('core/aggregated_feed.html', context)
    return response


def profile(request, username):
    '''
    Shows the users profile
    '''
    profile_user = get_user_model().objects.get(username=username)
    feed = feed_manager.get_user_feed(profile_user.id)
    if request.REQUEST.get('delete'):
        feed.delete()
    activities = feed.get(limit=25)['results']
    context = RequestContext(request)
    context['profile_user'] = profile_user
    context['profile_pins'] = enrich_activities(activities)
    response = render_to_response('core/profile.html', context)
    return response


@login_required
def pin(request):
    '''
    Simple view to handle (re) pinning an item
    '''
    output = {}
    if request.method == "POST":
        data = request.POST.copy()
        data['user'] = request.user.id
        form = forms.PinForm(data=data)

        if form.is_valid():
            pin = form.save()
            if pin:
                output['pin'] = dict(id=pin.id)
            if not request.GET.get('ajax'):
                return redirect_to_next(request)
        else:
            output['errors'] = dict(form.errors.items())

    else:
        form = forms.PinForm()

    return render_output(output)


def redirect_to_next(request):
    return HttpResponseRedirect(request.REQUEST.get('next', '/'))


def render_output(output):
    ajax_response = HttpResponse(
        json.dumps(output), content_type='application/json')
    return ajax_response


@login_required
def follow(request):
    '''
    A view to follow other users
    '''
    output = {}
    if request.method == "POST":
        data = request.POST.copy()
        data['user'] = request.user.id
        form = forms.FollowForm(data=data)

        if form.is_valid():
            follow = form.save()
            if follow:
                output['follow'] = dict(id=follow.id)
        else:
            output['errors'] = dict(form.errors.items())
    else:
        form = forms.FollowForm()
    return HttpResponse(json.dumps(output), content_type='application/json')


def enrich_activities(activities):
    '''
    Load the models attached to these activities
    (Normally this would hit a caching layer like memcached or redis)
    '''
    pin_ids = [a['object'] for a in activities]
    pin_dict = Pin.objects.in_bulk(pin_ids)
    for a in activities:
        a['pin'] = pin_dict.get(int(a['object']))
    return activities


def enrich_aggregated_activities(aggregated_activities):
    '''
    Load the models attached to these aggregated activities
    (Normally this would hit a caching layer like memcached or redis)
    '''
    pin_ids = []
    for aggregated_activity in aggregated_activities:
        for activity in aggregated_activity['activities']:
            pin_ids.append(activity['object'])

    pin_dict = Pin.objects.in_bulk(pin_ids)
    for aggregated_activity in aggregated_activities:
        for activity in aggregated_activity['activities']:
            activity['pin'] = pin_dict.get(int(activity['object']))
    return aggregated_activities
