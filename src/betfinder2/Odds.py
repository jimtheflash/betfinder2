import random, requests, time

class Odds:
  
  def __init__(self, sportsbook, config):
    self.sportsbook = sportsbook
    self.config = config
    
  def get_data(self, sport, sleep_max = 3):
    self.sport = sport
    config_subset = self.config[self.sportsbook]['get_data']
    
    # if self.sportsbook == 'br':
    #   all_events_uri = config_subset['all_events_stem']
    #   all_events_params = config_subset['all_events_params']
    #   all_events_params.update({'groupId':1000093652})
    #   headers = requests.utils.default_headers()
    #   headers.update({'User-Agent': 'Mozilla/5.0'})
    #   all_events = requests.get(all_events_uri, headers=headers, params = all_events_params)

    if self.sportsbook == 'bs':
      all_events = requests.get(config_subset['all_events_stem'][sport], params = config_subset['all_events_params']).json()
      all_event_ids = [i['id'] for i in all_events['events']]
      list_of_event_dicts = [requests.get(config_subset['event_stem'] + i, params = config_subset['event_params']).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]

    # if self.sportsbook == 'csr':
    #   all_events = requests.get(config_subset['all_events_stem'] + config_subset['event_groups'][sport], params = {'format':'json'}).json()
    #   all_event_ids = [i['eventId'] for i in all_events['eventGroup']['events']]
    #   list_of_event_dicts = [requests.get(event_stem + i, params = {'format':'json'}).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]

    if self.sportsbook == 'dk':
      all_events = requests.get(config_subset['all_events_stem'] + config_subset['event_groups'][sport], params = {'format':'json'}).json()
      all_event_ids = [i['eventId'] for i in all_events['eventGroup']['events']]
      list_of_event_dicts = [requests.get(config_subset['event_stem'] + i, params = {'format':'json'}).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]
    
    if self.sportsbook == 'fd':
      all_events_params = config_subset['all_events_params']
      all_events_params.update({'customPageId':sport})
      all_events = requests.get(config_subset['all_events_stem'], params = all_events_params).json()
      all_event_ids = list(all_events['attachments']['events'].keys())
      event_params = config_subset['event_params']
      event_tabs = config_subset['event_tabs'][sport]
      list_of_event_dicts = []
      for i in all_event_ids:
        time.sleep(random.random() * sleep_max)
        popular = requests.get(config_subset['event_stem'] + i, params = event_params.update({'eventId': i})).json()
        list_of_event_dicts.append(popular)
        for j in event_tabs:
          tab = requests.get(config_subset['event_stem'] + i, params = event_params.update({'tab': j})).json()
          list_of_event_dicts.append(tab)
          
    if self.sportsbook == 'pb':
      'do this'
      
    if self.sportsbook == 'mgm':
      'do this'

      
        
      
    
