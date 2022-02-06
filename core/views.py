from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    # return render(request, 'core/index.html', {})
    template = loader.get_template('core/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))