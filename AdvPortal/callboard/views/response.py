from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect
from ..models import Response, Advert
from ..forms import ResponseForm
from ..filter import AdvertFilter


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


class ResponseCreate(LoginRequiredMixin, CreateView):
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


class ResponseUpdate(LoginRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'callboard/response_update.html'

    def get_object(self, **kwargs):
        idu = self.kwargs.get('pk')
        return Response.objects.get(pk=idu)

    def form_valid(self, form):
        messages.success(self.request, "The response was updated successfully.")
        return super(ResponseUpdate, self).form_valid(form)


class ResponseDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'callboard.advert_delete'
    permission_denied_message = "Permission Denied"
    model = Response
    template_name = 'callboard/response_delete.html'
    success_url = '/callboard/responses/'


class ResponseUserList(LoginRequiredMixin, ListView):
    """ Отклики пользователей на объявление """
    template_name = 'callboard/responses.html'  # 'reply_users_to_advert'
    context_object_name = 'adverts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Advert.objects.filter(
            responses__user=self.request.user, responses__accept=True).order_by('-date')
        self.filterset = AdvertFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
def reply_on(request, pk):
    obj = Response.objects.get(id=pk)
    obj.status_on()
    return redirect('response_detail', id)


@login_required
def reply_off(request, pk):
    obj = Response.objects.get(id=pk)
    obj.status_off()
    return redirect('response_detail', obj.id)
