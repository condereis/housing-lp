from django.conf import settings
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import render
from django.template import loader

from .forms import EstimateRequestForm


def estimate_request(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()

    form = EstimateRequestForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest()

    form.save()
    new_price = form.instance.price * 1.15 / settings.TOTAL_QUOTAS if form.instance.price else None
    return JsonResponse({
        'price': round(new_price, 2) if new_price else None,
        'condominium': round(form.instance.condominium / settings.TOTAL_QUOTAS, 2) if form.instance.condominium else None,
        'iptu': round(form.instance.iptu / settings.TOTAL_QUOTAS, 2) if form.instance.iptu else None,
        'currency': form.instance.currency if form.instance.currency else None,
        'savings': int(100 * (form.instance.price - new_price) / form.instance.price) if new_price else None
    })

def index(request):
    form = EstimateRequestForm()
    return render(request, 'core/index.html', {'form': form})
