from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.forms import model_to_dict
from tastypie import fields
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.http import HttpForbidden, HttpUnauthorized, HttpBadRequest
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation


from activities.models import Activity, PersonActivity

class ActivityResource(ModelResource):
    class Meta:
        queryset = Activity.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'act'
        collection_name = 'acts'
        excludes = ['id']
        always_return_data = True



class PersonActivityResource(ModelResource):
    activity = fields.ToOneField('api.activity.ActivityResource', 'activity', null=True, blank=True, full=True)

    class Meta:
        queryset = PersonActivity.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'activity'
        collection_name = 'activities'
        excludes = ['id']
        always_return_data = True

        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(person__user=bundle.request.user)
    