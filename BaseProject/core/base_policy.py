# Portions of this file are adapted from Wagtail
# (https://github.com/wagtail/wagtail)
# Licensed under the BSD 3-Clause License

from django.utils.functional import cached_property
from django.contrib.auth import get_permission_codename, get_user_model
from django.contrib.contenttypes.models import ContentType

from BaseProject.core.utilities.models import resolve_model_string


class BasePermissionPolicy:
  """
  A 'permission policy' is an object that handles all decisions about the actions
  users are allowed to perform on a given model.

  BasePermissionPolicy is an abstract class that all permission policies inherit from.
  The only method that subclasses need to implement is `users_with_any_permission`;
  """

  def __init__(self, model):
    self._model_or_name = model

  @cached_property
  def model(self):
    model = resolve_model_string(self._model_or_name)
    # self.check_model(model)
    return model

  @cached_property
  def app_label(self):
    return self.model._meta.app_label

  @cached_property
  def _content_type(self):
    return ContentType.objects.get_for_model(self.model)

  def _get_permission_codenames(self, actions):
      return { get_permission_codename(action, self.model._meta) for action in actions }

  def _get_permission_name(self, action):
    """
    Get the full app-label-qualified permission name (as required by
    user.has_perm(...) ) for the given action on this model
    p/e. return app.action_model.
    """
    return "{}.{}".format(
      self.app_label,
      get_permission_codename(action, self.model._meta),
    )

  def user_has_permissions(self, user, actions: list, instance: any = None) -> bool:
    """
    Return whether the given user has permissions to perform the given action.

    actions = ['app.action_model', 'action', '']
    """
    if not user.is_authenticated or not user.is_active:
      return False

    for action in actions:
      if action in ["add", "change", "delete", "view"]:
        if not user.has_perm(self._get_permission_name(action)): return False
      else:
        if not user.has_perm(action): return False
    return True

  def user_has_any_permission(self, user, actions):
    """
    Return whether the given user has permission to perform any of the given actions
    on some or all instances of this model
    """
    if not user.is_authenticated or not user.is_active:
      return False

    return any(self.user_has_permissions(user, [action]) for action in actions)

