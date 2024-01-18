from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _

from .models import User
from .forms import UserCreateForm, UserUpdateForm
from task_manager.mixins import (UserPermissionMixin, UserAuthRequiredMixin,
                                 ObjectDeleteProtectionMixin)


class UserListView(ListView):
    template_name = 'users/user_list.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'form.html'
    success_message = _('User created successfully')
    extra_context = {
        'header': _('Create User'),
        'button': _('Register')
    }


class UserUpdateView(SuccessMessageMixin, UserAuthRequiredMixin,
                     UserPermissionMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'form.html'

    login_url = reverse_lazy('login')
    success_url = reverse_lazy('users')
    success_message = _('User updated successfully')

    permission_message = _('You do not have permission to edit another user.')
    permission_url = success_url

    permission_denied_message = _('You must to be log in')

    extra_context = {
        'header': _('Update User'),
        'button': _('Update')
    }


class UserDeleteView(SuccessMessageMixin, UserAuthRequiredMixin,
                     ObjectDeleteProtectionMixin,
                     UserPermissionMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'

    login_url = reverse_lazy('login')

    success_url = reverse_lazy('users')
    success_message = _('User successfully removed')

    permission_message = _('You do not have permission to edit another user.')
    permission_url = success_url

    permission_denied_message = _('You must to be log in')

    protected_url = success_url
    protection_message = _('Cannot delete user because it is in use')
