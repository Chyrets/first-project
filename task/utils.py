from datetime import datetime, timedelta
from calendar import HTMLCalendar

from django.views.generic import ListView


class CalendarUtil(HTMLCalendar, ListView):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(CalendarUtil, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, tasks, notes):
        start_tasks_per_day = tasks.filter(start_date__day=day)
        end_tasks_per_day = tasks.filter(end_date__day=day)
        notes_per_day = notes.filter(date__day=day)
        d = ''

        for task in start_tasks_per_day:
            d += f'<li class="list-group-item list-group-item-primary">{task.get_html_url} </li>'

        for task in end_tasks_per_day:
            d += f'<li class="list-group-item list-group-item-warning">{task.get_html_url} </li>'

        for note in notes_per_day:
            d += f'<li class="list-group-item list-group-item-info"> {note.get_html_url} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, tasks, notes):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, tasks, notes)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formattmonth(self, tasks, notes, theyear, themonth, withyear=True):

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, tasks, notes)}\n'
        return cal
