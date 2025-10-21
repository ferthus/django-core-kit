# Portions of this file are adapted from Wagtail
# (https://github.com/wagtail/wagtail)
# Licensed under the BSD 3-Clause License

from django.apps import apps
from django.db.models import Model


def get_model_string(model):
  """
  Returns a string that can be used to identify the specified model.

  The format is: `app_label.ModelName`

  This an be reversed with the `resolve_model_string` function
  """
  return model._meta.app_label + "." + model.__name__



def resolve_model_string(model_string, default_app=None):
  """
  Resolve an 'app_label.model_name' string into an actual model class.
  If a model class is passed in, just return that.

  Raises a LookupError if a model can not be found, or ValueError if passed
  something that is neither a model or a string.
  """
  if isinstance(model_string, str):
    try:
      app_label, model_name = model_string.split(".")
    except ValueError:
      if default_app is not None:
        # If we can't split, assume a model in current app
        app_label = default_app
        model_name = model_string
      else:
        raise ValueError(
          "Can not resolve {0!r} into a model. Model names "
          "should be in the form app_label.model_name".format(model_string),
          model_string,
        )

    return apps.get_model(app_label, model_name)

  elif isinstance(model_string, type) and issubclass(model_string, Model):
    return model_string

  else:
    raise ValueError(
      "Can not resolve {0!r} into a model".format(model_string), model_string
    )
