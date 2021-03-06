from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^payments/$', views.pending_payments, name='pending_payments'),
    url(r'^payments/admin$', views.admin_payments, name='admin_payments'),
    url(r'^payments/(?P<pk>[0-9a-f-]+)/$', views.payment_detail, name='payment_detail'),

    url(r'^wallet/$', views.user_wallet, name='user_wallet'),
    url(r'^wallet/search/$', views.wallet_search, name='wallet_search'),

    url(r'^wallet/types$', views.wallet_types_list, name='wallet_types_list'),
    url(r'^transactions/$', views.transaction_list, name='transaction_list'),
    url(r'^transactions/new/$', views.new_transaction, name='new_transaction'),


]