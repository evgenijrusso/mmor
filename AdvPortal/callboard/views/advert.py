from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, \
    ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.http.response import HttpResponse
from django.contrib import messages
from callboard.models import Advert, User
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


class AdvertDetail(DetailView):  # class PostDetail(LoginRequiredMixin, DetailView):
    model = Advert
    template_name = 'callboard/advert_detail.html'
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Advert'
        return context


class AdvertCreate(CreateView):
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


class AdvertUpdate(UpdateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'callboard/advert_update.html'

    #    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        idu = self.kwargs.get('pk')
        return Advert.objects.get(pk=idu)

    def form_valid(self, form):
        messages.success(self.request, "The advert was updated successfully.")
        return super(AdvertUpdate, self).form_valid(form)


class AdvertDelete(DeleteView):
    model = Advert
    template_name = 'callboard/advert_delete.html'
    success_url = '/callboard/'


#    permission_required = ('news.delete_post',)


# ------подтверждение авторизации ---------
class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, template_name='callboard/invalid_code.html')
        return redirect('account_login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'callboard/profile.html'  # возвращаемся после авторизации
