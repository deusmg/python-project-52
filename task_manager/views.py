from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.http import HttpResponse


class IndexView(TemplateView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        try:
            a = None
            a.hello() # Creating an error with an invalid line of code
            return HttpResponse("Hello, world. You're at the pollapp index.")
        except Exception as e:
            report_exception(request, extra_data={'my_custom_info': 'some additional info'})
            raise e

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    next_page = reverse_lazy('home')
    success_message = _('You are login in')
    extra_context = {
        'header': _('Log in'),
        'button': _('Enter')
    }


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('home')
    success_message = _('You are logout')

    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
