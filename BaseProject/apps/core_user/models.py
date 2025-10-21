from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import ValidationError

# from stdimage import StdImageField
from BaseProject.core.utilities.data import flatten_dict
# from BaseProject.core.models.mixins import CreateUpdateMixin
# from BaseProject.apps.custom_user.constants import USER_PERMISSIONS


# class User(CreateUpdateMixin, AbstractUser):
class User(AbstractUser):
    """
        All user are customer for the CentralTaxi
        User is_active for status general (active or inactive)
    """
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    # avatar = StdImageField(
    #     upload_to='usuarios/%Y/%m/',
    #     variations={
    #         'thumbnail': (56, 42, True),  # 4:3 landscape -> 40x30
    #         'card'     : (255, 340, True),  # 4:3 portrait -> 243x324
    #         'md'       : (304, 228, True),  # 4:3 landscape -> 260x195
    #     },
    #     default="usuarios/avatar.png"
    # )
    def __str__(self):
        return f'{self.username}'

    # class Meta:
    #     permissions = USER_PERMISSIONS

    # ========= Validations ==========
    def clean(self):
        if User.objects.filter(username=self.username).exclude(id=self.id).count():
            raise ValidationError({ 'user': "El nombre del usuario ya se encuentra registrado" })
        return super().clean()


class UserConfig(models.Model):
  """Portions of this file are adapted from NetBox
    (https://github.com/netbox-community/netbox)
    Licensed under the Apache License, Version 2.0"""

  user = models.OneToOneField(
    to=User,
    on_delete=models.CASCADE,
    related_name='config'
  )
  data = models.JSONField(default=dict)

  class Meta:
    ordering = ['user']
    verbose_name = _('user preferences')
    verbose_name_plural = _('user preferences')

  def get(self, path, default=None):
    """
    Retrieve a configuration parameter specified by its dotted path. Example:

        userconfig.get('foo.bar.baz')

    :param path: Dotted path to the configuration key. For example, 'foo.bar' returns self.data['foo']['bar'].
    :param default: Default value to return for a nonexistent key (default: None).
    """
    d = self.data
    keys = path.split('.')

    # Iterate down the hierarchy, returning the default value if any invalid key is encountered
    try:
      for key in keys:
        d = d[key]
      return d
    except (TypeError, KeyError):
      pass

    # Finally, return the specified default value (if any)
    return default

  def all(self):
    """
    Return a dictionary of all defined keys and their values.
    """
    return flatten_dict(self.data)

  def set(self, path, value, commit=False):
    """
    Define or overwrite a configuration parameter. Example:

        userconfig.set('foo.bar.baz', 123)

    Leaf nodes (those which are not dictionaries of other nodes) cannot be overwritten as dictionaries. Similarly,
    branch nodes (dictionaries) cannot be overwritten as single values. (A TypeError exception will be raised.) In
    both cases, the existing key must first be cleared. This safeguard is in place to help avoid inadvertently
    overwriting the wrong key.

    :param path: Dotted path to the configuration key. For example, 'foo.bar' sets self.data['foo']['bar'].
    :param value: The value to be written. This can be any type supported by JSON.
    :param commit: If true, the UserConfig instance will be saved once the new value has been applied.
    """
    d = self.data
    keys = path.split('.')

    # Iterate through the hierarchy to find the key we're setting. Raise TypeError if we encounter any
    # interim leaf nodes (keys which do not contain dictionaries).
    for i, key in enumerate(keys[:-1]):
      if key in d and type(d[key]) is dict:
        d = d[key]
      elif key in d:
        err_path = '.'.join(path.split('.')[:i + 1])
        raise TypeError(
          _("Key '{path}' is a leaf node; cannot assign new keys").format(path=err_path)
        )
      else:
        d = d.setdefault(key, {})

    # Set a key based on the last item in the path. Raise TypeError if attempting to overwrite a non-leaf node.
    key = keys[-1]
    if key in d and type(d[key]) is dict:
      if type(value) is dict:
        d[key].update(value)
      else:
        raise TypeError(
          _("Key '{path}' is a dictionary; cannot assign a non-dictionary value").format(
            path=path)
        )
    else:
      d[key] = value

    if commit:
      self.save()

  def clear(self, path, commit=False):
    """
    Delete a configuration parameter specified by its dotted path. The key and any child keys will be deleted.
    Example:

        userconfig.clear('foo.bar.baz')

    Invalid keys will be ignored silently.

    :param path: Dotted path to the configuration key. For example, 'foo.bar' deletes self.data['foo']['bar'].
    :param commit: If true, the UserConfig instance will be saved once the new value has been applied.
    """
    d = self.data
    keys = path.split('.')

    for key in keys[:-1]:
      if key not in d:
        break
      if type(d[key]) is dict:
        d = d[key]

    key = keys[-1]
    d.pop(key, None)  # Avoid a KeyError on invalid keys

    if commit:
      self.save()
