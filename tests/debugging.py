import requests
sport='mlb'
config_subset=cfg['br']['get_data']


resp=requests.get(
  'https://il.betrivers.com/api/service/sportsbook/offering/listview/events?t=&cageCode=847&type=live&type=prematch&groupId=1000093616&pageNr=1&pageSize=10&offset=0', 
  headers={
    'User-Agent':'libcurl/7.88.1 r-curl/4.3.2 httr/1.4.4',
    'Accept':'application/json, text/xml, application/xml, */*'
  }
  )
