#!/usr/bin/env python
"""
metoffer

Wrapper for MetOffice DataPoint API
<http://www.metoffice.gov.uk/datapoint>.

The UK's Met Office collects a great deal of meteorological
information which it makes available through its website.
It also offers forecast information.  These data are available
through their API to anyone who has signed up to receive a
'key'.   metoffer offers the ability to retrieve and browse
this data in a handy Python format.

                        *    *    *

Copyright 2012-2014 Stephen B Murray

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
__version__ = "1.3.2"
__author__ = "Stephen B Murray <sbm199@gmail.com>"

import datetime
import json
import operator
try:
    import urllib.request as url_lib
except ImportError:
    import urllib2 as url_lib

HOST = "http://datapoint.metoffice.gov.uk/public/data"

# Data categories
VAL = "val"             # Location-specific data
TEXT = "txt"            # Textual data
IMAGE = "image"         # Stand-alone imagery
LAYER = "layer"         # Map overlay imagery

# Resource type: forecast or observation
FORECAST = "wxfcs"
OBSERVATIONS = "wxobs"

# Field
ALL = "all"             # Can also be used instead of a location ID
# For textual data only:
UK_EXTREMES = "ukextremes"
NATIONAL_PARK = "nationalpark"
REGIONAL_FORECAST = "regionalforecast"
MOUNTAIN_AREA = "mountainarea"
# For stand-alone image only:
SURFACE_PRESSURE = "surfacepressure"

DATA_TYPE = "json"      # Easier to work with than the XML alternative

# Requests
SITELIST = "sitelist"
CAPABILITIES = "capabilities"
LATEST = "latest"       # For textual data only

# Time steps
DAILY = "daily"
THREE_HOURLY = "3hourly"
HOURLY = "hourly"

# Some Met Office constants to aid interpretation of data
WEATHER_CODES = {"NA": "Not available",
                 0: "Clear night",
                 1: "Sunny day",
                 2: "Partly cloudy (night)",
                 3: "Partly cloudy (day)",
                 4: "Not used",
                 5: "Mist",
                 6: "Fog",
                 7: "Cloudy",
                 8: "Overcast",
                 9: "Light rain shower (night)",
                 10: "Light rain shower (day)",
                 11: "Drizzle",
                 12: "Light rain",
                 13: "Heavy rain shower (night)",
                 14: "Heavy rain shower (day)",
                 15: "Heavy rain",
                 16: "Sleet shower (night)",
                 17: "Sleet shower (day)",
                 18: "Sleet",
                 19: "Hail shower (night)",
                 20: "Hail shower (day)",
                 21: "Hail",
                 22: "Light snow shower (night)",
                 23: "Light snow shower (day)",
                 24: "Light snow",
                 25: "Heavy snow shower (night)",
                 26: "Heavy snow shower (day)",
                 27: "Heavy snow",
                 28: "Thunder shower (night)",
                 29: "Thunder shower (day)",
                 30: "Thunder"}
VISIBILITY = {"UN": "Unknown",
              "VP": "Very poor - Less than 1 km",
              "PO": "Poor - Between 1-4 km",
              "MO": "Moderate - Between 4-10 km",
              "GO": "Good - Between 10-20 km",
              "VG": "Very good - Between 20-40 km",
              "EX": "Excellent - More than 40 km"}
REGIONS = {"os": "Orkney and Shetland",
           "he": "Highland and Eilean Siar",
           "gr": "Grampian",
           "ta": "Tayside",
           "st": "Strathclyde",
           "dg": "Dumfries, Galloway, Lothian",
           "ni": "Northern Ireland",
           "yh": "Yorkshire and the Humber",
           "ne": "Northeast England",
           "em": "East Midlands",
           "ee": "East of England",
           "se": "London and Southeast England",
           "nw": "Northwest England",
           "wm": "West Midlands",
           "sw": "Southwest England",
           "wl": "Wales",
           "uk": "United Kingdom"}

def guidance_UV(index):
    """Return Met Office guidance regarding UV exposure based on UV index"""
    if 0 < index < 3:
        guidance = "Low exposure. No protection required. You can safely stay outside"
    elif 2 < index < 6:
        guidance = "Moderate exposure. Seek shade during midday hours, cover up and wear sunscreen"
    elif 5 < index < 8:
        guidance = "High exposure. Seek shade during midday hours, cover up and wear sunscreen"
    elif 7 < index < 11:
        guidance = "Very high. Avoid being outside during midday hours. Shirt, sunscreen and hat are essential"
    elif index > 10:
        guidance = "Extreme. Avoid being outside during midday hours. Shirt, sunscreen and hat essential."
    else:
        guidance = None
    return guidance

class MetOffer():
    def __init__(self, key):
        self.key = key

    def _query(self, data_category, resource_category, field, request, step, isotime=None):
        """
        Request and return data from DataPoint RESTful API.
        """
        rest_url = "/".join([HOST, data_category, resource_category, field, DATA_TYPE, request])
        query_string = "?" + "&".join(["res=" + step, "time=" + isotime if isotime is not None else "", "key=" + self.key])
        url = rest_url + query_string
        page = url_lib.urlopen(url)
        pg = page.read()
        return pg
    
    def loc_forecast(self, request, step, isotime=None):
        """
        Return location-specific forecast data (including lists of available
        sites and time capabilities) for given time step.
        
        request:
            metoffer.SITELIST        Returns available sites
            metoffer.CAPABILITIES    Returns available times
            site ID, e.g. "3021"     Returns forecast data for site
            metoffer.ALL             Returns forecast data for ALL sites
        step:
            ""                       Step not required with SITELIST
                                     or CAPABILITIES
            metoffer.DAILY           Returns daily forecasts
            metoffer.THREE_HOURLY    Returns forecast for every three hours
        isotime:
            An ISO 8601 formatted datetime as string
                                     Returns only data for this time step.
                                     Possible time steps may be obtained
                                     through metoffer.CAPABILITIES
        """
        return json.loads(self._query(VAL, FORECAST, ALL, request, step, isotime).decode(errors="replace"))

    def nearest_loc_forecast(self, lat, lon, step):
        """
        Work out nearest possible site to lat & lon coordinates
        and return its forecast data for the given time step.
        
        lat:                        float or int.  Latitude.
        lon:                        float or int.  Longitude.
        step:
            metoffer.DAILY          Returns daily forecasts
            metoffer.THREE_HOURLY   Returns forecast for every three hours
        """
        sitelist = self.loc_forecast(SITELIST, step)
        sites = parse_sitelist(sitelist)
        site = get_nearest_site(sites, lat, lon)
        return self.loc_forecast(site, step)
        

    def loc_observations(self, request):
        """
        Return location-specific observation data, including a list of sites
        (time step will be HOURLY).
        
        request: 
            metoffer.SITELIST        Returns available sites
            metoffer.CAPABILITIES    Returns available times
            site ID, e.g. "3021"     Returns observation data for site
            metoffer.ALL             Returns observation data for ALL sites
        """
        return json.loads(self._query(VAL, OBSERVATIONS, ALL, request, HOURLY).decode(errors="replace"))

    def nearest_loc_obs(self, lat, lon):
        """
        Work out nearest possible site to lat & lon coordinates
        and return observation data for it.
        
        lat:    float or int.  Latitude.
        lon:    float or int.  Longitude.
        """
        sitelist = self.loc_observations(SITELIST)
        sites = parse_sitelist(sitelist)
        site = get_nearest_site(sites, lat, lon)
        return self.loc_observations(site)

    def text_forecast(self, field, request):
        """
        Return textual forecast data for regions, national parks or mountain
        areas.
        
        field:
            metoffer.NATIONAL_PARK           Data on national parks
            metoffer.REGIONAL_FORECAST       Regional data (see REGIONS)
            metoffer.MOUNTAIN_AREA           Data on mountain areas
        request:
            metoffer.SITELIST                Returns available sites
            metoffer.CAPABILITIES            Returns available times
            site ID, e.g. "3021"             Returns forecast data for site
            Can also use metoffer.ALL to return data for ALL sites,
                but ONLY when field=metoffer.NATIONAL_PARK
        """
        if request == ALL and field != NATIONAL_PARK: # "All" locations only for use with national parks
            raise TypeError
        return json.loads(self._query(TEXT, FORECAST, field, request, "").decode(errors="replace"))

    def text_uk_extremes(self, request):
        """
        Return textual data of UK extremes.
        
        request:
            metoffer.CAPABILITIES            Returns available extreme date
                                             and issue time
            metoffer.LATEST                  Returns data of latest extremes
                                             for all regions
        """
        return json.loads(self._query(TEXT, OBSERVATIONS, UK_EXTREMES, request, "").decode(errors="replace"))

    def stand_alone_imagery(self):
        """
        Returns capabilities data for stand alone imagery and includes
        URIs for the images.
        """
        return json.loads(self._query(IMAGE, FORECAST, SURFACE_PRESSURE, CAPABILITIES, "").decode(errors="replace"))

    def map_overlay_forecast(self):
        """Returns capabilities data for forecast map overlays."""
        return json.loads(self._query(LAYER, FORECAST, ALL, CAPABILITIES, "").decode(errors="replace"))

    def map_overlay_obs(self):
        """Returns capabilities data for observation map overlays."""
        return json.loads(self._query(LAYER, OBSERVATIONS, ALL, CAPABILITIES, "").decode(errors="replace"))

class Site():
    """
    Describes object to hold site metadata.  Also describes method
    to return a Site instance's 'distance' from any given lat & lon
    coordinates.  This 'distance' is a value which is used to guide
    MetOffer.nearest_loc_forecast and MetOffer.nearest_loc_obs.  It
    simply calculates the difference between the two sets of coord-
    inates and arrives at a value through Pythagorean theorem.
    """
    def __init__(self, ident, name, lat=None, lon=None):
        self.ident = ident
        self.name = name
        self.lat = lat
        self.lon = lon
    def distance_to_coords(self, lat_a, lon_a):
        self.distance = (abs(self.lat - lat_a) ** 2) + (abs(self.lon - lon_a) ** 2) ** .5

def parse_sitelist(sitelist):
    """Return list of Site instances from retrieved sitelist data"""
    sites = []
    for site in sitelist["Locations"]["Location"]:
        try:
            ident = site["id"]
            name = site["name"]
        except KeyError:
            ident = site["@id"] # Difference between loc-spec and text for some reason
            name = site["@name"]
        if "latitude" in site:
            lat = float(site["latitude"])
            lon = float(site["longitude"])
        else:
            lat = lon = None
        s = Site(ident, name, lat, lon)
        sites.append(s)
    return sites

def get_nearest_site(sites, lat, lon):
    """
    Return a string which can be used as "request" in calls to loc_forecast
    and loc_observations.
    
    sites:    List of Site instances
    lat:      float or int.  Interesting latitude
    lon:      float or int.  Interesting longitude
    """
    for site in sites:
        site.distance_to_coords(lat, lon)
    sites.sort(key=operator.attrgetter("distance"))
    return sites[0].ident

def extract_data_key(returned_data):
    """
    Build and return dict containing measurement 'name', description ('text')
    and unit of measurement.
    """
    return {i["name"]: {"text": i["$"], "units": i["units"]} for i in returned_data["SiteRep"]["Wx"]["Param"]}

def parse_val(returned_data):
    """
    Parse returned dict of MetOffer location-specific data into a
    Weather instance.
    """
    def _weather_dict_gen(returned_data):
        returned_reps = returned_data["SiteRep"]["DV"]["Location"]["Period"]
        if type(returned_reps) != list:
            returned_reps = [returned_reps]
        for i in returned_reps:
            y, m, d = i["value"][:-1].split("-")
            date = datetime.datetime(int(y), int(m), int(d))
            ureps = i["Rep"]
            if type(ureps) != list:
                ureps = [i["Rep"]]
            for rep in ureps:
                try:
                    dt = (date + datetime.timedelta(seconds=int(rep["$"]) * 60), "") # dt always a tuple
                except(ValueError):
                    dt = (date, rep["$"]) # Used for "DAILY" (time) step
                del rep["$"]
                weather = {"timestamp": dt}
                for n in rep:
                    try:
                        # -99 is used by the Met Office as a value where no data is held.
                        weather[data_key[n]["text"]] = (int(rep[n]) if rep[n]!= "-99" else None, data_key[n]["units"], n)
                    except(ValueError):
                        try:
                            weather[data_key[n]["text"]] = (float(rep[n]), data_key[n]["units"], n)
                        except(ValueError):
                            weather[data_key[n]["text"]] = (rep[n], data_key[n]["units"], n)
                yield weather
    ident = returned_data["SiteRep"]["DV"]["Location"]["i"]
    name = returned_data["SiteRep"]["DV"]["Location"]["name"]
    country = returned_data["SiteRep"]["DV"]["Location"]["country"]
    continent = returned_data["SiteRep"]["DV"]["Location"]["continent"]
    lat = returned_data["SiteRep"]["DV"]["Location"]["lat"]
    lon = returned_data["SiteRep"]["DV"]["Location"]["lon"]
    elevation = returned_data["SiteRep"]["DV"]["Location"]["elevation"]
    dtype = returned_data["SiteRep"]["DV"]["type"]
    data_date = returned_data["SiteRep"]["DV"]["dataDate"]
    data_key = extract_data_key(returned_data)
    data = []
    for weather in _weather_dict_gen(returned_data):
        data.append(weather)
    return Weather(ident, name, country, continent, lat, lon, elevation, dtype, data_date, data)

class Weather():
    """A hold-all for returned weather data, including associated metadata."""
    def __init__(self, ident, name, country, continent, lat, lon, elevation, dtype, data_date, data):
        self.ident = ident
        self.name = name
        self.country = country
        self.continent = continent
        self.lat = float(lat)
        self.lon = float(lon)
        self.elevation = float(elevation)
        self.dtype = dtype
        self.data_date = data_date
        self.data = data
