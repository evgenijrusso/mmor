from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect
from ..models import Response, Advert
from ..forms import ResponseForm


class ResponseList(ListView):
    model = Response
    template_name = 'callboard/responses.html'
    context_object_name = 'responses'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of responses'
        return context


class ResponseDetail(DetailView):
    model = Response
    template_name = 'callboard/response_detail.html'
    context_object_name = 'response'


class ResponseCreate(CreateView):
    model = Response
    form_class = ResponseForm
    context_object_name = 'response'
    template_name = 'callboard/response_create.html'
    success_url = '/callboard/responses/'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.user = self.request.user
        response.save()
        messages.success(self.request, "The response was created successfully.")
        return super(ResponseCreate, self).form_valid(form)


class ResponseUpdate(UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'callboard/response_update.html'

    def get_object(self, **kwargs):
        idu = self.kwargs.get('pk')
        return Response.objects.get(pk=idu)

    def form_valid(self, form):
        messages.success(self.request, "The response was updated successfully.")
        return super(ResponseUpdate, self).form_valid(form)


class ResponseDelete(DeleteView):
    model = Response
    template_name = 'callboard/response_delete.html'
    success_url = '/callboard/responses/'
