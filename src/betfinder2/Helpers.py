import yaml

def read_yaml(filename):
  with open(filename) as f:
    output = yaml.safe_load(f)
  return output
