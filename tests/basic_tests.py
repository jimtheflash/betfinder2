from betfinder2 import Odds
import os
import yaml

cfg_pth=os.environ['BF2_PATH']
with open(cfg_pth) as f:
  cfg = yaml.safe_load(f)

# testing...
test = Odds.Odds('fd', config=cfg).get_data('mlb').parse_data('strikeouts')
# test = Odds.Odds('fd', config=cfg).get_data('nba').parse_data('nba_finals')

# works :)
bs_obj = Odds.Odds('bs', config=cfg).get_data('mlb')
csr_obj = Odds.Odds('csr', config=cfg).get_data('mlb')
dk_obj = Odds.Odds('dk', config=cfg).get_data('mlb').parse_data('home_runs')
fd_obj = Odds.Odds('fd', config=cfg).get_data('mlb').parse_data('strikeouts').parse_data('home_runs')
mgm_obj = Odds.Odds('mgm', config=cfg).get_data('mlb')
pb_obj = Odds.Odds('pb', config=cfg).get_data('mlb')


# # broken >:(
# br_obj = Odds.Odds('br', config=cfg).get_data('mlb')
