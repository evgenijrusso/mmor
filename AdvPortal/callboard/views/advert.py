from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, \
    ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.http.response import HttpResponse

from callboard.models import Advert
from callboard.forms import AdvertForm
from datetime import date


class Index(View):

    def get(self, request):
        models = Advert.objects.all()
        context = {
            'models': models,
        }
        return HttpResponse(render(request, 'callboard/index.html', context))


class AdvertList(ListView):
    model = Advert
    template_name = 'callboard/adverts.html'
    context_object_name = 'adverts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of adverts'
        return context


class AdvertDetail(DetailView):
    model = Advert
    template_name = 'callboard/advert_detail.html'
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Advert'
        return context


class AdvertCreate(LoginRequiredMixin, CreateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'callboard/advert_create.html'
    success_url = '/callboard/'

    #   permission_required = ('news.add_post',)

    def form_valid(self, form):
        advert = form.save(commit=False)
        advert.user = self.request.user
        advert.save()
        messages.success(self.request, "The advert was created successfully.")
        return super(AdvertCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AdvertUpdate(LoginRequiredMixin, UpdateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'callboard/advert_update.html'

    def get_object(self, **kwargs):
        idu = self.kwargs.get('pk')
        return Advert.objects.get(pk=idu)

    def form_valid(self, form):
        messages.success(self.request, "The advert was updated successfully.")
        return super(AdvertUpdate, self).form_valid(form)


class AdvertDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'callboard.advert_delete'
    permission_denied_message = "Permission Denied"
    model = Advert
    template_name = 'callboard/advert_delete.html'
    context_object_name = 'advert'
    success_url = '/callboard/'


