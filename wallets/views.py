# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

import helpers
from helpers import superuser_required
from wallets.forms.TransactionForm import TransactionForm
from wallets.models import Payment, Wallet, TransactionLog, Transaction, WalletType


@login_required
def pending_payments(request):
    pending_payments = Payment.objects.pending(user=request.user)

    page = request.GET.get('page')
    pending_payments = helpers.paginate(pending_payments, page, elems_perpage=10)
    params = {
        'payments': pending_payments
    }

    if request.is_ajax():
        response = render(request, 'wallets/payments_query.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'wallets/pending_payments.html', params)



@login_required
def payment_detail(request, pk):

    payment = get_object_or_404(Payment, pk=pk)
    can_edit = request.user == payment.receiver or request.user.is_superuser

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para ver este pago')
        return redirect('entity_detail', pk=payment.pk )

    params = { 'payment': payment }

    if request.method == "POST":
        action = request.POST.get("action", "")
        if action == 'accept':
            try:
                payment.accept_payment()
                if request.is_ajax():
                    return JsonResponse({'success':True})
                else:
                    return redirect('pending_payments')
            except Wallet.NotEnoughBalance:
                params['notenoughbalance'] = True
                if request.is_ajax():
                    response = JsonResponse({'error':'notenoughbalance', 'error_message':'El monedero no tiene saldo suficiente.'})
                    response.status_code = 400
                    return response

        if action == 'cancel':
            payment.cancel_payment()
            if request.is_ajax():
                return JsonResponse({'success': True})
            else:
                return redirect('pending_payments')

    sender_type, sender = payment.sender.get_related_entity()
    receiver_type, entity = payment.receiver.get_related_entity()
    params['sender'] = sender
    if receiver_type == 'entity':
        params['bonus'] = entity.bonus(payment.total_amount, sender_type)

    return render(request, 'wallets/payment_detail.html', params)


@login_required
def user_wallet(request):

    pending_payments = Payment.objects.pending(user=request.user)
    wallet = Wallet.objects.filter(user=request.user).first()
    transactions = TransactionLog.objects.filter(wallet=wallet)
    page = request.GET.get('page')
    transactions = helpers.paginate(transactions, page, elems_perpage=10)

    if request.is_ajax():
        response = render(request, 'wallets/transaction_logs_query.html', {'transactions':transactions})
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'wallets/user_wallet.html', {
            'pending_payments': pending_payments,
            'showing_all': False,
            'wallet': wallet, 'transactions': transactions
        })


@superuser_required
def admin_payments(request):
    payments = Payment.objects.all().order_by('-timestamp')

    page = request.GET.get('page')
    payments = helpers.paginate(payments, page, elems_perpage=10)
    params = {
        'payments': payments,
        'showing_all': True
    }

    if request.is_ajax():
        response = render(request, 'wallets/payments_query.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'wallets/admin_payments.html', params)

@superuser_required
def transaction_list(request):

    start_date = timezone.now() - datetime.timedelta(days=71)
    end_date = timezone.now()

    transactions = Transaction.objects.all().order_by('-timestamp')
    transactions_bydate = Transaction.objects.filter(timestamp__gte=start_date,
                                                  timestamp__lte=end_date) \
                                        .annotate(day=TruncDay('timestamp')) \
                                      .values('day') \
                                      .annotate(total=Sum('amount')).order_by('day')


    page = request.GET.get('page')
    transactions = helpers.paginate(transactions, page, elems_perpage=10)
    params = {
        'transactions': transactions,
    }

    if request.is_ajax():
        response = render(request, 'wallets/transactions_query.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        params['transactions_bydate'] = transactions_bydate
        return render(request, 'wallets/transactions_list.html', params)



@superuser_required
def wallet_search(request):

    wallets = Wallet.objects.all().select_related('user')

    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q'].strip()
        entry_query = helpers.get_query(query_string, ['user__entity__name', 'user__person__name', 'user__username'])
        if entry_query:
            wallets = wallets.filter(entry_query)

    page = request.GET.get('page')
    wallets = helpers.paginate(wallets, page, elems_perpage=12)

    params = {
        'ajax_url': reverse('wallet_search'),
        'query_string': query_string,
        'wallets': wallets,
    }

    if request.is_ajax():
        response = render(request, 'wallets/wallets_query.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'wallets/wallets_list.html', params)


@superuser_required
def new_transaction(request):

    params = {
        'ajax_url': reverse('wallet_search'),
    }

    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES)

        if form.is_valid():
            transaction = form.save(commit=False)
            wallet_from = transaction.wallet_from


            success = True
            try:
                t = wallet_from.new_transaction(
                    transaction.amount,
                    wallet=transaction.wallet_to,
                    concept=transaction.concept,
                    bonus=transaction.is_bonification,
                    made_byadmin=True,
                    is_euro_purchase=False,
                )
                transaction.wallet_to.notify_transaction(t)

            except Wallet.NotEnoughBalance:
                params['notenoughbalance'] = True
                params['wallet_from_display'] = wallet_from.user.get_related_entity()[1]
                params['wallet_to_display'] = transaction.wallet_to.user.get_related_entity()[1] if transaction.wallet_to.user else 'Débito'
                success = False

            if success:
                return redirect('transaction_list')
        else:
            print(form.errors.as_data())
    else:
        form = TransactionForm()

    params['form'] = form
    return render(request, 'wallets/new_transaction.html', params)


@superuser_required
def wallet_types_list(request):

    wallet_types = WalletType.objects.all()
    return render(request, 'wallets/types_list.html', {'wallet_types':wallet_types})
