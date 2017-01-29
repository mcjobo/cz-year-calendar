from dateutil.rrule import rrulestr
import dates
import vobject
import datetime
import pytz
from operator import itemgetter

cal_str = '''
BEGIN:VCALENDAR
PRODID:Zimbra-Calendar-Provider
VERSION:2.0
BEGIN:VTIMEZONE
TZID:Europe/Berlin
BEGIN:STANDARD
DTSTART:16010101T030000
TZOFFSETTO:+0100
TZOFFSETFROM:+0200
RRULE:FREQ=YEARLY;WKST=MO;INTERVAL=1;BYMONTH=10;BYDAY=-1SU
TZNAME:CET
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:16010101T020000
TZOFFSETTO:+0200
TZOFFSETFROM:+0100
RRULE:FREQ=YEARLY;WKST=MO;INTERVAL=1;BYMONTH=3;BYDAY=-1SU
TZNAME:CEST
END:DAYLIGHT
END:VTIMEZONE
BEGIN:VEVENT
UID:3b61b806-9a09-4216-90f8-b9ae9f409f2f
RRULE:FREQ=WEEKLY;INTERVAL=1;BYDAY=TH
SUMMARY:Iranische Gruppe
DESCRIPTION:\n
ORGANIZER;CN=Anja Bolay:mailto:anja@bolay.org
DTSTART;TZID="Europe/Berlin":20170105T160000
DTEND;TZID="Europe/Berlin":20170105T180000
STATUS:CONFIRMED
CLASS:PUBLIC
TRANSP:OPAQUE
LAST-MODIFIED:20170119T160327Z
DTSTAMP:20170119T160327Z
SEQUENCE:0
END:VEVENT
END:VCALENDAR
'''

alianz_str = '''
BEGIN:VCALENDAR
PRODID:Zimbra-Calendar-Provider
VERSION:2.0
BEGIN:VEVENT
UID:8cb03196-eea8-46d4-99ea-d6efd547e2df
SUMMARY:Allianzgebetswoche
DESCRIPTION:\n
ORGANIZER;CN=Anja Bolay:mailto:anja@bolay.org
DTSTART;VALUE=DATE:20170109
DTEND;VALUE=DATE:20170116
STATUS:CONFIRMED
CLASS:PUBLIC
X-MICROSOFT-CDO-ALLDAYEVENT:TRUE
TRANSP:TRANSPARENT
LAST-MODIFIED:20170119T160523Z
DTSTAMP:20170119T160523Z
SEQUENCE:0
END:VEVENT
END:VCALENDAR
'''


school_holiday = "ferien_mecklenburg-vorpommern_2017.ics"
public_holiday= "feiertage_mecklenburg-vorpommern_2017.ics"



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
                for date in dates.daterange2(rule_start, rule_end, False):
                    entry = {}
                    entry["data"] = events["data"]
                    entry["summary"] = event.summary.value
                    entry["start"] = date if type(date) is datetime.date else date.date()
                    entry["end"] = date if type(date) is datetime.date else date.date()
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
