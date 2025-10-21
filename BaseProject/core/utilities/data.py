"""Portions of this file are adapted from NetBox
    (https://github.com/netbox-community/netbox)
    Licensed under the Apache License, Version 2.0"""

__all__ = (
  'flatten_dict',
)

def flatten_dict(d, prefix='', separator='.'):
  """
  Flatten nested dictionaries into a single level by joining key names with a separator.

  :param d: The dictionary to be flattened
  :param prefix: Initial prefix (if any)
  :param separator: The character to use when concatenating key names
  """
  ret = {}
  for k, v in d.items():
    key = separator.join([prefix, k]) if prefix else k
    if type(v) is dict:
      ret.update(flatten_dict(v, prefix=key, separator=separator))
    else:
      ret[key] = v
  return ret
