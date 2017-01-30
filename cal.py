# -*- coding: utf-8 -*-

import pdf
import datetime
import parsecal
import pytz
import caldav2
import dates

tz = pytz.timezone('Europe/Berlin')

def draw_page(canvas,start,end):

    print("parse holiday")
    holiday = parsecal.read_holiday()
    holiday_list = parsecal.populate_list(holiday, start, end)
    for holiday in holiday_list:
        daterange = dates.daterange2(holiday["start"], holiday["end"], False)
        for date in daterange:
            pdf.draw_holiday(canvas, date)

    pdf.create_Site(canvas, start, end, "CZ Rostock 2017")
    pdf.draw_legend(canvas, "AG - Afrikanische Gruppe / GBA + MAT - Gemeindebewegerabend & MA-Treffen / GC - Gemeinde College / GF - Gebetsfrühstück","IG Iranische Gruppe / JA - Jugendabend / KU - Konfirmandenunterricht / MAT KiGoDi - MA-Treffen Kindergottesdienst / SD - Segnungsdienst")


    event_list = caldav2.get_events(start, end)

    list = parsecal.populate_list(event_list, start, end)

    date = start.day-1
    counter = 1
    entry_print = []
    for entry in list:
        ent = {"date":entry["start"], "summary": entry["summary"], "multi": entry["multi"]}
        if entry["multi"]:
            pdf.draw_multi_date(canvas, entry)
        elif entry["start"] == date:
            entry_print.append(ent)
        else:
            date = entry["start"]
            pdf.draw_date(canvas, entry_print)
            entry_print = []
            entry_print.append(ent)

    pdf.draw_date(canvas, entry_print)

canvas = pdf.create_pdf("cal.pdf")
start = datetime.datetime(2017,1,1, tzinfo=tz)
end = datetime.datetime(2017,6,30, tzinfo=tz)
draw_page(canvas,start,end)


pdf.add_page(canvas)
start = datetime.datetime(2017, 7, 1,  tzinfo=tz)
end = datetime.datetime(2017, 12, 31, tzinfo=tz)
draw_page(canvas,start,end)

pdf.save(canvas)