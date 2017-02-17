# -*- coding: utf-8 -*-

import caldav
from configobj import ConfigObj




def connect():
  # Caldav url
  #url = "https://bolay.org/dav/jorg@bolay.org/calendar"
  config = ConfigObj("year/settings.ini")
  url = config["server"]["url"]

  client = caldav.DAVClient(url, username=config["user"]["username"], password=config["user"]["password"])
  calendar = caldav.Calendar(client, url=url)

  return calendar


def search_calendar(calendar, start, end):
  results = calendar.date_search(start,end)
  return results


def iter_event(results):
  event_list = []
  for event in results:
    event_values = {}
    event_values["data"] = event.data
    event_list.append(event_values)
  return event_list

def get_events(start,end):
  cal = connect()
  events = search_calendar(cal,start,end)
  return iter_event(events)


# start = datetime(2017,1,1)
# end = datetime(2017,6,30)
# cal = connect()
# events = search_calendar(cal,start,end)
# ev = iter_event(events)
#for event in ev:
#    print(event)
