# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from wallets.models import Payment, Wallet, TransactionLog


@login_required
def pending_payments(request):
    pending_payments = Payment.objects.pending(user=request.user)
    return render(request, 'wallets/pending_payments.html', {
        'pending_payments': pending_payments
    })


@login_required
def payment_detail(request, pk):

    payment = get_object_or_404(Payment, pk=pk)
    can_edit = request.user == payment.receiver or request.user.is_superuser

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para ver este pago')
        return redirect('entity_detail', pk=payment.pk )

    if request.method == "POST":
        action = request.POST.get("action", "")

        if action == 'accept':
            payment.accept_payment()
            return redirect('pending_payments')

        if action == 'cancel':
            payment.cancel_payment()
            return redirect('pending_payments')

    else:
        user_type, entity = payment.receiver.get_related_entity()
        bonus = entity.bonus(payment.total_amount)
        return render(request, 'wallets/payment_detail.html', {
            'payment': payment,
            'bonus': bonus
        })


@login_required
def user_wallet(request):

    pending_payments = Payment.objects.pending(user=request.user)
    wallet = Wallet.objects.filter(user=request.user).first()

    transactions = TransactionLog.objects.filter(wallet=wallet)

    return render(request, 'wallets/user_wallet.html', {
        'pending_payments': pending_payments,
        'wallet': wallet, 'transactions':transactions
    })
