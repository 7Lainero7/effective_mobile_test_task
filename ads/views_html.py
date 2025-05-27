from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q

from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from .filters import AdFilter


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return render(request, 'ads/error.html', {'message': 'Нет доступа'})
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return render(request, 'ads/error.html', {'message': 'Нет доступа'})
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})


@login_required
def propose_exchange(request, ad_id):
    receiver_ad = get_object_or_404(Ad, pk=ad_id)

    # Нельзя предлагать обмен своему же объявлению
    if receiver_ad.user == request.user:
        messages.error(request, 'Нельзя предложить обмен своего товара на свой же товар!')
        return redirect('ad_list')

    # Получаем объявления текущего пользователя для выбора
    user_ads = Ad.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        selected_ad_id = request.POST.get('sender_ad')

        if form.is_valid() and selected_ad_id:
            sender_ad = get_object_or_404(Ad, pk=selected_ad_id, user=request.user)
            proposal = form.save(commit=False)
            proposal.ad_sender = sender_ad
            proposal.ad_receiver = receiver_ad
            proposal.status = 'pending'
            proposal.save()
            messages.success(request, 'Предложение обмена отправлено!')
            return redirect('ad_list')
    else:
        form = ExchangeProposalForm()

    return render(request, 'ads/propose_exchange.html', {
        'form': form,
        'receiver_ad': receiver_ad,
        'user_ads': user_ads
    })


def ad_list(request):
    qs = Ad.objects.all().order_by('-created_at')
    ad_filter = AdFilter(request.GET, queryset=qs)
    # Можно добавить пагинацию, например:
    paginator = Paginator(ad_filter.qs, 10)
    page_number = request.GET.get('page')
    ads_page = paginator.get_page(page_number)
    return render(request, 'ads/ad_list.html', {'ads': ads_page, 'filter': ad_filter})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ad_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def public_proposals_page(request):
    sender_filter = request.GET.get('sender', '')
    receiver_filter = request.GET.get('receiver', '')
    status_filter = request.GET.get('status', '')

    proposals = ExchangeProposal.objects.all()

    sender_options = User.objects.filter(
        id__in=proposals.values_list('ad_sender__user', flat=True).distinct()
    )
    receiver_options = User.objects.filter(
        id__in=proposals.values_list('ad_receiver__user', flat=True).distinct()
    )

    if sender_filter:
        proposals = proposals.filter(ad_sender__user__id=sender_filter)
    if receiver_filter:
        proposals = proposals.filter(ad_receiver__user__id=receiver_filter)
    if status_filter:
        proposals = proposals.filter(status=status_filter)

    context = {
        'sender_options': sender_options,
        'receiver_options': receiver_options,
        'selected_sender': sender_filter,
        'selected_receiver': receiver_filter,
        'selected_status': status_filter,
        'proposals': proposals,
    }
    return render(request, 'ads/proposals_public.html', context)


@login_required
def my_proposals_page(request):
    sender_filter = request.GET.get('sender', '')
    receiver_filter = request.GET.get('receiver', '')
    status_filter = request.GET.get('status', '')

    proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user)
    )

    sender_options = User.objects.filter(
        id__in=proposals.values_list('ad_sender__user', flat=True).distinct()
    )
    receiver_options = User.objects.filter(
        id__in=proposals.values_list('ad_receiver__user', flat=True).distinct()
    )

    if sender_filter:
        proposals = proposals.filter(ad_sender__user__id=sender_filter)
    if receiver_filter:
        proposals = proposals.filter(ad_receiver__user__id=receiver_filter)
    if status_filter:
        proposals = proposals.filter(status=status_filter)

    # Можно дополнительно разделить на отправленные и полученные:
    context = {
        'sent_proposals': proposals.filter(ad_sender__user=request.user),
        'received_proposals': proposals.filter(ad_receiver__user=request.user),
        'sender_options': sender_options,
        'receiver_options': receiver_options,
        'selected_sender': sender_filter,
        'selected_receiver': receiver_filter,
        'selected_status': status_filter,
    }
    return render(request, 'ads/proposals_private.html', context)
