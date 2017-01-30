# -*- coding: utf-8 -*-

from datetime import datetime
import caldav
from caldav.elements import dav, cdav
from configobj import ConfigObj


config = ConfigObj("settings.ini")

def connect():
  # Caldav url
  url = "https://bolay.org/dav/jorg@bolay.org/calendar"

  client = caldav.DAVClient(url, username=config["User"]["username"], password=config["User"]["password"])
  #principal = client.principal()
  # calendars = principal.calendars()

  # print ("\nClient: ", client)
  # print ("\nPrinzipal: ", principal)

  calendar = caldav.Calendar(client, url="https://bolay.org/dav/jorg@bolay.org/CZ-Rostock")
  #principal.calendar(cal_id="https://bolay.org/dav/jorg@bolay.org/CZ-Rostock")
  # print ("The Cal: ", calendar)
  #prop = calendar.get_properties([dav.DisplayName()])
  # print ("\nProperties: ", prop)

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
    #print ("Found", event)
    #print (event.get_properties([dav.DisplayName()]))
    # print (event.instance.vevent.summary.name, " ", event.instance.vevent.summary.value)
    # print(event.instance.vevent.dtstart.name, " ", event.instance.vevent.dtstart.value)
    # print(event.instance.vevent.dtend.name, " ", event.instance.vevent.dtend.value)
    # if hasattr(event.instance.vevent, 'rrule'):
    #   print(event.instance.vevent.rrule.name, " ", event.instance.vevent.rrule.value)
    #
    # print (event.instance.vevent.__dict__)
    # print(event.data)
    #print(event.instance.__dict__)
    #print ("\ndict: ", event.instance.vevent.summary.__dict__)
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
