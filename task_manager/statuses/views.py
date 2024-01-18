from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Status
from .forms import StatusCreateForm, StatusUpdateForm
from ..mixins import UserAuthRequiredMixin, ObjectDeleteProtectionMixin


class StatusListView(UserAuthRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'

    login_url = reverse_lazy('login')

    permission_denied_message = _('You must to be log in')


class StatusCreateView(SuccessMessageMixin, UserAuthRequiredMixin, CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = 'form.html'

    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')

    success_message = _('Status created successfully')
    permission_denied_message = _('You must to be log in')

    extra_context = {
        'header': _('Create status'),
        'button': _('Create'),
    }


class StatusUpdateView(SuccessMessageMixin, UserAuthRequiredMixin, UpdateView):
    model = Status
    form_class = StatusUpdateForm
    template_name = 'form.html'

    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')

    success_message = _('Status updated successfully')
    permission_denied_message = _('You must to be log in')

    extra_context = {
        'header': _('Update status'),
        'button': _('Update'),
    }


class StatusDeleteView(SuccessMessageMixin, UserAuthRequiredMixin,
                       ObjectDeleteProtectionMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('statuses')
    protected_url = success_url

    success_message = _('Status successfully removed')
    permission_denied_message = _('You must to be log in')
    protection_message = _('Cannot delete status because it is in use')
