from betfinder2 import Odds
import os
import yaml

cfg_pth=os.environ['BF2_PATH']
with open(cfg_pth) as f:
  cfg = yaml.safe_load(f)

# works locally :)
try:
  bs_obj = Odds.Odds('bs', config=cfg).get_data('mlb')
except:
  print('died at bs')
  
try:
  csr_obj = Odds.Odds('csr', config=cfg).get_data('mlb')
except:
  print('died at csr')
  
try:
  dk_obj = Odds.Odds('dk', config=cfg).get_data('wnba')
except:
  print('died at dk')

try:
  fd_obj = Odds.Odds('fd', config=cfg).get_data('wnba')
except:
  print('died at fd')

try:
  mgm_obj = Odds.Odds('mgm', config=cfg).get_data('mlb')
except:
  print('died at mgm')

try:
  pb_obj = Odds.Odds('pb', config=cfg).get_data('mlb')
except:
  print('died at pb')


# # broken >:(
# br_obj = Odds.Odds('br', config=cfg).get_data('mlb')
