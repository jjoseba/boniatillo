from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.forms import model_to_dict
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.http import HttpForbidden, HttpUnauthorized, HttpBadRequest
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation

from currency.forms.user import UserForm
from currency.models.extend_user import get_user_by_related
from wallets.models import Wallet


class RegisterResource(ModelResource):
    entity = fields.ToOneField('api.entities.EntitiesDetailResource', 'entity', null=True, blank=True, full=True)
    person = fields.ToOneField('api.persons.PersonsResource', 'person', null=True, blank=True, full=True)

    class Meta:
        queryset = User.objects.all()
        include_resource_uri = False
        always_return_data = True
        list_allowed_methods = ['post']
        resource_name = 'register'
        excludes = ['password', 'is_staff', 'is_superuser', 'id']
        validation = FormValidation(form_class=UserForm)

        authentication = Authentication()  # No need for auth, public resource
        authorization = Authorization()

    def hydrate(self, bundle):

        if 'email' in bundle.data and bundle.data.get('email') != '':
            if 'entity' in bundle.data and not ('email' in bundle.data['entity']):
                bundle.data['entity']['email'] = bundle.data['email']
            elif 'person' in bundle.data and not ('email' in bundle.data['person']):
                bundle.data['person']['email'] = bundle.data['email']

        if 'person' in bundle.data:
            if 'name' in bundle.data['person']:
                bundle.data['first_name'] = bundle.data['person']['name']
            if 'surname' in bundle.data['person']:
                bundle.data['lastt_name'] = bundle.data['person']['surname']

        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(RegisterResource, self).obj_create(bundle, request=request, **kwargs)
        user = bundle.obj
        password = bundle.data.get('password')
        pin_code = bundle.data.get('pin_code')

        user.set_password(password)
        user.save()

        u = authenticate(username=user.username, password=password)
        if u is not None and u.is_active:
            if pin_code:
                Wallet.update_user_pin_code(u, pin_code)
            login(bundle.request, u)
        return bundle

    def dehydrate(self, bundle):
        user = bundle.obj
        bundle.data = gen_userwallet_data(user, include_type=False)

        return bundle



def gen_userwallet_data(user, include_type=True, include_apikey=True):

    data = {}

    user_type, instance = user.get_related_entity()
    if include_type:
        data['type'] = user_type
    if include_apikey:
        data['api_key'] = ApiKey.objects.get_or_create(user=user)[0].key

    data['entity'] = model_to_dict(instance) if user_type is 'entity' else None
    data['person'] = model_to_dict(instance) if user_type is 'person' else None



    if (data['entity'] is not None) and 'user' in data['entity']:
        data['entity']['id'] = instance.pk
        if data['entity']['logo']:
            data['entity']['logo'] = data['entity']['logo'].url
            data['entity']['logo_thumbnail'] = instance.logo_thumbnail.url
        del data['entity']['user']
        del data['entity']['gallery']

    if (data['person'] is not None) and 'user' in data['person']:
        data['person']['id'] = instance.pk
        del data['person']['user']

        if data['person']['fav_entities']:
            for i, fav in enumerate(data['person']['fav_entities']):
                data['person']['fav_entities'][i] = fav.pk

    return data


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        list_allowed_methods = ['post']
        detail_allowed_methods = ['get']
        excludes = ['password', 'is_staff', 'is_superuser', 'id']

    def prepend_urls(self):
        return [
            url(r"^login/$", self.wrap_view('login'), name="api_login"),
            url(r"^logout/$", self.wrap_view('logout'), name='api_logout'),
            url(r"^reset_password/$", self.wrap_view('reset_password'), name='api_reset_password'),
        ]


    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                response = { 'success': True }
                response['data'] = gen_userwallet_data(user)
                return self.create_response(request, response)
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if request.user and request.user.is_authenticated:
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)


    def reset_password(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        email = data.get('email', '')
        form = PasswordResetForm({'email': email})
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'email_template_name':'registration/password_reset_email.html',
                'subject_template_name':'registration/password_reset_subject.txt',
                'request': request,
            }
            form.save(**opts)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpBadRequest)


    def obj_get(self, bundle, **kwargs):
        uuid = kwargs['pk']
        return get_user_by_related(uuid)

    def dehydrate(self, bundle):
        user = bundle.obj
        bundle.data = gen_userwallet_data(user, include_apikey=False)

        return bundle