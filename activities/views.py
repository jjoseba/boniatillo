# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

# Create your views here.
import helpers
from activities.forms.PersonActivityForm import PersonActivityForm
from activities.models import Activity, PersonActivity
from currency.models import Person
from helpers import superuser_required


@superuser_required
def activity_list(request):

    activities = Activity.objects.all()

    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = helpers.get_query(query_string, ['name', 'description', 'type_activity'])
        if entry_query:
            activities = activities.filter(entry_query)

    page = request.GET.get('page')
    activities = helpers.paginate(activities, page, elems_perpage=15)

    params = {
        'ajax_url': reverse('activity_list'),
        'query_string': query_string,
        'activities': activities,
        'page': page
    }

    if request.is_ajax():
        response = render(request, 'activity/search_results.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'activity/list.html', params)

@superuser_required
def activity_detail(request):

    params = {
        'ajax_url': reverse('activity_detail'),
        'act': request.GET.get('act', None),
        'person': request.GET.get('person', None),
    }

    activities = PersonActivity.objects.all()
    if ('act' in request.GET) and request.GET['act'].strip():
        act = request.GET['act']
        activities = activities.filter(activity=act)
        params['activity'] = Activity.objects.filter(pk=act).first()

    if ('person' in request.GET) and request.GET['person'].strip():
        person = request.GET['person']
        activities = activities.filter(person=person)
        params['person'] = Person.objects.filter(pk=person).first()

    page = request.GET.get('page')
    activities = helpers.paginate(activities, page, elems_perpage=10)

    params['activities'] = activities
    params['page'] = page

    if request.is_ajax():
        response = render(request, 'activity/activity_query.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'activity/detail_list.html', params)



@superuser_required
def add_activity(request):

    params = {}
    initial = {}

    activity_id = request.GET.get('activity', None)
    if activity_id:
        activity = Activity.objects.filter(pk=activity_id).first()
        if activity:
            params['activity'] = activity
            initial['activity'] = activity

    profile_id = request.GET.get('person', None)
    if profile_id:
        person = Person.objects.filter(pk=profile_id).first()
        if person:
            params['person'] = person
            initial['person'] = person

    if request.method == "POST":
        form = PersonActivityForm(request.POST, request.FILES)
        if form.is_valid():
            act = form.save(commit=False)

            act.save()
            form.save_m2m()
            if profile_id:
                return redirect(reverse('activity_detail')+'?person='+str(act.person.pk))
            elif activity_id:
                return redirect(reverse('activity_detail')+'?act='+str(act.activity.pk))
            else:
                return redirect('activity_detail')
        else:
            print form.errors.as_data()
    else:
        form = PersonActivityForm(initial=initial)

    params['form'] = form
    return render(request, 'activity/add.html', params)