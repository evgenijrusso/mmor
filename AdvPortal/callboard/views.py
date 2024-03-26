from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView, TemplateView
from django.http.response import HttpResponse
from .models import Advert, User


class Index(View):

    def get(self, request):
        models = Advert.objects.all()
        context = {
            'models': models,
        }
        return HttpResponse(render(request, 'callboard/index.html', context))


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

