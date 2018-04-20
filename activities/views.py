# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
import helpers
from activities.models import Activity
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