from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.conf import settings
from .models import Status
from .forms import StatusCreateForm, StatusUpdateForm
from ..mixins import UserAuthRequiredMixin, ObjectDeleteProtectionMixin


class BaseStatusView(UserAuthRequiredMixin):
    login_url = reverse_lazy(getattr(settings, 'LOGIN_URL', 'login'))
    permission_denied_message = _('You must to be log in')


class StatusListView(BaseStatusView, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(BaseStatusView, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status created successfully')
    extra_context = {
        'header': _('Create status'),
        'button': _('Create'),
    }


class StatusUpdateView(BaseStatusView, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status updated successfully')
    extra_context = {
        'header': _('Update status'),
        'button': _('Update'),
    }


class StatusDeleteView(BaseStatusView, ObjectDeleteProtectionMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
    protected_url = success_url
    success_message = _('Status successfully removed')
    permission_denied_message = _('You must be logged in')
    protection_message = _('Cannot delete status because it is in use')
