import datetime
from babel.dates import format_date # $ pip install babel
from dateutil import rrule, parser
from dateutil.relativedelta import relativedelta

def get_day_name(date, locale, syntax):
  return format_date(date, syntax, locale)

def get_month_name(date, locale, syntax):
  return format_date(date, syntax, locale)

def daterange(start_date, end_date):
  if start_date <= end_date:
    for n in range((end_date - start_date).days + 1):
      yield start_date + datetime.timedelta(n)
  else:
    for n in range((start_date - end_date).days + 1):
      yield start_date - datetime.timedelta(n)

def daterange2(start_date, end_date, incl_end=True):
  start_date = start_date if type(start_date) is datetime.date else start_date.date()
  end_date = end_date if type(end_date) is datetime.date else end_date.date()
  if start_date == end_date:
    return [start_date]
  end_date = end_date if incl_end else end_date + relativedelta(days=-1)
  dates = list(rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date))
  return dates