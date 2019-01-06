"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import datetime

class DateFormatter(object):

    @staticmethod
    def year_month_day(year, month, day):
        return datetime.datetime.strptime("%d-%d-%d"%(year, month, day), "%Y-%m-%d")

    @staticmethod
    def year_month_day_now():
        now = datetime.datetime.now()
        return datetime.datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")

    def __init__(self, weeks=0, days=0, hours=0, minutes=0, seconds=0):
        self._time_now = datetime.datetime.now()
        if weeks > 0:
            new_now = self._time_now + datetime.timedelta(days=weeks*7)
            self._time_now = new_now
        if days > 0:
            new_now = self._time_now + datetime.timedelta(days=days)
            self._time_now = new_now
        if hours > 0:
            new_now = self._time_now + datetime.timedelta(seconds=hours*60*60)
            self._time_now = new_now
        if minutes > 0:
            new_now = self._time_now + datetime.timedelta(seconds=minutes*60)
            self._time_now = new_now
        if seconds > 0:
            new_now = self._time_now + datetime.timedelta(seconds=seconds)
            self._time_now = new_now

    @property
    def time_now(self):
        return self._time_now

    def abbreviated_weekday(self):
        return self._time_now.strftime("%a")

    def full_weekday(self):
        return self._time_now.strftime("%A")

    def abbreviated_month(self):
        return self._time_now.strftime("%b")

    def full_month(self):
        return self._time_now.strftime("%B")

    def locate_appropriate_date_time(self):
        return self._time_now.strftime("%c")

    def decimal_day_of_month(self):
        return self._time_now.strftime("%d")

    def hour_24_hour_clock(self):
        return self._time_now.strftime("%H")

    def hour_12_hour_clock(self):
        return self._time_now.strftime("%I")

    def decimal_day_of_year(self):
        return self._time_now.strftime("%j")

    def decimal_month(self):
        return self._time_now.strftime("%m")

    def decimal_minute(self):
        return self._time_now.strftime("%M")

    def am_or_pm(self):
        return self._time_now.strftime("%p")

    def decimal_second(self):
        return self._time_now.strftime("%S")

    def decimal_week_number_sunday_as_first(self):
        return self._time_now.strftime("%U")

    def decimal_week_number_monday_as_first(self):
        return self._time_now.strftime("%W")

    def decimal_weekday(self):
        return self._time_now.strftime("%w")

    def date_representation(self):
        return self._time_now.strftime("%x")

    def time_representation(self):
        return self._time_now.strftime("%X")

    def year_2_digit(self):
        return self._time_now.strftime("%y")

    def year_4_digit(self):
        return self._time_now.strftime("%Y")

    def timezone_name(self):
        return self._time_now.strftime("%Z")
