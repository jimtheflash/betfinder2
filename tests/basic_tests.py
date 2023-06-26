from betfinder2 import Odds
import os
import yaml

cfg_pth=os.environ['BF2_PATH']
with open(cfg_pth) as f:
  cfg = yaml.safe_load(f)

# works :)
bs_obj = Odds.Odds('bs', config=cfg).get_data('mlb')
csr_obj = Odds.Odds('csr', config=cfg).get_data('mlb')
dk_obj = Odds.Odds('dk', config=cfg).get_data('mlb')
fd_obj = Odds.Odds('fd', config=cfg).get_data('mlb')
mgm_obj = Odds.Odds('mgm', config=cfg).get_data('mlb')
pb_obj = Odds.Odds('pb', config=cfg).get_data('mlb')


## untested :shrugs:
# br
