"""
Copyright (c) 2016 Keith Sterling

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
import json
import logging
import os

import metoffer

DIRECTIONS = { 'N':     'North',
               'NNE':   'North North East',
               'NE':    'North East',
               'ENE':   'East North East',
               'E':     'East',
               'ESE':   'East South East',
               'SE':    'South East',
               'ESE':   'SouthSouth East',
               'S':     'South',
               'SSW':   'South South West',
               'SW':    'South West',
               'WSW':   'West South West',
               'W':     'West',
               'WNW':   'West North West',
               'NW':    'North West',
               'NNW':   'North North West',
               }

PRESSURE_TENDANCY = { 'F': "Falling",
                      'R': 'Rising'}

class DataPoint(object):

    def extract_attribute(self, json, name, data_type, time_period):
        if name in json:
            return json[name]
        else:
            if data_type == MetOfficeWeatherReport.ObservationDataPoint:
                logging.warning('%s attribute missing from ObservationDataPoint data point'%name)
            elif data_type == MetOfficeWeatherReport.FORECAST:
                if time_period == metoffer.THREE_HOURLY:
                    logging.warning('%s attribute missing from three hourly forecast data point'%name)
                if time_period == metoffer.DAILY:
                    logging.warning('%s attribute missing from daily forecast data point' % name)
            return None

    def direction_to_full_text(self, direction):
        if direction in DIRECTIONS:
            return DIRECTIONS[direction]
        else:
            return "Unknown"

class DailyForecastDayDataPoint(DataPoint):
    def __int__(self):
        self._type                                      # $
        self._wind_direction = None                     # D
        self._temp_max = None                           # Dm
        self._temperature_feels_like_max = None         # FDm
        self._wind_gust_noon = None                     # Gn
        self._screen_relative_humidity_noon = None      # Hn
        self._precipitation_probability                 # PPd
        self._wind_speed = None                         # S
        self._uv_index_max = None                       # U
        self._uv_guidance = None
        self._visibility_code                           # V
        self._visibility_text = None
        self._weather_type_code = None                  # W
        self._weather_type_text = None

    #
    # Matches an AIML Pattern of
    # <pattern></pattern>
    #
    def to_program_y_text(self):
        return "WEATHER %s"%(
            self._weather_type_text
        )

    def parse_json(self, json, data_type, time_period):
        self._type = self.extract_attribute(json, '$', data_type, time_period)
        self._wind_direction = self.extract_attribute(json, 'D', data_type, time_period)
        self._temp_max = self.extract_attribute(json, 'Dm', data_type, time_period)
        self._temperature_feels_like_max = self.extract_attribute(json, 'FDm', data_type, time_period)
        self._wind_gust_noon = self.extract_attribute(json, 'Gn', data_type, time_period)
        self._screen_relative_humidity_noon = self.extract_attribute(json, 'Hn', data_type, time_period)
        self._precipitation_probability = self.extract_attribute(json, 'PPd', data_type, time_period)
        self._wind_speed = self.extract_attribute(json, 'S', data_type, time_period)
        self._uv_index_max = self.extract_attribute(json, 'U', data_type, time_period)
        if self._uv_index_max is not None:
            self._uv_guidance = metoffer.guidance_UV(int(self._uv_index_max))
        self._visibility_code = self.extract_attribute(json, 'V', data_type, time_period)
        if self._visibility_code is not None:
            self._visibility_text = metoffer.VISIBILITY[self._visibility_code]
        self._weather_type_code = self.extract_attribute(json, 'W', data_type, time_period)
        if self._weather_type_code is not None:
            self._weather_type_text = metoffer.WEATHER_CODES[int(self._weather_type_code)]

class DailyForecastNightDataPoint(DataPoint):
    def __int__(self):
        self._type                                      # $
        self._wind_direction = None                     # D
        self._temperature_feels_like_min = None         # FNm
        self._wind_gust_midnight = None                 # Gm
        self._screen_relative_humidity_midnight = None  # Hm
        self._temp_min = None                           # Nm
        self._precipitation_probability                 # PPn
        self._wind_speed = None                         # S
        self._visibility_code                           # V
        self._visibility_text = None
        self._weather_type_code = None                  # W
        self._weather_type_text = None

    #
    # Matches an AIML Pattern of
    # <pattern></pattern>
    #
    def to_program_y_text(self):
        return "WEATHER %s"%(
            self._weather_type_text
        )

    def parse_json(self, json, data_type, time_period):
        self._type = self.extract_attribute(json, '$', data_type, time_period)
        self._wind_direction = self.extract_attribute(json, 'D', data_type, time_period)
        self._temperature_feels_like_min = self.extract_attribute(json, 'FNm', data_type, time_period)
        self._wind_gust_midnight = self.extract_attribute(json, 'Gm', data_type, time_period)
        self._temp__min = self.extract_attribute(json, 'Nm', data_type, time_period)
        self._screen_relative_humidity_midnight = self.extract_attribute(json, 'Hm', data_type, time_period)
        self._precipitation_probability = self.extract_attribute(json, 'PPn', data_type, time_period)
        self._wind_speed = self.extract_attribute(json, 'S', data_type, time_period)
        self._visibility_code = self.extract_attribute(json, 'V', data_type, time_period)
        if self._visibility_code is not None:
            self._visibility_text = metoffer.VISIBILITY[self._visibility_code]
        self._weather_type_code = self.extract_attribute(json, 'W', data_type, time_period)
        if self._weather_type_code is not None:
            self._weather_type_text = metoffer.WEATHER_CODES[int(self._weather_type_code)]

class ThreeHourlyForecastDataPoint(DataPoint):
    def __int__(self):
        self._time = None                       # $

        self._weather_type_code = None          # W
        self._weather_type_text = None      

        self._temperature = None                # T
        self._temperature_feels_like = None     # F

        self._wind_gust = None                  # G
        self._wind_direction = None             # D
        self._wind_direction_full = None
        self._wind_speed = None                 # S

        self._visibility_code = None            # V
        self._visibility_text = None

        self._uv_index_max = None               # U
        self._uv_guidance = None

        self._precipitation_probability = None  # Pp
        self._screen_relative_humidity = None   # H

    def parse_json(self, json, data_type, time_period):
        self._time = self.extract_attribute(json, '$', data_type, time_period)
        self._temperature_feels_like = self.extract_attribute(json, 'F', data_type, time_period)
        self._wind_gust = self.extract_attribute(json, 'G', data_type, time_period)
        self._screen_relative_humidity = self.extract_attribute(json, 'H', data_type, time_period)
        self._temperature = self.extract_attribute(json, 'T', data_type, time_period)
        self._visibility_code = self.extract_attribute(json, 'V', data_type, time_period)
        if self._visibility_code is not None:
            self._visibility_text = metoffer.VISIBILITY[self._visibility_code]
        self._wind_direction = self.extract_attribute(json, 'D', data_type, time_period)
        if self._wind_direction is not None:
            self._wind_direction_full = self.direction_to_full_text(self._wind_direction)
        self._wind_speed = self.extract_attribute(json, 'S', data_type, time_period)
        self._uv_index_max = self.extract_attribute(json, 'U', data_type, time_period)
        if self._uv_index_max is not None:
            self._uv_guidance = metoffer.guidance_UV(int(self._uv_index_max))
        self._weather_type_code = self.extract_attribute(json, 'W', data_type, time_period)
        if self._weather_type_code is not None:
            self._weather_type_text = metoffer.WEATHER_CODES[int(self._weather_type_code)]
            self._weather_type_text = self._weather_type_text.replace("(day)", "")
            self._weather_type_text = self._weather_type_text.replace("(night)", "")

        self._precipitation_probability = self.extract_attribute(json, 'Pp', data_type, time_period)

    #
    # Matches an AIML Pattern of
    # <pattern></pattern>
    #
    def to_program_y_text(self):
        return "WEATHER %s TEMP % TF %s WIND D %s F %s S %s VISIBILITY %s UV I %s G %s RAIN %s HUMIDITY %s"%(
            self._weather_type_text,
            self._temperature, self._temperature_feels_like,
            self._wind_direction, self._wind_direction_full, self._wind_speed,
            self._visibility_text,
            self._uv_index_max, self._uv_guidance,
            self._precipitation_probability,
            self._screen_relative_humidity
        )

class ObservationDataPoint(DataPoint):
    def __init__(self):
        self._time = None                       # $
        self._temperature = None                # T
        self._visibility = None                 # V
        self._visibility_text = None
        self._wind_direction = None             # D
        self._wind_direction_full = None
        self._wind_speed = None                 # S
        self._weather_type_code = None          # W
        self._weather_type_text = None
        self._pressure = None                   # P
        self._pressure_tendancy = None          # Pt
        self._pressure_tendancy_full = None
        self._dew_point = None                  # Dp
        self._screen_relative_humidity = None   # H

    #
    # Matches an AIML Pattern of
    # <pattern>TEMP * VISIBILITY C * T * WIND D * DF * S * WEATHER * PRESSURE * T * TF * HUMIDITY *</pattern>
    #
    def to_program_y_text(self):
        temp = self._temperature.split(".")
        humid = self._screen_relative_humidity.split(".")

        return "WEATHER %s TEMP %s %s VISIBILITY V %s VF %s WIND D %s DF %s S %s PRESSURE P %s PT %s PTF %s HUMIDITY %s %s"%(
            self._weather_type_text,
            temp[0], temp[1],
            self._visibility, self._visibility_text,
            self._wind_direction, self._wind_direction_full, self._wind_speed,
            self._pressure, self._pressure_tendancy, self._pressure_tendancy_full,
            humid[0], humid[1]
        )

    def parse_json(self, json, data_type, time_period):
        self._time = self.extract_attribute(json, '$', data_type, time_period)
        self._temperature = self.extract_attribute(json, 'T', data_type, time_period)
        self._visibility = self.extract_attribute(json, 'V', data_type, time_period)
        if self._visibility is not None:
            self._visibility_text = self.parse_visibility_to_text(self._visibility)
        self._wind_direction = self.extract_attribute(json, 'D', data_type, time_period)
        if self._wind_direction is not None:
            self._wind_direction_full = self.direction_to_full_text(self._wind_direction)
        self._wind_speed = self.extract_attribute(json, 'S', data_type, time_period)
        self._weather_type_code = self.extract_attribute(json, 'W', data_type, time_period)
        if self._weather_type_code is not None:
            self._weather_type_text = metoffer.WEATHER_CODES[int(self._weather_type_code)]
        self._pressure = self.extract_attribute(json, 'P', data_type, time_period)
        self._pressure_tendancy = self.extract_attribute(json, 'Pt', data_type, time_period)
        if self._pressure_tendancy is not None:
            self._pressure_tendancy_full = self.parse_pressure_tendancy(self._pressure_tendancy)
        self._dew_point = self.extract_attribute(json, 'Dp', data_type, time_period)
        self._screen_relative_humidity = self.extract_attribute(json, 'H', data_type, time_period)

    def parse_visibility_to_text(self, code):
        distance_in_kms = int(code)/1000
        if distance_in_kms < 1:
            return "Very poor"
        if distance_in_kms >= 1 and distance_in_kms < 4:
            return "Poor"
        if distance_in_kms >= 4 and distance_in_kms < 10:
            return "Moderate"
        if distance_in_kms >= 10 and distance_in_kms < 20:
            return "Good"
        if distance_in_kms >= 20 and distance_in_kms < 40:
            return "Very Good"
        if distance_in_kms >= 40:
            return "Excellent"

    def parse_pressure_tendancy(self, tendancy):
        if tendancy in PRESSURE_TENDANCY:
            return PRESSURE_TENDANCY[tendancy]
        else:
            return "Unknown"

class Report(object):
    def __init__(self, data_type, time_period):
        self._data_type = data_type
        self._time_period = time_period

        self._time_periods = []

        self._type = None
        self._report_date = None

    def parse_json(self, json):
        for element in json['Rep']:
            if self._data_type == MetOfficeWeatherReport.ObservationDataPoint:
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
                    raise ValueError("Unknown time period %s"%self._time_period)
            else:
                raise ValueError("Unknown data type %s"%self._data_type)

            period.parse_json(element, self._data_type, self._time_period)
            self._time_periods.append(period)

        if self._data_type == MetOfficeWeatherReport.ObservationDataPoint or self._time_period == metoffer.THREE_HOURLY:
            if len(self._time_periods) > 0:
                self._time_periods.sort(key=lambda period: int(period._time))

        if 'type' in json:
            self._type = json['type']
        else:
            raise ValueError("type missing from DV data")

        if 'value' in json:
            try:
                self._report_date = datetime.datetime.strptime(json['value'], "%Y-%m-%dZ")
            except:
                raise ValueError("Invalid date time format for value in Report data")
        else:
            raise ValueError("value missing from Report data")

    def get_last_time_period(self):
        if len(self._time_periods) > 0:
            return self._time_periods[-1]
        return None

    def get_time_period_by_type(self, type):
        if len(self._time_periods) > 0:
            for time_period in self._time_periods:
                if time_period._type == type:
                    return time_period
        return None

    def get_time_period_by_time(self, time):
        if len(self._time_periods) > 0:
            for time_period in self._time_periods:
                if time_period._time == time:
                    return time_period
        return None


class Location(object):
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

    def get_latest_report(self):
        if len(self._reports) > 0:
            return self._reports[-1]
        return None

    def get_report_for_date(self, report_date):
        if len(self._reports) > 0:
            for report in self._reports:
                if report._report_date == report_date:
                    return report
        return None

    def parse_jason(self, json):
        for element in json['Period']:
            report = Report(self._data_type, self._time_period)
            report.parse_json(element)
            self._reports.append(report)

        # Sort Reports by _report_date which is is either
        # a) The date of the observation
        # b) The date of the daily forecast
        if len(self._reports) > 0:
            self._reports.sort(key=lambda report: report._report_date)

        if 'continent' in json:
            self._continent = json['continent']
        else:
            raise ValueError("continent missing from Location data")

        if 'country' in json:
            self._country = json['country']
        else:
            raise ValueError("country missing from Location data")

        if 'elevation' in json:
            self._elevation = json['elevation']
        else:
            raise ValueError("elevation missing from Location data")

        if 'i' in json:
            self._i = json['i']
        else:
            raise ValueError("i missing from Location data")

        if 'lat' in json:
            self._lat = json['lat']
        else:
            raise ValueError("lat missing from Location data")

        if 'lon' in json:
            self._lon = json['lon']
        else:
            raise ValueError("lon missing from Location data")

        if 'name' in json:
            self._name = json['name']
        else:
            raise ValueError("name missing from Location data")

class DV(object):
    def __init__(self, data_type, time_period):
        self._data_type = data_type
        self._time_period = time_period
        self._date = None
        self._type = None
        self._location = None

    def parse_jason(self, json):

        if "Location" not in json:
            raise ValueError("Location missing from DV data")
        self._location = Location(self._data_type, self._time_period)
        self._location.parse_jason(json['Location'])

        if 'dataDate' in json:
            try:
                self._date = datetime.datetime.strptime(json['dataDate'], "%Y-%m-%dT%H:%M:%SZ")
            except:
                raise ValueError("dataDate missing from DV data")

        if 'type' in json:
            self._type = json['type']
        else:
            raise ValueError("type missing from DV data")

class SiteReport(object):
    def __init__(self, data_type, time_period):
        self._time_period = time_period
        self._data_type = data_type
        self._dv = None

    def parse_json(self, json):
        if "DV" not in json:
            raise ValueError("DV missing from site report data")
        self._dv = DV(self._data_type, self._time_period)
        self._dv.parse_jason(json['DV'])

class MetOfficeWeatherReport(object):

    FORECAST = 1
    ObservationDataPoint = 2

    def __init__(self, data_type, time_period=0):
        self._data_type = data_type
        self._time_period = time_period
        self._site_report = None

    def parse_json(self, json):
        if "SiteRep" not in json:
            raise ValueError("SiteRep missing from weather report")
        else:
            self._site_report = SiteReport(self._data_type, self._time_period)
            self._site_report.parse_json(json["SiteRep" ])

    def get_latest_report(self):
        return self._site_report._dv._location.get_latest_report()

    def get_latest(self):
        return self.get_latest_report().get_last_time_period()

    def get_report_for_date(self, report_date):
        return self._site_report._dv._location.get_report_for_date(report_date)


class MetOffice(object):

    def __init__(self, license_keys):

        self.current_observation_response_file = None
        self.three_hourly_forecast_response_file = None
        self.daily_forecast_response_file = None

        if license_keys.has_key('METOFFICE_API_KEY'):
            api_key = license_keys.get_key('METOFFICE_API_KEY')
        else:
            raise Exception ("No valid license key METOFFICE_API_KEY found")

        if license_keys.has_key('CURRENT_OBSERVATION_RESPONSE_FILE'):
            self.current_observation_response_file = license_keys.get_key('CURRENT_OBSERVATION_RESPONSE_FILE')
        if license_keys.has_key('THREE_HOURLY_FORECAST_RESPONSE_FILE'):
            self.three_hourly_forecast_response_file = license_keys.get_key('THREE_HOURLY_FORECAST_RESPONSE_FILE')
        if license_keys.has_key('DAILY_FORECAST_RESPONSE_FILE'):
            self.daily_forecast_response_file = license_keys.get_key('DAILY_FORECAST_RESPONSE_FILE')

        self._met_office_api = metoffer.MetOffer(api_key)

    def set_current_observation_response_file(self, filename):
        self.current_observation_response_file = filename

    def set_three_hourly_forecast_response_file(self, filename):
        self.three_hourly_forecast_response_file = filename

    def set_daily_forecast_response_file(self, filename):
        self.daily_forecast_response_file = filename

    def nearest_location_forecast(self, lat, lon, type):
        if type == metoffer.THREE_HOURLY and self.three_hourly_forecast_response_file is not None:
            json_data = self.load_datapoints_from_file(self.three_hourly_forecast_response_file)
        elif type == metoffer.DAILY and self.daily_forecast_response_file is not None:
            json_data = self.load_datapoints_from_file(self.daily_forecast_response_file)
        else:
            json_data = self._met_office_api.nearest_loc_forecast(lat, lon, type)
        forecast = MetOfficeWeatherReport(MetOfficeWeatherReport.FORECAST, type)
        forecast.parse_json(json_data)
        return forecast

    def nearest_location_forecast_to_file(self, lat, lon, type, filename):
        json_data = self._met_office_api.nearest_loc_forecast(lat, lon, type)
        self.write_datapoints_to_file(json_data, filename)
        forecast = MetOfficeWeatherReport(MetOfficeWeatherReport.FORECAST, type)
        forecast.parse_json(json_data)
        return forecast

    def nearest_location_forecast_from_file(self, type, filename):
        json_data = self.load_datapoints_from_file(filename)
        return self.nearest_location_forecast_from_json(type, json_data)

    def nearest_location_forecast_from_json(self, type, json_data):
        forecast = MetOfficeWeatherReport(MetOfficeWeatherReport.FORECAST, type)
        forecast.parse_json(json_data)
        return forecast

    def nearest_location_observation(self, lat, lon):
        if self.current_observation_response_file is None:
            json_data = self._met_office_api.nearest_loc_obs(lat, lon)
        else:
            json_data = self.load_datapoints_from_file(self.current_observation_response_file)
        ObservationDataPoint = MetOfficeWeatherReport(MetOfficeWeatherReport.ObservationDataPoint)
        ObservationDataPoint.parse_json(json_data)
        return ObservationDataPoint

    def nearest_location_observation_to_file(self, lat, lon, filename):
        json_data = self._met_office_api.nearest_loc_obs(lat, lon)
        self.write_datapoints_to_file(json_data, filename)

    def nearest_location_observation_from_file(self, filename):
        json_data = self.load_datapoints_from_file(filename)
        return self.nearest_location_observation_from_json(json_data)

    def nearest_location_observation_from_json(self, json_data):
        ObservationDataPoint = MetOfficeWeatherReport(MetOfficeWeatherReport.ObservationDataPoint)
        ObservationDataPoint.parse_json(json_data)
        return ObservationDataPoint

    def daily_forecast(self, lat, lon):
        return self.nearest_location_forecast(lat, lon, metoffer.DAILY)

    def three_hourly_forecast(self, lat, lon):
        return self.nearest_location_forecast(lat, lon, metoffer.THREE_HOURLY)

    def current_observation(self, lat, lon):
        return self.nearest_location_observation(lat, lon)

    def write_datapoints_to_file(self, datapoints, filename):
        with open(filename, "w+") as data_file:
            json.dump(datapoints, data_file, sort_keys=True, indent=2)

    def load_datapoints_from_file(self, filename):
        with open(filename, 'r+') as json_data_file:
            json_data = json.load(json_data_file)
            return json_data

if __name__ == '__main__':

    # Only to be used to create test data for unit aiml_tests

    from programy.utils.license.keys import LicenseKeys

    license_keys = LicenseKeys()
    license_keys.load_license_key_file(os.path.dirname(__file__) + '/../../../../bots/y-bot/config/license.keys')

    met_office = MetOffice(license_keys)

    lat = 56.0720397
    lng = -3.1752001

    log_to_file = False

    if log_to_file is True:
        met_office.nearest_location_observation_to_file(lat, lng, "observation.json")
        met_office.nearest_location_forecast_to_file(lat, lng, metoffer.DAILY, "forecast_daily.json")
        met_office.nearest_location_forecast_to_file(lat, lng, metoffer.THREE_HOURLY, "forecast_threehourly.json")
    else:
        met_office.nearest_location_observation(lat, lng)
        met_office.nearest_location_forecast(lat, lng, metoffer.DAILY)
        met_office.nearest_location_forecast(lat, lng, metoffer.THREE_HOURLY)

    # Only to be used to create test data for unit aiml_tests

