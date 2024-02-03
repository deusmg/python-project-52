from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from django.conf import settings

from ..mixins import UserAuthRequiredMixin, ObjectDeleteProtectionMixin
from .models import Label
from .forms import LabelCreateForm, LabelUpdateForm


class BaseLabelView(UserAuthRequiredMixin):
    login_url = reverse_lazy(getattr(settings, 'LOGIN_URL', 'login'))
    permission_denied_message = _('You must to be log in')


class LabelListView(BaseLabelView, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(BaseLabelView, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label created successfully')


class LabelUpdateView(BaseLabelView, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelUpdateForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label updated successfully')


class LabelDeleteView(BaseLabelView, ObjectDeleteProtectionMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')
    protected_url = success_url
    success_message = _('Label successfully removed')
    protection_message = _('Cannot delete label because it is in use')
