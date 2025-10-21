# Portions of this file are adapted from Wagtail
# (https://github.com/wagtail/wagtail)
# Licensed under the BSD 3-Clause License

from django.core.exceptions import PermissionDenied


class PermissionCheckedMixin:
    """
    Mixin for class-based views to enforce permission checks according to:

    * permission_policy (a policy object)
    * permission_required (list of permission codenames required)
    * any_permission_required (
        list of permission codenames - some of which are required
      )
    TODO: implement django-guardian for validate the permission on instance #
    """

    permission_policy = None
    permission_required = None
    any_permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if self.permission_required is not None:
            if not self.user_has_permissions(self.permission_required):
                raise PermissionDenied

        if self.any_permission_required is not None:
            if not self.user_has_any_permission(self.any_permission_required):
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def user_has_permissions(self, permissions):
        return not self.permission_policy or (
            self.permission_policy.user_has_permissions(self.request.user, permissions)
        )

    def user_has_any_permission(self, permissions):
        return not self.permission_policy or (
            self.permission_policy.user_has_any_permission(
                self.request.user, permissions
            )
        )
