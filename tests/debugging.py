# TODO: figure out wtf this function is doing and why it needs to exist :facepalm:
def get_list_index(LIST, key, val):
  '''Get index or indices of list elements when those elements are dicts with keys containing values matching the val
  Args:
    LIST: list
    key: str key from dict
    val: something that can be evaluated as a logical'''
    
  return next((index for (index, d) in enumerate(LIST) if d[key] == val), None)


import re
sport='mlb'
config_subset=cfg['bs']['parse_data']
market_subset=config_subset['markets']['mlb']['home_runs']
event=bs_obj.events_list[3]

nba = Odds.Odds('fd', config=cfg).get_data('nba').parse_data('nba_finals')
mlb = Odds.Odds('fd', config=cfg).get_data('mlb')
test=Odds.Odds('fd', config=cfg).get_data('mlb').parse_data('home_runs')
event = mlb.events_list[11]


# import requests
# sport='mlb'
# config_subset=cfg['br']['get_data']
# resp=requests.get(
#   'https://il.betrivers.com/api/service/sportsbook/offering/listview/events?t=&cageCode=847&type=live&type=prematch&groupId=1000093616&pageNr=1&pageSize=10&offset=0', 
#   headers={
#     'User-Agent':'libcurl/7.88.1 r-curl/4.3.2 httr/1.4.4',
#     'Accept':'application/json, text/xml, application/xml, */*'
#   }
# )
# 
