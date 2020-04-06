"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import datetime
try:
    import metoffer

except ModuleNotFoundError as error:
    print("First use 'pip install metoffer' before using this service")

from programy.utils.logging.ylogger import YLogger

DIRECTIONS = {'N': 'North',
              'NNE': 'North North East',
              'NE': 'North East',
              'ENE': 'East North East',
              'E': 'East',
              'ESE': 'East South East',
              'SE': 'South East',
              'SSE': 'South South East',
              'S': 'South',
              'SSW': 'South South West',
              'SW': 'South West',
              'WSW': 'West South West',
              'W': 'West',
              'WNW': 'West North West',
              'NW': 'North West',
              'NNW': 'North North West'}

PRESSURE_TENDANCY = {'F': "Falling",
                     'R': 'Rising'}


class DataPoint:

    def extract_attribute(self, json_data, name, data_type, time_period=None):
        if name in json_data:
            return json_data[name]
        else:
            if data_type == MetOfficeWeatherReport.OBSERVATION:
                YLogger.warning(self, '%s attribute missing from ObservationDataPoint data point', name)
            elif data_type == MetOfficeWeatherReport.FORECAST:
                if time_period == metoffer.THREE_HOURLY:
                    YLogger.warning(self, '%s attribute missing from three hourly forecast data point', name)
                if time_period == metoffer.DAILY:
                    YLogger.warning(self, '%s attribute missing from daily forecast data point', name)
            return None

    def direction_to_full_text(self, direction):
        if direction in DIRECTIONS:
            return DIRECTIONS[direction]
        return "Unknown"


class DailyForecastDayDataPoint(DataPoint):

    def __init__(self):
        self._type = None  # $
        self._wind_direction = None  # D
        self._temp_max = None  # Dm
        self._temperature_feels_like_max = None  # FDm
        self._wind_gust_noon = None  # Gn
        self._screen_relative_humidity_noon = None  # Hn
        self._precipitation_probability = None  # PPd
        self._wind_speed = None  # S
        self._uv_index_max = None  # U
        self._uv_guidance = None
        self._visibility_code = None  # V
        self._visibility_text = None
        self._weather_type_code = None  # W
        self._weather_type_text = None


    @property
    def type(self):
        return self._type

    #
    # Matches an AIML Pattern of
    # <pattern></pattern>
    #
    def to_program_y_text(self):
        text = "FORECAST DAYS TYPE %s WINDDIR %s WINDSPEED %s WINDGUST %s TEMP %s FEELS %s HUMID %s" \
               " RAINPROB %s" % (
                   self._type,
                   self._wind_direction,
                   self._wind_speed,
                   self._wind_gust_noon,
                   self._temp_max,
                   self._temperature_feels_like_max,
                   self._screen_relative_humidity_noon,
                   self._precipitation_probability)

        if self._uv_index_max is not None:
            text += " UVINDEX %s" % self._uv_index_max

        if self._uv_guidance is not None:
            text += " UVGUIDE %s" % self._uv_guidance

        if self._visibility_text is not None:
            text += " VIS %s" % self._visibility_text

        if self._weather_type_text is not None:
            text += " WEATHER %s" % self._weather_type_text

        return text

    def parse_json(self, json_data, data_type, time_period):
        self._type = self.extract_attribute(json_data, '$', data_type, time_period)
        self._wind_direction = self.extract_attribute(json_data, 'D', data_type, time_period)
        self._temp_max = self.extract_attribute(json_data, 'Dm', data_type, time_period)
        self._temperature_feels_like_max = self.extract_attribute(json_data, 'FDm', data_type, time_period)
        self._wind_gust_noon = self.extract_attribute(json_data, 'Gn', data_type, time_period)
        self._screen_relative_humidity_noon = self.extract_attribute(json_data, 'Hn', data_type, time_period)
        self._precipitation_probability = self.extract_attribute(json_data, 'PPd', data_type, time_period)
        self._wind_speed = self.extract_attribute(json_data, 'S', data_type, time_period)
        self._uv_index_max = self.extract_attribute(json_data, 'U', data_type, time_period)
        if self._uv_index_max is not None:
            self._uv_guidance = metoffer.guidance_UV(int(self._uv_index_max))
        self._visibility_code = self.extract_attribute(json_data, 'V', data_type, time_period)
        if self._visibility_code is not None:
            self._visibility_text = metoffer.VISIBILITY[self._visibility_code]
        self._weather_type_code = self.extract_attribute(json_data, 'W', data_type, time_period)
        if self._weather_type_code is not None:
            self._weather_type_text = metoffer.WEATHER_CODES[int(self._weather_type_code)]


class DailyForecastNightDataPoint(DataPoint):

    def __init__(self):
        self._type = None  # $
        self._wind_direction = None  # D
        self._temperature_feels_like_min = None  # FNm
        self._wind_gust_midnight = None  # Gm
        self._screen_relative_humidity_midnight = None  # Hm
        self._temp_min = None  # Nm
        self._precipitation_probability = None  # PPn
        self._wind_speed = None  # S
        self._visibility_code = None  # V
        self._visibility_text = None
        self._weather_type_code = None  # W
        self._weather_type_text = None

    @property
    def type(self):
        return self._type

    #
    # Matches an AIML Pattern of
    # <pattern></pattern>
    #
    def to_program_y_text(self):
        text = "WEATHER"

        if self._weather_type_text is not None:
            text += " TYPE %s" % self._weather_type_text

        text += " WINDDIR %s WINDGUST %s WINDSPEED %s TEMP %s FEELS %s HUMID %s RAINPROB %s" % (
                   self._wind_direction,
                   self._wind_gust_midnight,
                   self._wind_speed,
                   self._temp_min,
                   self._temperature_feels_like_min,
                   self._screen_relative_humidity_midnight,
                   self._precipitation_probability)

        if self._visibility_text is not None:
            text += " VISTEXT %s" % self._visibility_text

        if self._weather_type_text is not None:
            text += " WEATHER %s" % self._weather_type_text

        return text

    def parse_json(self, json_data, data_type, time_period):
        self._type = self.extract_attribute(json_data, '$', data_type, time_period)
        self._wind_direction = self.extract_attribute(json_data, 'D', data_type, time_period)
        self._temperature_feels_like_min = self.extract_attribute(json_data, 'FNm', data_type, time_period)
        self._wind_gust_midnight = self.extract_attribute(json_data, 'Gm', data_type, time_period)
        self._temp_min = self.extract_attribute(json_data, 'Nm', data_type, time_period)
        self._screen_relative_humidity_midnight = self.extract_attribute(json_data, 'Hm', data_type, time_period)
        self._precipitation_probability = self.extract_attribute(json_data, 'PPn', data_type, time_period)
        self._wind_speed = self.extract_attribute(json_data, 'S', data_type, time_period)
        self._visibility_code = self.extract_attribute(json_data, 'V', data_type, time_period)
        if self._visibility_code is not None:
            self._visibility_text = metoffer.VISIBILITY[self._visibility_code]
        self._weather_type_code = self.extract_attribute(json_data, 'W', data_type, time_period)
        if self._weather_type_code is not None:
            self._weather_type_text = metoffer.WEATHER_CODES[int(self._weather_type_code)]


class ThreeHourlyForecastDataPoint(DataPoint):

    def __init__(self):
        self._time = None  # $

        self._weather_type_code = None  # W
        self._weather_type_text = None

        self._temperature = None  # T
        self._temperature_feels_like = None  # F

        self._wind_gust = None  # G
        self._wind_direction = None  # D
        self._wind_direction_full = None
        self._wind_speed = None  # S

        self._visibility_code = None  # V
        self._visibility_text = None

        self._uv_index_max = None  # U
        self._uv_guidance = None

        self._precipitation_probability = None  # Pp
        self._screen_relative_humidity = None  # H

    @property
    def time(self):
        return self._time

    def parse_json(self, json_data, data_type, time_period):
        self._time = self.extract_attribute(json_data, '$', data_type, time_period)
        self._temperature_feels_like = self.extract_attribute(json_data, 'F', data_type, time_period)
        self._wind_gust = self.extract_attribute(json_data, 'G', data_type, time_period)
        self._screen_relative_humidity = self.extract_attribute(json_data, 'H', data_type, time_period)
        self._temperature = self.extract_attribute(json_data, 'T', data_type, time_period)
        self._visibility_code = self.extract_attribute(json_data, 'V', data_type, time_period)
        if self._visibility_code is not None:
            self._visibility_text = metoffer.VISIBILITY[self._visibility_code]
        self._wind_direction = self.extract_attribute(json_data, 'D', data_type, time_period)
        if self._wind_direction is not None:
            self._wind_direction_full = self.direction_to_full_text(self._wind_direction)
        self._wind_speed = self.extract_attribute(json_data, 'S', data_type, time_period)
        self._uv_index_max = self.extract_attribute(json_data, 'U', data_type, time_period)
        if self._uv_index_max is not None:
            self._uv_guidance = metoffer.guidance_UV(int(self._uv_index_max))
        self._weather_type_code = self.extract_attribute(json_data, 'W', data_type, time_period)
        if self._weather_type_code is not None:
            self._weather_type_text = metoffer.WEATHER_CODES[int(self._weather_type_code)]
            self._weather_type_text = self._weather_type_text.replace("(day)", "")
            self._weather_type_text = self._weather_type_text.replace("(night)", "")

        self._precipitation_probability = self.extract_attribute(json_data, 'Pp', data_type, time_period)

    #
    # Matches an AIML Pattern of
    # <pattern></pattern>
    #
    def to_program_y_text(self):
        text = "FORECAST HOURS"

        if self._weather_type_text is not None:
            text += " TYPE %s" % self._weather_type_text

        text += " TEMP %s FEELS %s WINDSPEED %s UVINDEX %s UVGUIDE %s RAINPROB %s HUMIDITY %s" % (
                   self._temperature,
                   self._temperature_feels_like,
                   self._wind_speed,
                   self._uv_index_max,
                   self._uv_guidance,
                   self._precipitation_probability,
                   self._screen_relative_humidity
               )

        if self._wind_direction is not None:
            text += " WINDDIR %s" % self._wind_direction

        if self._wind_direction_full is not None:
            text += " WINDDIRFULL %s" % self._wind_direction_full

        if self._visibility_text is not None:
            text += " VIS %s" % self._visibility_text

        return text


class ObservationDataPoint(DataPoint):

    def __init__(self):
        self._time = None  # $
        self._temperature = None  # T
        self._visibility = None  # V
        self._visibility_text = None
        self._wind_direction = None  # D
        self._wind_direction_full = None
        self._wind_speed = None  # S
        self._weather_type_code = None  # W
        self._weather_type_text = None
        self._pressure = None  # P
        self._pressure_tendancy = None  # Pt
        self._pressure_tendancy_full = None
        self._dew_point = None  # Dp
        self._screen_relative_humidity = None  # H

    @property
    def time(self):
        return self._time

    #
    # Matches an AIML Pattern of
    # <pattern>OBSERVATION TEMP * * * HUMIDITY * * VISIBILITY V * VF * PRESSURE P * PT * PTF * WIND D * DF * S *</pattern>
    #
    def to_program_y_text(self):
        temp = self._temperature.split(".")
        humid = self._screen_relative_humidity.split(".")

        text = "OBSERVATION"
        if self._weather_type_text is not None:
            text += " TYPE %s" % self._weather_type_text

        text += " TEMP %s %s %s" % ("MINUS" if self._temperature.startswith("-") else "PLUS", temp[0], temp[1])

        text += " HUMIDITY %s %s" % (humid[0], humid[1])

        if self._visibility is not None:
            text += " VISIBILITY V %s VF %s" % (self._visibility, self._visibility_text)

        text += " PRESSURE P %s" % self._pressure
        if self._pressure_tendancy is not None:
            text += " PT %s PTF %s" % (self._pressure_tendancy, self._pressure_tendancy_full)

        if self._wind_direction is not None:
            text += " WIND D %s DF %s" % (self._wind_direction, self._wind_direction_full)

        text += " S %s" % self._wind_speed

        return text

    def parse_json(self, json_data, data_type, time_period):
        self._time = self.extract_attribute(json_data, '$', data_type, time_period)
        self._temperature = self.extract_attribute(json_data, 'T', data_type, time_period)
        self._visibility = self.extract_attribute(json_data, 'V', data_type, time_period)
        if self._visibility is not None:
            self._visibility_text = self.parse_visibility_to_text(self._visibility)
        self._wind_direction = self.extract_attribute(json_data, 'D', data_type, time_period)
        if self._wind_direction is not None:
            self._wind_direction_full = self.direction_to_full_text(self._wind_direction)
        self._wind_speed = self.extract_attribute(json_data, 'S', data_type, time_period)
        self._weather_type_code = self.extract_attribute(json_data, 'W', data_type, time_period)
        if self._weather_type_code is not None:
            self._weather_type_text = metoffer.WEATHER_CODES[int(self._weather_type_code)]
        self._pressure = self.extract_attribute(json_data, 'P', data_type, time_period)
        self._pressure_tendancy = self.extract_attribute(json_data, 'Pt', data_type, time_period)
        if self._pressure_tendancy is not None:
            self._pressure_tendancy_full = self.parse_pressure_tendancy(self._pressure_tendancy)
        self._dew_point = self.extract_attribute(json_data, 'Dp', data_type, time_period)
        self._screen_relative_humidity = self.extract_attribute(json_data, 'H', data_type, time_period)

    def parse_visibility_to_text(self, code):
        distance_in_kms = int(code) // 1000
        if distance_in_kms < 1:
            return "Very poor"
        elif distance_in_kms > 0 and distance_in_kms < 4:
            return "Poor"
        elif distance_in_kms > 3 and distance_in_kms < 10:
            return "Moderate"
        elif distance_in_kms > 9 and distance_in_kms < 20:
            return "Good"
        elif distance_in_kms > 19 and distance_in_kms < 40:
            return "Very Good"
        else: # > 39:
            return "Excellent"

    def parse_pressure_tendancy(self, tendancy):
        if tendancy in PRESSURE_TENDANCY:
            return PRESSURE_TENDANCY[tendancy]
        return "Unknown"


class Report:

    def __init__(self, data_type, time_period):
        self._data_type = data_type
        self._time_period = time_period

        self._time_periods = []

        self._type = None
        self._report_date = None

    @property
    def time_period(self):
        return self._time_period

    @property
    def time_periods(self):
        return self._time_periods

    @property
    def type(self):
        return self._type

    @property
    def report_date(self):
        return self._report_date

    def parse_json(self, json_data):
        for element in json_data['Rep']:
            if self._data_type == MetOfficeWeatherReport.OBSERVATION:
                period = ObservationDataPoint()

            elif self._data_type == MetOfficeWeatherReport.FORECAST:
                if self._time_period == metoffer.DAILY:
                    if element['$'] == 'Day':
                        period = DailyForecastDayDataPoint()

                    elif element['$'] == 'Night':
                        period = DailyForecastNightDataPoint()

                    else:
                        raise ValueError("Unknown report type %s" % element['$'])

                elif self._time_period == metoffer.THREE_HOURLY:
                    period = ThreeHourlyForecastDataPoint()

                else:
                    raise ValueError("Unknown time period %s" % self._time_period)

            else:
                raise ValueError("Unknown data type %s" % self._data_type)

            period.parse_json(element, self._data_type, self._time_period)
            self._time_periods.append(period)

        if self._data_type == MetOfficeWeatherReport.OBSERVATION or self._time_period == metoffer.THREE_HOURLY:
            self._time_periods.sort(key=lambda period: int(period.time))

        if 'type' in json_data:
            self._type = json_data['type']
        else:
            raise ValueError("type missing from DV data")

        if 'value' in json_data:
            try:
                self._report_date = datetime.datetime.strptime(json_data['value'], "%Y-%m-%dZ")
            except:
                raise ValueError("Invalid date time format for value in Report data")
        else:
            raise ValueError("value missing from Report data")

    def get_last_time_period(self):
        if self._time_periods:
            return self._time_periods[-1]
        return None

    def get_time_period_by_type(self, period_type):
        if self._time_periods:
            for time_period in self._time_periods:
                if time_period.type == period_type:
                    return time_period
        return None

    def get_time_period_by_time(self, time):
        if self._time_periods:
            for time_period in self._time_periods:
                if time_period.time == time:
                    return time_period
        return None


class Location:

    def __init__(self, data_type, time_period):
        self._data_type = data_type
        self._time_period = time_period
        self._reports = []

        self._continent = None
        self._country = None
        self._elevation = None
        self._i = None
        self._lat = None
        self._lon = None
        self._name = None

    @property
    def time_period(self):
        return self._time_period

    @property
    def data_type(self):
        return self._data_type

    @property
    def reports(self):
        return self._reports

    def get_latest_report(self):
        if self._reports:
            return self._reports[-1]
        return None

    def get_report_for_date(self, report_date):
        if self._reports:
            for report in self._reports:
                if report.report_date == report_date:
                    return report
        return None

    def parse_json(self, json_data):
        for element in json_data['Period']:
            report = Report(self._data_type, self._time_period)
            report.parse_json(element)
            self._reports.append(report)

        # Sort Reports by _report_date which is is either
        # a) The date of the observation
        # b) The date of the daily forecast
        if self._reports:
            self._reports.sort(key=lambda report: report.report_date)

        if 'continent' in json_data:
            self._continent = json_data['continent']
        else:
            raise ValueError("continent missing from Location data")

        if 'country' in json_data:
            self._country = json_data['country']
        else:
            raise ValueError("country missing from Location data")

        if 'elevation' in json_data:
            self._elevation = json_data['elevation']
        else:
            raise ValueError("elevation missing from Location data")

        if 'i' in json_data:
            self._i = json_data['i']
        else:
            raise ValueError("i missing from Location data")

        if 'lat' in json_data:
            self._lat = json_data['lat']
        else:
            raise ValueError("lat missing from Location data")

        if 'lon' in json_data:
            self._lon = json_data['lon']
        else:
            raise ValueError("lon missing from Location data")

        if 'name' in json_data:
            self._name = json_data['name']
        else:
            raise ValueError("name missing from Location data")


class DV:

    def __init__(self, data_type, time_period):
        self._data_type = data_type
        self._time_period = time_period
        self._date = None
        self._type = None
        self._location = None

    @property
    def location(self):
        return self._location

    def parse_json(self, json_data):

        if "Location" not in json_data:
            raise ValueError("Location missing from DV data")
        self._location = Location(self._data_type, self._time_period)
        self._location.parse_json(json_data['Location'])

        if 'dataDate' in json_data:
            try:
                self._date = datetime.datetime.strptime(json_data['dataDate'], "%Y-%m-%dT%H:%M:%SZ")
            except:
                raise ValueError("Invalid date format for dataDate in DV data")
        else:
            raise ValueError("dataDate missing from DV data")

        if 'type' in json_data:
            self._type = json_data['type']
        else:
            raise ValueError("type missing from DV data")


class SiteReport:

    def __init__(self, data_type, time_period):
        self._time_period = time_period
        self._data_type = data_type
        self._dv = None

    @property
    def dv(self):
        return self._dv

    def parse_json(self, json_data):
        if "DV" not in json_data:
            raise ValueError("DV missing from site report data")
        self._dv = DV(self._data_type, self._time_period)
        self._dv.parse_json(json_data['DV'])


class MetOfficeWeatherReport:
    FORECAST = 1
    OBSERVATION = 2

    def __init__(self, data_type, time_period=0):
        self._data_type = data_type
        self._time_period = time_period
        self._site_report = None
        self._time_periods = {}

    def parse_json(self, json_data):
        if "SiteRep" not in json_data:
            raise ValueError("SiteRep missing from weather report")
        else:
            self._site_report = SiteReport(self._data_type, self._time_period)
            self._site_report.parse_json(json_data["SiteRep"])

        self.cache_time_periods()

    def cache_time_periods(self):
        pass                        # pragam: no cover


class MetOfficeObservation(MetOfficeWeatherReport):

    def __init__(self):
        MetOfficeWeatherReport.__init__(self, MetOfficeWeatherReport.OBSERVATION)

    def cache_time_periods(self):
        self._time_periods.clear()
        for report in self._site_report.dv.location.reports:
            for time_period in report.time_periods:
                fulltime = report.report_date + datetime.timedelta(minutes=int(time_period.time))
                self._time_periods[fulltime] = time_period

    def get_observations(self):
        return self._time_periods

    def get_latest_observation(self):
        items = list(self._time_periods.items())
        return items[-1][1]

    def get_last_n_observations(self, n):
        return list(self._time_periods.items())[-n:]


class MetOfficeForecast(MetOfficeWeatherReport):

    def __init__(self, time_period):
        MetOfficeWeatherReport.__init__(self, MetOfficeWeatherReport.FORECAST, time_period)

    def get_forecasts(self):
        return self._time_periods

    def get_latest_forecast(self):
        items = list(self._time_periods.items())
        return items[-1][1]


class MetOffice5DayForecast(MetOfficeForecast):

    def __init__(self):
        MetOfficeForecast.__init__(self, metoffer.DAILY)

    def cache_time_periods(self):
        self._time_periods.clear()
        for report in self._site_report.dv.location.reports:
            daytime = report.report_date + datetime.timedelta(hours=6)
            self._time_periods[daytime] = report.time_periods[0]
            nighttime = report.report_date + datetime.timedelta(hours=18)
            self._time_periods[nighttime] = report.time_periods[1]

    def _calc_date_n_days_ahead(self, days, fromdate=None):
        if fromdate is None:
            return datetime.datetime.now() + datetime.timedelta(days=days)
        else:
            return datetime.datetime.strptime(fromdate, '%Y-%m-%dZ') + datetime.timedelta(days=days)

    def get_forecast_for_n_days_ahead(self, days, fromdate=None):
        search_date = self._calc_date_n_days_ahead(days, fromdate=fromdate)

        for day_forecast in self._time_periods.keys():
            if day_forecast > search_date:
                return self._time_periods[day_forecast].to_program_y_text()

        return None


class MetOffice24HourForecast(MetOfficeForecast):

    def __init__(self):
        MetOfficeForecast.__init__(self, metoffer.THREE_HOURLY)

    def cache_time_periods(self):
        self._time_periods.clear()
        for report in self._site_report.dv.location.reports:
            for time_period in report.time_periods:
                period_datetime = report.report_date + datetime.timedelta(minutes=int(time_period.time))
                self._time_periods[period_datetime] = time_period

    def _calc_date_n_hours_ahead(self, hours, fromdate=None):
        if fromdate is None:
            return datetime.datetime.now() + datetime.timedelta(hours=hours)
        else:
            return datetime.datetime.strptime(fromdate,  "%Y-%m-%dZ") + datetime.timedelta(hours=hours)

    def get_forecast_for_n_hours_ahead(self, hours, fromdate=None):
        search_date = self._calc_date_n_hours_ahead(hours, fromdate=fromdate)

        for hour_forecast in self._time_periods.keys():
            if hour_forecast > search_date:
                return self._time_periods[hour_forecast].to_program_y_text()

        return None


class MetOffice:

    def __init__(self, api_key):
        self._met_office_api = metoffer.MetOffer(api_key)

    def get_forecast_data(self, lat, lon, forecast_type):
        return self._met_office_api.nearest_loc_forecast(lat, lon, forecast_type)       # pragma: no cover

    def get_observation_data(self, lat, lng):
        return self._met_office_api.nearest_loc_obs(lat, lng)                           # pragma: no cover

    def nearest_location_forecast(self, lat, lng, forecast_type):
        json_data = self.get_forecast_data(lat, lng, forecast_type)
        return json_data

    @staticmethod
    def parse_forecast(json_data, forecast_type):
        if forecast_type == metoffer.THREE_HOURLY:
            forecast = MetOffice24HourForecast()

        elif forecast_type == metoffer.DAILY:
            forecast = MetOffice5DayForecast()

        else:
            raise ValueError("Unsupported forecast_type: [%s]" % forecast_type)

        forecast.parse_json(json_data)
        return forecast

    def twentyfour_hour_forecast(self, lat, lng):
        return self.nearest_location_forecast(lat, lng, metoffer.THREE_HOURLY)

    def five_day_forecast(self, lat, lng):
        return self.nearest_location_forecast(lat, lng, metoffer.DAILY)

    @staticmethod
    def parse_observation(json_data):
        report = MetOfficeObservation()
        report.parse_json(json_data)
        return report

    def nearest_location_observation(self, lat, lng):
        json_data = self.get_observation_data(lat, lng)
        return json_data

    def current_observation(self, lat, lng):
        return self.nearest_location_observation(lat, lng)
