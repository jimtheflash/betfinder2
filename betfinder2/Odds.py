import random, requests, time

class Odds:
  '''Odds class is the workhorse of betfinder2, with methods for getting, parsing, and tidying data from several betting markets across a number of sportsbooks.'''
  
  def __init__(self, sportsbook, config):
    '''Initialize an Odds object.
    Args:
      sportsbook: str which sportsbooks to use
      config: dict of parameters for betfinder2'''
    self.sportsbook = sportsbook
    self.config = config[sportsbook]

  def get_data(self, sport, sleep_max=1):
    '''get_data GETs (in most cases) data for a given sport from the sportsbook.
    Args:
      sport: str of sport for markets to GET
      sleep_max: int maximum number of seconds to sleep between GET calls'''
    
    config_subset = self.config['get_data']
    
    # TODO: there's got to be a better way than all this elif nonsense...
    if self.sportsbook == 'br':
      pass
    elif self.sportsbook == 'bs':
      all_events = requests.get(config_subset['all_events_stem'][sport], params = config_subset['all_events_params']).json()
      all_event_ids = [i['event']['id'] for i in all_events['events']]
      list_of_event_dicts = [requests.get(config_subset['event_stem'] + str(i), params = config_subset['event_params']).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]
    elif self.sportsbook == 'csr':
      all_events = requests.get(config_subset['all_events_stem'][sport]).json()
      all_comps = all_events['competitions']
      all_event_ids = [i['id'] for i in all_comps[get_list_index(all_comps, 'name', config_subset['competition_names'][sport])]['events']]
      list_of_event_dicts = [requests.get(config_subset['event_stem'] + i).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]
    elif self.sportsbook == 'dk':
      all_events = requests.get(config_subset['all_events_stem'] + str(config_subset['event_groups'][sport]), params = {'format':'json'}).json()
      all_event_ids = [i['eventId'] for i in all_events['eventGroup']['events']]
      list_of_event_dicts = [requests.get(config_subset['event_stem'] + str(i)).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]
    elif self.sportsbook == 'fd':
      all_events_params = config_subset['all_events_params']
      all_events_params.update({'customPageId':sport})
      all_events = requests.get(config_subset['all_events_stem'], params = all_events_params).json()
      all_event_ids = list(all_events['attachments']['events'].keys())
      event_params = config_subset['event_params']
      event_tabs = config_subset['event_tabs'][sport]
      list_of_event_dicts = []
      for i in all_event_ids:
        event_output = []
        time.sleep(random.random() * sleep_max)
        del event_params['eventId']
        event_params['eventId'] = str(i)
        main = requests.get(config_subset['event_stem'], params = event_params).json()
        main['tab_name'] = 'main'
        event_output.append(main)
        for j in event_tabs:
          event_params['tab'] = j
          tab = requests.get(config_subset['event_stem'], params = event_params).json()
          tab['tab_name'] = j
          event_output.append(tab)
          del event_params['tab'], tab
        list_of_event_dicts.append(event_output)
    elif self.sportsbook == 'mgm':
      pass
    elif self.sportsbook == 'pb':
      all_events = requests.get(config_subset['all_events_stem']['part1'] + str(config_subset['sport_values'][sport]) + config_subset['all_events_stem']['part2'], params = config_subset['all_events_params']).json()
      all_event_ids = [i['key'] for i in all_events['events']]
      list_of_event_dicts = [requests.get(config_subset['event_stem'] + str(i)).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]
    else:
      list_of_event_dicts = []
      
    self.sport = sport
    self.events_list = [i for i in list_of_event_dicts if i is not None]

    return self
  
  def parse_data(self, market):
    '''parse_data extracts the data from a specific market from the events_list attribute of an Odds object. Upcoming markets are in scope, but live markets are not.
    Args:
      market: str market to parse'''
    
    config_subset = self.config['parse_data']
    market_subset = config_subset['markets'][self.sport][market]
    events_list = self.events_list
    parsed_events = []
    sportsbook = self.sportsbook
    if sportsbook == 'br':
      pass
    elif sportsbook == 'bs':
      
      def bs_parser(event, market_type, offer_label):
        event_state = event['events'][0]['state']
        if event_state == 'STARTED':
          return None
        output = {}
        output['event_start'] = event['events'][0]['start']
        output['matchup'] = event['events'][0]['name']
        if market_type == 'prop':
          selected_offer = [i for i in event['betOffers'] if i['criterion']['label'] == offer_label]
          output['outcomes'] = selected_offer[0]['outcomes']
          return output
      
      for i in events_list:
        try:
          parsed_event = parsed_events.append(bs_parser(i, market_subset['market_type'], market_subset['offer_label']))
        except:
          continue
    elif sportsbook == 'csr':
      pass
    elif sportsbook == 'dk':
      
      def dk_parser(event, market_type, category_name, subcategory_name):
        if event['event']['eventStatus']['state'] == 'STARTED':
          return None
        else:
          output = {}
          output['event_start'] = event['event']['startDate']
          output['matchup'] = event['event']['name']
          if market_type == 'prop':
            category_data = event['eventCategories'][get_list_index(event['eventCategories'], 'name', category_name)]
            subcategory_data = category_data['componentizedOffers'][get_list_index(category_data['componentizedOffers'], 'subcategoryName', subcategory_name)]
            # TODO: finding offers like this is gross - two empty lists doesn't feel like its a reproducible pattern. but finding an object named 'offers' does!
            offers = subcategory_data['offers'][0][0]
            outcomes = offers['outcomes']
            output['outcomes'] = offers['outcomes']
            return output
          else:
            return None

      for i in events_list:
        try:
          parsed_event = parsed_events.append(dk_parser(i, market_subset['market_type'], market_subset['category_name'], market_subset['subcategory_name']))
        except:
          continue
    elif sportsbook == 'fd':
      
      def fd_parser(event, market_type, tab_name, market_name):
        event_id = list(event[0]['attachments']['events'].keys())[0]
        if event[0]['attachments']['events'][event_id]['inPlay'] == True:
          return None
        output = {}
        output['event_start'] = event[0]['attachments']['events'][event_id]['openDate']
        output['matchup'] = event[0]['attachments']['events'][event_id]['name']
        if market_type == 'prop':
          tab_markets = event[get_list_index(event, 'tab_name', tab_name)]['attachments']['markets'].values()
          for market in tab_markets:
            if market['marketName'] != market_name:
              continue
            elif market['marketStatus'] != 'OPEN':
              continue
            else:
              output['outcomes'] = market['runners']
          
          return output

      for i in events_list:
        try:
          parsed_event = parsed_events.append(fd_parser(i, market_subset['market_type'], market_subset['tab_name'], market_subset['market_name']))
        except:
          continue

    elif sportsbook == 'mgm':
      pass
    elif sportsbook == 'pb':
      pass
    else:
      parsed_events = []
    
    self.market = market
    self.parsed_events = [i for i in parsed_events if i is not None]
    
    return self
  
  def tidy_data(self):
    config_subset = self.config['tidy_data']
    
    if self.sportsbook == 'br':
      pass
    elif self.sportsbook == 'bs':
      pass
    elif self.sportsbook == 'csr':
      pass
    elif self.sportsbook == 'dk':
      pass
    elif self.sportsbook == 'fd':
      pass
    elif self.sportsbook == 'mgm':
      pass
    elif self.sportsbook == 'pb':
      pass
    else:
      pass
    
    return self
    
