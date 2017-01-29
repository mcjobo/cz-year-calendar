from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
import dates
from dateutil.relativedelta import relativedelta
from calendar import monthrange


borderLeft = 20
borderRight = 20
borderTop = 25
borderBottom = 20
borderHorizontal = borderTop + borderBottom
borderVertical = borderLeft + borderRight
monthCorrection = 0


def calc_dimension(can):
    pagesize = can._pagesize
    tup = ((pagesize[0] - borderVertical ) / 6, (pagesize[1] - borderHorizontal) / 32)
    return tup


def draw_rect(can, month, day, weekend, holiday=False):
    print(month, day, weekend, holiday)
    tup = calc_dimension(can)
    cell_width = tup[0]
    cell_height = tup[1]
    if holiday:
      can.setFillColorRGB(0.1,0.1,0.5)
      can.rect((month) * cell_width + borderLeft + cell_width -3, (31 - day) * cell_height + borderBottom, 3, cell_height,
               fill=True)
    else:
      if weekend:
        can.setFillColorRGB(0.1,0.1,0.7)
      can.rect((month) * cell_width + borderLeft, (31 - day) * cell_height + borderBottom, cell_width, cell_height, fill=weekend)
    can.setFillColorRGB(0, 0, 0)


def draw_string(can, month, day, text, indent_bottom, indent_left, center = True):
    tup = calc_dimension(can)
    cell_width = tup[0]
    cell_height = tup[1]
    if center:
        can.drawString((month) * cell_width + borderLeft + indent_left, (30 - day) * cell_height + borderBottom + indent_bottom, text)

    else:
        can.drawCentredString((month) * cell_width + borderLeft + indent_left,
                          (30 - day) * cell_height + borderBottom + indent_bottom, text)


def draw_days_str(canvas, start, end):
    for date in dates.daterange(start, end):
      day_str = str(date.day) + " " + dates.get_day_name(date, "de_DE", "EE")
      draw_string(canvas, date.month - 1 - monthCorrection, date.day - 1, day_str, 5, 2)


def draw_month_header(canvas, start, end):
    month_list = []
    for date in dates.daterange(start, end):
        month_name = dates.get_month_name(date, "de_DE", "MMMM")
        if month_name not in month_list:
            month_list.append(month_name)

    tup = calc_dimension(canvas)
    cell_width = tup[0]
    counter = 0
    for month in month_list:
        draw_string(canvas, counter, -1, month, 5, cell_width/2, False)
        counter += 1


def draw_date(canvas, event_list):
    tup = calc_dimension(canvas)
    cellWidth = tup[0]
    cellHeight = tup[1]
    indentLeft = 29
    # print ("height: ", cellHeight, " ", cellWidth, " ", cellHeight/2, " ", indentLeft+2, date)

    number = 0
    for event in event_list:
      number += 1
      if number == 1:
        left = indentLeft
        bottom = cellHeight/2+1
      elif number == 2:
        left = indentLeft
        bottom = 2
      elif number == 3:
        left = ((cellWidth-indentLeft)/2)  + indentLeft
        bottom = cellHeight/2+1
      elif number == 4:
        left = ((cellWidth-indentLeft)/2)  + indentLeft
        bottom = 2
      #print("indent: ", left, " ", bottom)
      half_size = (((cellWidth-indentLeft)/2) + 2 + indentLeft) - (indentLeft+2)
      stringsize = half_size - 2 if len(event_list) > 2 else half_size*2
      cutString = cut_string_to_size(canvas, event["summary"], stringsize)
      draw_string(canvas, event["date"].month-1-monthCorrection, event["date"].day-1, cutString, bottom, left, True)


def cut_string_to_size(canvas, text, size):
  print("orig: ", canvas.stringWidth(text, canvas._fontname, canvas._fontsize), text, size)
  cut = False
  cutText = text
  textWidth = canvas.stringWidth(cutText, canvas._fontname, canvas._fontsize)
  while textWidth > size:
    cut = True
    cutText = cutText[:-1]
    textWidth = canvas.stringWidth(cutText+"..", canvas._fontname, canvas._fontsize)

  cutText = cutText+".." if cut else cutText
  print("cut: ", cutText)
  return cutText


def create_pdf(name):
    can = canvas.Canvas(name)
    can.setPageSize(landscape(A4))
    return can


def create_Site(canvas, start, end, header):
    for month in range(6):
      for day in range(32):
        date = start + relativedelta(months=month)+relativedelta(days=day-1)
        weekend = (date.isoweekday() == 7)
        month_days = monthrange(date.year, start.month+month)
        is_day = day >= 1 and day <= month_days[1]
        # print("date: ", date,date.isoweekday(), weekend, is_day, month, day, month_days)
        draw_rect(canvas, month, day, weekend and is_day)

    canvas.setFont("Helvetica", 9)
    draw_days_str(canvas, start, end)
    draw_month_header(canvas, start, end)
    draw_header(canvas, header)
    canvas.setFont("Helvetica", 7)


def add_page(canvas):
    canvas.showPage()
    global monthCorrection
    monthCorrection =  monthCorrection + 6


def save (can):
    can.save()


def draw_header(can, header):
  pagesize = can._pagesize
  old_font = can._fontsize
  can.setFont("Helvetica", 12)
  can.drawString(borderLeft, pagesize[1]-20 , header)
  can.setFont("Helvetica", old_font)


def draw_legend(canvas, legend1, legend2):
  pagesize = canvas._pagesize
  old_font = canvas._fontsize
  canvas.setFont("Helvetica", 5)
  canvas.drawRightString(pagesize[0]-borderRight, pagesize[1] - 10, legend1)
  canvas.drawRightString(pagesize[0] - borderRight, pagesize[1] - 20, legend2)
  canvas.setFont("Helvetica", old_font)


def draw_holiday(canvas, date):
  print(date)
  draw_rect(canvas, date.month-1 if date.month <=6 else date.month-7, date.day, False, True)