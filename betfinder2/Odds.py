import random, re, requests, time
import polars as pl

## TODO: in cases where this function is necessary, coerce the object to a dict beforehand, then we don't need this function anymore
## this function exists cuz initially i treated python lists like r lists, when in fact a python dict is more akin to an r list. 
## ok we figured out what it does and why (when a list should be a dict cuz we want to access indices by names, this enables it, but really that means our lists should be dicts in most cases)
def get_list_index(LIST, key, val):
  '''Get index or indices of list elements when those elements are dicts with keys containing values matching the val
  Args:
    LIST: list
    key: str key from dict
    val: something that can be evaluated as a logical'''
    
  return next((index for (index, d) in enumerate(LIST) if d[key] == val), None)

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

    # For each of the sports books, read the config and grab the data for that sport
    # TODO: there's got to be a better way than all this elif nonsense...
    if self.sportsbook == 'br':
      
      pass
      # # TODO: this is broken, see github issues
      # all_events_params = config_subset['all_events_params']
      # all_events_params.update({'groupId':config_subset['group_ids'][sport]})
      # all_events = requests.get(config_subset['all_events_stem'], params=all_events_params, headers=config_subset['viable_headers']).json()
      # all_event_ids = [i['event']['id'] for i in all_events['events']]
      # list_of_event_dicts = []
      # for i in all_event_ids:
      #   event_params=config_subset['event_params']
      #   event_params.update({'eventId':i})
      #   list_of_event_dicts.append(requests.get(config_subset['event_stem'], params=event_params).json())
    elif self.sportsbook == 'bs':
      all_events = requests.get(config_subset['all_events_stem'][sport], params=config_subset['all_events_params']).json()
      all_event_ids = [i['event']['id'] for i in all_events['events']]
      list_of_event_dicts = [requests.get(config_subset['event_stem'] + str(i), params=config_subset['event_params']).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]
    elif self.sportsbook == 'csr':
      all_events = requests.get(config_subset['all_events_stem'][sport], headers=config_subset['viable_headers']).json()
      all_comps = all_events['competitions']
      all_event_ids = [i['id'] for i in all_comps[get_list_index(all_comps, 'name', config_subset['competition_names'][sport])]['events']]
      list_of_event_dicts = [requests.get(config_subset['event_stem'] + i, headers=config_subset['viable_headers']).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]
    elif self.sportsbook == 'dk':
      # TODO: move the params into the config
      all_events = requests.get(config_subset['all_events_stem'] + str(config_subset['event_groups'][sport]), params={'format':'json'}).json()
      all_event_ids = [i['eventId'] for i in all_events['eventGroup']['events']]
      list_of_event_dicts = [requests.get(config_subset['event_stem'] + str(i)).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]
    elif self.sportsbook == 'fd':
      all_events_params = config_subset['all_events_params']
      all_events_params.update({'customPageId':sport})
      all_events = requests.get(config_subset['all_events_stem'], params=all_events_params).json()
      ## create list of events, add the main page to it
      list_of_event_dicts = []
      list_of_event_dicts.append(all_events)
      ## iterate through the event ids to get all the active events
      all_event_ids = list(all_events['attachments']['events'].keys())
      event_params = config_subset['event_params']
      event_tabs = config_subset['event_tabs'][sport]
      for i in all_event_ids:
        event_output = []
        time.sleep(random.random() * sleep_max)
        event_params.update({'eventId':str(i)})
        main = requests.get(config_subset['event_stem'], params=event_params).json()
        main['tab_name'] = 'main-event'
        event_output.append(main)
        for j in event_tabs:
          event_params['tab'] = j
          tab = requests.get(config_subset['event_stem'], params=event_params).json()
          tab['tab_name'] = j
          event_output.append(tab)
          del event_params['tab'], tab
        list_of_event_dicts.append(event_output)
    elif self.sportsbook == 'mgm':
      all_events_params = config_subset['all_events_params']
      sport_val = config_subset['sport_values'][sport]
      all_events_params.update({'competitionId':sport_val})
      all_events = requests.get(config_subset['all_events_stem'], params=all_events_params, headers=config_subset['viable_headers']).json()
      # TODO: fix this nasty 'keep the first element' logic
      marquee_widget = [i for i in all_events['widgets'] if i['type'] == 'Marquee'][0]
      fixtures = marquee_widget['payload']['fixtures']
      fixture_ids = [i['fixture']['id'] for i in fixtures]
      list_of_event_dicts = []
      for fid in fixture_ids:
        event_params = config_subset['event_params']
        event_params.update({'fixtureIds':fid})
        event_output = requests.get(config_subset['event_stem'], params=event_params, headers=config_subset['viable_headers']).json()
        list_of_event_dicts.append(event_output)
    elif self.sportsbook == 'pb':
      all_events = requests.get(config_subset['all_events_stem']['part1'] + str(config_subset['sport_values'][sport]) + config_subset['all_events_stem']['part2'], params=config_subset['all_events_params'], headers=config_subset['viable_headers']).json()
      all_event_ids = [i['key'] for i in all_events['events']]
      list_of_event_dicts = [requests.get(config_subset['event_stem'] + str(i), headers=config_subset['viable_headers']).json() for i in all_event_ids if time.sleep(random.random() * sleep_max) is None]
    else:
      list_of_event_dicts = []
      
    self.sport = sport
    self.events_list = [i for i in list_of_event_dicts if i is not None]

    return self
  
  def parse_data(self, market):
    '''parse_data extracts the data from a specific market from the events_list attribute of an Odds object. Upcoming markets are in scope, but live markets are not.
    Args:
      market: str market to parse'''
    
    # extract some constants from configs that will be used across books
    config_subset = self.config['parse_data']
    market_subset = config_subset['markets'][self.sport][market]
    events_list = self.events_list
    parsed_events = []
    if self.sportsbook == 'br':
      pass
    elif self.sportsbook == 'bs':
      for event in events_list:
          # if there's a specific label to get, do that, else use regex
          if 'offer_label' in market_subset.keys():
            try:
              selected_offer = [i for i in event['betOffers'] if i['criterion']['label'] == market_subset['offer_label']]
            except:
              continue
          elif 'offer_regex' in market_subset.keys():
            try:
              selected_offer = [i for i in event['betOffers'] if re.search(pattern=market_subset['offer_regex'], string=i['criterion']['label']) is not None]
            except:
              continue
          else:
            continue
          parsed_events.append(selected_offer)
      
    elif self.sportsbook == 'csr':
      pass
    elif self.sportsbook == 'dk':
      # pull out some values from the markets
      category_name = market_subset['category_name']
      subcategory_name = market_subset['subcategory_name']
      # loop through all the events
      for event in events_list:
        # print(event['event']['name'])
        # check if it has started, move along if it breaks
        try:
          event_start = event['event']['eventStatus']['state'] == 'STARTED'
        except:
          continue
        # if it has started, then move along
        if event_start:
          continue
        # get to parsin' within a try-except block
        try:
          ## create an output dict with a few values
          output = {}
          output['event_start'] = event['event']['startDate']
          output['matchup'] = event['event']['name']
          ## extract the correct category and subcategory info
          category_data = event['eventCategories'][get_list_index(event['eventCategories'], 'name', category_name)]
          subcategory_data = category_data['componentizedOffers'][get_list_index(category_data['componentizedOffers'], 'subcategoryName', subcategory_name)]
          # TODO: finding offers like this is gross - two empty lists doesn't feel like its a reproducible pattern. but finding an object named 'offers' does!
          offers = subcategory_data['offers'][0][0]
          outcomes = offers['outcomes']
          output['outcomes'] = offers['outcomes']
          parsed_events.append(output)
        except:
          continue
    elif self.sportsbook == 'fd':
      # loop through the events in the events_list
      for event in events_list:
        output = {}
        # if there's a tab_name, get the market from that tab
        if 'tab_name' in market_subset.keys():
          try:
            # find the markets if the event is a list or dict
            if isinstance(event, list):
              tab_markets = event[get_list_index(event, 'tab_name', market_subset['tab_name'])]['attachments']['markets']
            elif isinstance(event, dict):
              tab_markets = event['attachments']['markets']
            else:
              continue
          except:
            continue
        else:
          try:
            # if there isn't a tab name, then just get the markets (it oughta just be a dict)
            tab_markets = event['attachments']['markets']
          except:
            continue
        # loop through the markets in the tab
        if tab_markets == {}:
          continue
        for tab_market in tab_markets:
          try:
            # get the market dict
            tm_dict = tab_markets[tab_market]
            # check if the market name matches exactly if we need it to
            tm_dict_name = tm_dict['marketName']
            if 'market_name' in market_subset.keys():
              # if not an exact match move on
              if tm_dict_name != market_subset['market_name']:
                continue
              else:
                output['outcomes'] = tm_dict
            # otherwise see if its a regex
            elif 'market_regex' in market_subset.keys():
              # if the market name doesn't hit the regex move on
              if re.search(market_subset['market_regex'], tm_dict_name) is None:
                continue
              else:
                output['outcomes'] = tm_dict
            else:
              continue
          except:
            continue
        # extract some info about events based on market_type
        #### TODO: HANDLE THE DIFFERENT WAYS THIS SHIT GETS PARSED OUT, SOMEHOW
        if market_subset['market_type'] == 'future':
          output['event_start'] = None
          output['name'] = None
        elif isinstance(event, list):
          try:
            event_data = event[0]['attachments']['events']
            output['event_start'] = event_data[list(event_data.keys())[0]]['openDate']
            output['name'] = event_data[list(event_data.keys())[0]]['name']
          except:
            pass
        elif isinstance(event, dict):
          try:
            if len(event['attachments']['events'].keys()) == 1:
              event_data = event[list(event.keys())[0]]['attachments']['events']
              output['event_start'] = event_data[list(event_data.keys())[0]]['openDate']
              output['name'] = event_data[list(event_data.keys())[0]]['name']
            else:
              pass
          except:
            pass
        else:
          pass
        # return that output object
        parsed_events.append(output)
    elif self.sportsbook == 'mgm':
      pass
    elif self.sportsbook == 'pb':
      pass
    else:
      parsed_events = []
    # check if there are already parsed events; if there aren't, create the dict
    if not hasattr(self, 'parsed_events'):
      self.parsed_events = {}
    # create a new attribute of the parsed_events dict for the market
    self.parsed_events[market] = [i for i in parsed_events if i is not None and i != {} and i != []]
    return(self)
  
  def tidy_df(self):
    '''tidy_df extracts the relevant fields from the parsed events and renames them to be consistent across books, and generates a dataFrame with the following columns:
        
        - book: Odds object sportsbook
        - sport: Odds object sport
        - market: Odds object market
        - matchup: Odds object matchup for matchups or tournaments, else null
        - start: the starting date and time for the event
        - playerid: for bets involving specific players, extracts the book-specific player identifier, else "team" or "game"
        - teamid: for bets involving a player on a team or a team, the book-specific team identifier, else "game"
        - overunder: for bets involving an over under, either "over" or "under", else null
        - line: for bets involving a betting line, the specific line as a number, else null
        - americanodds: american odds for the bet, can't be null'''
    
    config_subset = self.config['tidy_df']
    output = pl.DataFrame(schema={
        'book':str,
        'sport':str,
        'market':str,
        'matchup':str,
        'event_start':str,
        'playerid':str,
        'teamid':str,
        'over_under':str,
        'line':pl.Float32,
        'american_odds':pl.Float32
        })
        
    if self.sportsbook == 'br':
      pass
    elif self.sportsbook == 'bs':
      pass
    elif self.sportsbook == 'csr':
      pass
    elif self.sportsbook == 'dk':
      
      def dk_df(parsed_event):
        outcomes_df = pl.DataFrame(parsed_event['outcomes'])
        
        try:
          playerid = outcomes_df['dkPlayerId']
        except:
          playerid = None
        
        if playerid is not None:
          teamid = None
        else:
          teamid = outcomes_df['label']
        
        output_df = pl.DataFrame({
          'book':None,
          'sport':None,
          'market':None,
          'matchup':parsed_event['matchup'],
          'event_start':parsed_event['event_start'],
          'playerid':playerid,
          'teamid':teamed 
        })
        
        
      df = pl.DataFrame(data={
        'book':str,
        'sport':str,
        'market':str,
        'matchup':str,
        'playerid':str,
        'teamid':str,
        'overunder':str,
        'line':pl.Float32,
        'americanodds':pl.Float32
        })
      
      
    elif self.sportsbook == 'fd':
      pass
    elif self.sportsbook == 'mgm':
      pass
    elif self.sportsbook == 'pb':
      pass
    else:
      pass
    
    return self
    
