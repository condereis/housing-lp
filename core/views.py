from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader

from .forms import EstimateRequestForm


def estimate_request(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EstimateRequestForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            print(type(form.instance.price))
            new_price = form.instance.price * 1.15 / settings.TOTAL_QUOTAS if form.instance.price else None
            return JsonResponse({
                'price': round(new_price, 2) if new_price else None,
                'condominium': round(form.instance.condominium / settings.TOTAL_QUOTAS, 2) if form.instance.condominium else None,
                'iptu': round(form.instance.iptu / settings.TOTAL_QUOTAS, 2) if form.instance.iptu else None,
                'currency': form.instance.currency if form.instance.currency else None,
                'savings': int(100 * (form.instance.price - new_price) / form.instance.price) if new_price else None
            })
        else:
            print(form.errors)


def index(request):
    form = EstimateRequestForm()
    return render(request, 'core/index.html', {'form': form})



# def index(request):
#     # return render(request, 'core/index.html', {})
#     template = loader.get_template('core/index.html')
#     context = {
#     }
#     return HttpResponse(template.render(context, request))
