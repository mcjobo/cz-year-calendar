import datetime
from operator import itemgetter

import pytz
import vobject
from dateutil.rrule import rrulestr
from year import dates




school_holiday = "year/ferien_mecklenburg-vorpommern_2017.ics"
public_holiday= "year/feiertage_mecklenburg-vorpommern_2017.ics"



def populate_list(event_list, start, end):
    result_list = []
    for events in event_list:
        parsed = vobject.readOne(events["data"])
        for event in parsed.vevent_list:
            if hasattr(event, 'rrule'):
                recuring_str = event.rrule.name + ":" + event.rrule.value
                rrule = rrulestr(recuring_str,dtstart=event.dtstart.value, tzinfos=pytz.timezone('Europe/Berlin'))
                rule_start = start if start > event.dtstart.value else parsed.vevent.dtstart.value
                rule_end = end

                print ("between: ", rule_start, rule_end, rrule)
                between = rrule.between(rule_start, rule_end, True)
                for date in between:
                    entry = {}
                    entry["data"] = events["data"]
                    entry["summary"] = event.summary.value
                    entry["start"] = date if type(date) is datetime.date else date.date()
                    entry["end"] = date if type(date) is datetime.date else date.date()
                    result_list.append(entry)
            else:
                dtstart = event.dtstart.value if type(event.dtstart.value) is datetime.date else event.dtstart.value.date()
                dtend = event.dtend.value if type(event.dtend.value) is datetime.date else event.dtend.value.date()

                start = start.date() if type(start) is datetime.datetime else start
                end = end.date() if type(end) is datetime.datetime else end
                rule_start = start if start > dtstart else dtstart
                rule_end = end if end < dtend else dtend
                daterange = dates.daterange2(rule_start, rule_end, False)
                # for date in daterange:
                entry = {}
                entry["data"] = events["data"]
                entry["summary"] = event.summary.value
                # entry["start"] = date if type(date) is datetime.date else date.date()
                # entry["end"] = date if type(date) is datetime.date else date.date()
                entry["start"] = rule_start if type(rule_start) is datetime.date else rule_start.date()
                entry["end"] = rule_end if type(rule_end) is datetime.date else rule_end.date()
                entry["multi"] = len(daterange) > 1
                result_list.append(entry)

    res = sort_events(result_list)
    return res


def sort_events(result_list):
    res = sorted(result_list, key=itemgetter("start"))
    return res



def read_holiday():
    event_list = []
    with open(school_holiday, 'r') as ical:
        content = ical.read()
        event_list.append({"data":content})
        # print(content)
    with open(public_holiday, 'r') as ical:
        content = ical.read()
        event_list.append({"data": content})
        # print(content)
    return event_list

# list = populate_list([{"data":cal_str}], datetime.datetime(2017,1,1), datetime.datetime(2017,6,30))
# list = sort_result_list(list)
# for i in list:
#     print (i)
