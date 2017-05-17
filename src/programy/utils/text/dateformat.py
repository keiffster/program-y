import datetime, time

class DateFormatter(object):

    @staticmethod
    def year_month_day(year, month, day):
        return datetime.datetime.strptime("%d-%d-%d"%(year, month, day), "%Y-%m-%d")

    @staticmethod
    def year_month_day_now():
        now = datetime.datetime.now()
        return datetime.datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")

    def __init__(self, weeks=0, days=0, hours=0, mins=0, secs=0):
        self._time_now = datetime.datetime.now()
        if weeks > 0:
            self._time_now += datetime.timedelta(days=days*7)
        if days > 0:
            self._time_now += datetime.timedelta(days=days)
        if hours > 0:
            self._time_now += datetime.timedelta(seconds=hours*60*60)
        if mins > 0:
            self._time_now += datetime.timedelta(seconds=mins*60)
        if secs > 0:
            self._time_now += datetime.timedelta(secs)

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

