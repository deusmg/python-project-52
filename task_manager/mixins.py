from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class UserPermissionMixin(UserPassesTestMixin):

    permission_message = None
    permission_url = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class PermissionDeniedMixin:

    permission_denied_message = None
    permission_denied_url = None

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_url)


class UserAuthRequiredMixin(LoginRequiredMixin, PermissionDeniedMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            self.permission_denied_message = _('You must to be log in')
            self.permission_denied_url = self.login_url
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ObjectDeleteProtectionMixin(PermissionDeniedMixin):

    protection_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            self.permission_denied_message = self.protection_message
            self.permission_denied_url = self.protected_url
            return self.handle_no_permission()


class TaskAuthorPermissionMixin(UserPassesTestMixin, PermissionDeniedMixin):

    author_url = None
    author_message = None

    def test_func(self):
        return self.request.user.id == self.get_object().author.id

    def handle_no_permission(self):
        messages.error(self.request, self.author_message)
        return redirect(self.author_url)
