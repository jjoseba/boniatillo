from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

import helpers
from currency.forms.EntityForm import EntityForm
from currency.forms.galleryform import PhotoGalleryForm
from currency.models import Entity, Gallery, Category
from helpers import superuser_required
from offers.models import Offer


@login_required
def user_entity(request):
    type, entity = get_user_model().get_related_entity(request.user)
    if type == 'entity':
        return redirect('entity_detail', pk= entity.pk)
    else:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para gestionar una entidad')
        return redirect('dashboard')


def entity_detail(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    if not entity.gallery:
        entity.gallery = Gallery.objects.create()
        entity.save()

    gallery = entity.gallery.photos.all()
    current_offers = Offer.objects.current(entity=entity)
    is_owner = request.user.is_authenticated and (request.user == entity.user)
    can_edit = is_owner or request.user.is_superuser

    return render(request, 'entity/detail.html', {
        'entity': entity,
        'gallery': gallery,
        'offers': current_offers,
        'can_edit_entity': can_edit,
        'is_entity_owner':is_owner
    })


@superuser_required
def entity_list(request):

    entities = Entity.objects.all()

    category_filter = request.GET.get('cat', None)
    if category_filter:
        entities = entities.filter(categories__pk=category_filter)

    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = helpers.get_query(query_string, ['name', 'description', 'short_description'])
        if entry_query:
            entities = entities.filter(entry_query)

    page = request.GET.get('page')
    entities = helpers.paginate(entities, page, elems_perpage=6)

    params = {
        'ajax_url': reverse('entity_list'),
        'query_string': query_string,
        'entities': entities,
        'page': page
    }

    if request.is_ajax():
        response = render(request, 'entity/search_results.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        params['categories'] = Category.objects.all()
        return render(request, 'entity/list.html', params)


@superuser_required
def add_entity(request):

    gallery_factory = PhotoGalleryForm.getGalleryFormset()
    initial_photos = PhotoGalleryForm.get_initial()

    if request.method == "POST":
        form = EntityForm(request.POST, request.FILES, initial={'is_new_entity':True})
        gallery_formset = gallery_factory(request.POST, request.FILES, initial=initial_photos)

        if form.is_valid() and gallery_formset.is_valid():
            entity = form.save(commit=False)

            owner_id = form.cleaned_data['owner_id']
            new_user_username = form.cleaned_data['new_user_username']
            new_user_password = form.cleaned_data['new_user_password']
            new_user_first_name = form.cleaned_data['new_user_first_name']
            new_user_last_name = form.cleaned_data['new_user_last_name']
            new_user_email = form.cleaned_data['new_user_email']

            if owner_id:
                user = User.objects.get(pk=owner_id)
                entity.user = user

            elif new_user_username and new_user_password:
                user_email = new_user_email if new_user_email else entity.email
                user, created = User.objects.get_or_create(username=new_user_username, email=user_email, password=new_user_password, first_name=new_user_first_name, last_name=new_user_last_name)
                user.set_password(new_user_password)
                user.save()
                entity.user = user
            else:
                entity.user = request.user

            gallery = Gallery.objects.create()
            entity.gallery = gallery
            entity.save()
            form.save_m2m()
            PhotoGalleryForm.save_galleryphoto(entity.gallery, gallery_formset)

            send_email = form.cleaned_data['send_welcome_email']
            if send_email:
                helpers.mailing.send_template_email(
                    'Bienvenid@ a la app del Boniatillo',
                    entity.email,
                    'welcome_entity',
                    {'entity': entity}
                )

            return redirect('entity_detail', pk=entity.pk)
        else:
            print(form.errors.as_data())
            print(gallery_formset.errors)
    else:
        form = EntityForm(initial={'is_new_entity':True})
        gallery_formset = gallery_factory(initial=initial_photos)

    categories = Category.objects.all()

    return render(request, 'entity/add.html', {
        'is_new': True,
        'categories': categories,
        'form': form,
        'gallery_formset':gallery_formset
    })


@login_required
def entity_edit(request, pk):

    entity = get_object_or_404(Entity, pk=pk)
    gallery = entity.gallery
    can_edit = request.user.is_superuser or request.user == entity.user

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para editar la entidad')
        return redirect('entity_detail', pk=entity.pk )

    gallery_factory = PhotoGalleryForm.getGalleryFormset(gallery)
    initial_photos = PhotoGalleryForm.get_initial(gallery)

    if request.method == "POST":
        form = EntityForm(request.POST, request.FILES, instance=entity)
        gallery_formset = gallery_factory(request.POST, request.FILES, initial=initial_photos)

        if form.is_valid() and gallery_formset.is_valid():

            entity = form.save(commit=False)
            if gallery is None:
                gallery = Gallery.objects.create()
            entity.gallery = gallery
            entity.save()
            form.save_m2m()

            PhotoGalleryForm.save_galleryphoto(entity.gallery, gallery_formset)

            return redirect('entity_detail', pk=entity.pk)
        else:
            print(form.errors.as_data())
            print(gallery_formset.errors)
    else:
        form = EntityForm(instance=entity)
        gallery_formset = gallery_factory(initial=initial_photos)

    categories = Category.objects.all()

    return render(request, 'entity/edit.html', {
        'form': form,
        'gallery_formset':gallery_formset,
        'categories': categories,
        'entity': entity,
        'can_edit_entity':can_edit
    })
