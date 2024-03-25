from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse
from .models import Advert


class Index(View):

    def get(self, request):
        models = Advert.objects.all()
        context = {
            'models': models,
        }
        return HttpResponse(render(request, 'callboard/index.html', context))
