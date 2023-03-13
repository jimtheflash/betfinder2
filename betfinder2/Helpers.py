import yaml

def get_list_index(LIST, key, val):
  '''Get index or indices of list elements when those elements are dicts with keys containing values matching the val
  Args:
    LIST: list
    key: str key from dict
    val: something that can be evaluated as a logical'''
  return next((index for (index, d) in enumerate(LIST) if d[key] == val), None)

def read_yaml(filename):
  '''Read a .yaml file as a dict
  Args:
    filename: str filename'''
  with open(filename) as f:
    output = yaml.safe_load(f)
  return output
