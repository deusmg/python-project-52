from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.conf import settings
from .models import User
from .forms import UserCreateForm, UserUpdateForm
from task_manager.mixins import (
    UserPermissionMixin,
    UserAuthRequiredMixin,
    ObjectDeleteProtectionMixin,
)


class BaseUserView(UserAuthRequiredMixin):
    login_url = reverse_lazy(getattr(settings, 'LOGIN_URL', 'login'))
    permission_denied_message = _('You must to be log in')


class UserListView(ListView):
    template_name = 'users/user_list.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    success_message = _('User created successfully')


class UserUpdateView(BaseUserView, SuccessMessageMixin, UserPermissionMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'

    success_url = reverse_lazy('users')
    success_message = _('User updated successfully')

    permission_message = _('You do not have permission to edit another user.')
    permission_url = success_url


class UserDeleteView(BaseUserView,
                     ObjectDeleteProtectionMixin,
                     UserPermissionMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = User
    template_name = 'users/delete.html'

    success_url = reverse_lazy('users')
    success_message = _('User successfully removed')

    permission_message = _('You do not have permission to edit another user.')
    permission_url = success_url

    protected_url = success_url
    protection_message = _('Cannot delete user because it is in use')
