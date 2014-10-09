from core import forms
from core.models import Item
from django.contrib.auth import authenticate, get_user_model, \
    login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from stream_django.feed_manager import feed_manager
from core.enrich import Enrich
from core.enrich import did_i_pin_items
from core.enrich import do_i_follow_users
import json


def trending(request):
    '''
    The most popular items
    '''
    if not request.user.is_authenticated() and not settings.USE_AUTH:
        # hack to log you in automatically for the demo app
        admin_user = authenticate(username='admin', password='admin')
        auth_login(request, admin_user)

    # show a few items
    context = RequestContext(request)
    popular = Item.objects.all()[:50]
    if request.user.is_authenticated():
        did_i_pin_items(request.user, popular)
    context['popular'] = popular
    response = render_to_response('core/trending.html', context)
    return response


@login_required
def feed(request):
    '''
    Items pinned by the people you follow
    '''
    enricher = Enrich(request.user)
    context = RequestContext(request)
    feed = feed_manager.get_feed('flat', request.user.id)
    if request.REQUEST.get('delete'):
        feed.delete()
    activities = feed.get(limit=25)['results']
    context['activities'] = enricher.enrich_activities(activities)
    response = render_to_response('core/feed.html', context)
    return response


@login_required
def aggregated_feed(request):
    '''
    Items pinned by the people you follow
    '''
    enricher = Enrich(request.user)
    context = RequestContext(request)
    feed = feed_manager.get_feed('aggregated', request.user.id)
    if request.REQUEST.get('delete'):
        feed.delete()
    activities = feed.get(limit=25)['results']
    context['activities'] = enricher.enrich_aggregated_activities(activities)
    response = render_to_response('core/aggregated_feed.html', context)
    return response


def profile(request, username):
    '''
    Shows the users profile
    '''
    enricher = Enrich(request.user)
    profile_user = get_user_model().objects.get(username=username)
    feed = feed_manager.get_user_feed(profile_user.id)
    if request.REQUEST.get('delete'):
        feed.delete()
    activities = feed.get(limit=25)['results']
    context = RequestContext(request)
    do_i_follow_users(request.user, [profile_user])
    context['profile_user'] = profile_user
    context['activities'] = enricher.enrich_activities(activities)
    response = render_to_response('core/profile.html', context)
    return response


@login_required
def people(request):
    context = RequestContext(request)
    people = get_user_model().objects.all()[:25]
    do_i_follow_users(request.user, people)
    context['people'] = people
    response = render_to_response('core/people.html', context)
    return response


@login_required
def pin(request):
    '''
    Simple view to handle (re) pinning an item
    '''
    output = {}
    if request.method == "POST":
        form = forms.PinForm(user=request.user, data=request.POST)

        if form.is_valid():
            pin = form.save()
            if pin:
                output['pin'] = dict(id=pin.id)
            if not request.GET.get('ajax'):
                return redirect_to_next(request)
        else:
            output['errors'] = dict(form.errors.items())
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
        form = forms.FollowForm(user=request.user, data=request.POST)

        if form.is_valid():
            follow = form.save()
            if follow:
                output['follow'] = dict(id=follow.id)
            if not request.GET.get('ajax'):
                return redirect_to_next(request)
        else:
            output['errors'] = dict(form.errors.items())
    return HttpResponse(json.dumps(output), content_type='application/json')
