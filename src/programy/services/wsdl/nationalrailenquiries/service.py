"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

This is an example extension that allow syou to call an external service to retreive the bank balance
of the customer. Currently contains no authentication
"""
import os
from datetime import datetime
from fuzzywuzzy import process
from programy.utils.logging.ylogger import YLogger
from programy.services.config import ServiceWSDLConfiguration
from programy.services.base import ServiceQuery
from programy.services.wsdl.base import WSDLService
from programy.services.wsdl.base import WSDLServiceException


class NationalRailEnquiriesWSDLServiceConfiguration(ServiceWSDLConfiguration):

    def __init__(self, service_type='wsdl'):
        ServiceWSDLConfiguration.__init__(self, service_type)
        self._station_codes_file = None

    @property
    def station_codes_file(self):
        return self._station_codes_file

    def from_yaml(self, service_data, filename):

        super(NationalRailEnquiriesWSDLServiceConfiguration, self).from_yaml(service_data, filename)

        self._station_codes_file = service_data.get("station_codes_file", None)


class NationalRailEnquiriesStationNameServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return NationalRailEnquiriesStationNameServiceQuery(service)

    def parse_matched(self, matched):
        self._crs = ServiceQuery._get_matched_var(matched, 0, "crs")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._crs = None

    def execute(self):
        return self._service.get_station_name_from_code(self._crs)

    def aiml_response(self, response):
        payload = response['response']['payload']
        station_name= payload['station_name']
        YLogger.debug(self, station_name)
        return station_name


class NationalRailEnquiriesStationCodeServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return NationalRailEnquiriesStationCodeServiceQuery(service)

    def parse_matched(self, matched):
        self._name = ServiceQuery._get_matched_var(matched, 0, "name")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._name = None

    def execute(self):
        return self._service.get_station_code_from_name(self._name)

    def aiml_response(self, response):
        payload = response['response']['payload']
        station_code = payload['station_code']
        YLogger.debug(self, station_code)
        return station_code


class NationalRailEnquiriesNextTrainFromServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return NationalRailEnquiriesNextTrainFromServiceQuery(service)

    def parse_matched(self, matched):
        self._station = ServiceQuery._get_matched_var(matched, 0, "station")
        self._platform = ServiceQuery._get_matched_var(matched, 1, "platform")
        self._destination = ServiceQuery._get_matched_var(matched, 2, "destination", optional=True)

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._station = None
        self._platform = None
        self._destination = None

    def execute(self):
        return self._service.next_trains_from_station(self._station, platform=self._platform, destination=self._destination)

    def aiml_response(self, response):
        payload = response['response']['payload']
        departures = payload['departures']
        platforms = departures['platforms']

        data = platforms[self._platform]
        first = data[0]
        std = first['std']
        eta = first['eta']
        operator = first['operator']
        origin = first['origin']
        destination = first['destination']

        data = "OPERATOR %s STD %s ETA %s ORIGIN %s DESTINATION %s"% (operator, std, eta, origin, destination)
        YLogger.debug(self, data)
        return data


class NationalRailEnquiriesWSDLServiceException(WSDLServiceException):

    def __init__(self, msg):
        WSDLServiceException.__init__(self, msg)


class NationalRailEnquiriesWSDLService(WSDLService):

    # https://lite.realtime.nationalrail.co.uk/OpenLDBWS/

    WSDL = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01'

    PATTERNS = [
        [r"STATION\sNAME\s(.+)", NationalRailEnquiriesStationNameServiceQuery],
        [r"STATION\sCODE\s(.+)", NationalRailEnquiriesStationCodeServiceQuery],
        [r"NEXT\sTRAIN\sFROM\s(.+)\sPLATFORM\s(.+)\sTO\s(.+)", NationalRailEnquiriesNextTrainFromServiceQuery],
        [r"NEXT\sTRAIN\sFROM\s(.+)\sPLATFORM\s(.+)", NationalRailEnquiriesNextTrainFromServiceQuery]
    ]

    def __init__(self, configuration):
        WSDLService.__init__(self, configuration)
        self._stations_cache = []
        self._stations_to_codes = {}
        self._codes_to_stations = {}
        self._header = None

    def patterns(self) -> list:
        return NationalRailEnquiriesWSDLService.PATTERNS

    def initialise(self, client):
        access_token = client.license_keys.get_key('NATIONAL_RAIL_ENQUIRIES')
        if access_token is None:
            YLogger.error(self, "NATIONAL_RAIL_ENQUIRIES missing from license.keys, service will not function correctly!")

        self._header = self._create_header(access_token)

        if self.configuration.station_codes_file:
            self._load_station_codes_to_stations(self.configuration.station_codes_file)

        if self.configuration.wsdl_file is None:
            self.create_wsdl_client(NationalRailEnquiriesWSDLService.WSDL)
        else:
            self.create_wsdl_client(self.configuration.wsdl_file)

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "nationalrailenquiries.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "nationalrailenquiries.conf"

    def _load_station_codes_to_stations(self, filename):
        self._stations_to_codes.clear()
        self._codes_to_stations.clear()
        self._stations_cache.clear()
        try:
            if os.path.exists(filename) is False:
                filename = os.path.dirname(__file__) + os.sep + filename

            with open(filename, 'r') as code_file:
                for line in code_file:
                    if line and ',' in line:
                        parts = line.strip().split(",")
                        station = parts[0].upper()
                        code = parts[1].upper()
                        self._stations_to_codes[code] = station
                        self._codes_to_stations[station] = code
                        self._stations_cache.append(station)
            YLogger.debug(self, "Loaded %d stations"%len(self._stations_cache))
        except Exception as e:
            YLogger.debug(self, "Failed to load station codes from %s"%filename)

    def _create_header(self, access_token):
        return {"AccessToken": access_token}

    def _validate_num_rows(self, num_rows):
        if num_rows < 1 or num_rows > 150:
            raise AttributeError("Invalid value for num_rows, between 1 and 150 only!")

    def _validate_crs(self, crs):
        if len(crs) != 3:
            raise AttributeError("Invalid crs value 3 letters only!")

    def _validate_filterCrs(self, filterCrs):
        if len(filterCrs) != 3:
            raise AttributeError("Invalid filterCrs value, 3 letters only!")

    def _validate_filterType(self, filterType):
        if filterType not in ['from', 'to']:
            raise AttributeError("Invalid filterType value, 'to' or 'from' only!")

    def _validate_filterList(self, filterList):
        if len(filterList) < 1 or len(filterList) > 15:
            raise AttributeError("Invalid filterList value, between 1 and 15 items")
        for filterCrs in filterList:
            if len(filterCrs) != 3:
                raise AttributeError("Invalid filterCrs value in filterList, 3 letters only!")

    def _validate_timeOffset(self, timeOffset):
        if timeOffset < -120 or timeOffset > 120:
            raise AttributeError("Invalid timeOffset value, between -120 and 120 only!")

    def _validate_timeWindow(self, timeWindow):
        if timeWindow < -120 or timeWindow > 120:
            raise AttributeError("Invalid timeWindow value, between -120 and 120 only!")

    def _validate_serviceID(self, serviceID):
        if not serviceID:
            raise AttributeError("Invalid serviceID value, None not allowed!")

    # Returns all public departures for the supplied CRS code within a defined time window, including service details.
    # GetArrBoardWithDetails(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoardWithDetails
    def get_arrival_boards_with_details(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetArrBoardWithDetails(numRows=numRows,
                                                               crs=crs,
                                                               filterCrs=filterCrs,
                                                               filterType=filterType,
                                                               timeOffset=timeOffset,
                                                               timeWindow=timeWindow,
                                                               _soapheaders=self._header)

            speed = started - datetime.now()

            if data is not None:
                result = {"arrival_boards_with_details": data}
                return self._create_success_payload("arrival_boards_with_details", started, speed, result)

            return self._create_failure_payload("arrival_boards_with_details", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("arrival_boards_with_details", started, speed, error)

    # Returns all public arrivals and departures for the supplied CRS code within a defined time window, including service details.
    # GetArrDepBoardWithDetails(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoardWithDetails
    def get_arrival_and_departure_boards_with_details(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetArrDepBoardWithDetails(numRows=numRows,
                                                                  crs=crs,
                                                                  filterCrs=filterCrs,
                                                                  filterType=filterType,
                                                                  timeOffset=timeOffset,
                                                                  timeWindow=timeWindow,
                                                                  _soapheaders=self._header)

            speed = started - datetime.now()

            if data is not None:
                result = {"arrival_and_departure_boards_with_details": data}
                return self._create_success_payload("arrival_and_departure_boards_with_details", started, speed, result)

            return self._create_failure_payload("arrival_and_departure_boards_with_details", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("arrival_and_departure_boards_with_details", started, speed, error)

    # Returns all public arrivals and departures for the supplied CRS code within a defined time window.
    # GetArrivalBoard(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoard
    def get_arrival_board(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetArrivalBoard(numRows=numRows,
                                                        crs=crs,
                                                        filterCrs=filterCrs,
                                                        filterType=filterType,
                                                        timeOffset=timeOffset,
                                                        timeWindow=timeWindow,
                                                        _soapheaders=self._header)
            speed = started - datetime.now()

            if data is not None:
                result = {"arrival_board": data}
                return self._create_success_payload("arrival_board", started, speed, result)

            return self._create_failure_payload("arrival_board", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("arrival_board", started, speed, error)

    # Returns all public arrivals and departures for the supplied CRS code within a defined time window.
    # GetArrivalDepartureBoard(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoard
    def get_arrival_and_departure_boards(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetArrivalDepartureBoard(numRows=numRows,
                                                                 crs=crs,
                                                                 filterCrs=filterCrs,
                                                                 filterType=filterType,
                                                                 timeOffset=timeOffset,
                                                                 timeWindow=timeWindow,
                                                                 _soapheaders=self._header)
            speed = started - datetime.now()

            if data is not None:
                result = {"arrival_and_departure_boards": data}
                return self._create_success_payload("arrival_and_departure_boards", started, speed, result)

            return self._create_failure_payload("arrival_and_departure_boards", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("arrival_and_departure_boards", started, speed, error)

    # Returns all public arrivals and departures for the supplied CRS code within a defined time window, including service details.
    # GetDepBoardWithDetails(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoardWithDetails
    def get_departure_board_with_details(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetDepBoardWithDetails(numRows=numRows,
                                                               crs=crs,
                                                               filterCrs=filterCrs,
                                                               filterType=filterType,
                                                               timeOffset=timeOffset,
                                                               timeWindow=timeWindow,
                                                               _soapheaders=self._header)
            speed = started - datetime.now()

            if data is not None:
                result = {"departure_board_with_details": data}
                return self._create_success_payload("departure_board_with_details", started, speed, result)

            return self._create_failure_payload("departure_board_with_details", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("departure_board_with_details", started, speed, error)

    # Returns all public departures for the supplied CRS code within a defined time window.
    # GetDepartureBoard(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoard
    def get_departure_board(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetDepartureBoard(numRows=numRows,
                                                          crs=crs,
                                                          filterCrs=filterCrs,
                                                          filterType=filterType,
                                                          timeOffset=timeOffset,
                                                          timeWindow=timeWindow,
                                                          _soapheaders=self._header)
            speed = started - datetime.now()

            if data is not None:
                result = {"departure_board": data}
                return self._create_success_payload("departure_board", started, speed, result)

            return self._create_failure_payload("departure_board", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("departure_board", started, speed, error)

    # Returns the public departure for the supplied CRS code within a defined time window to the locations specified in the filter with the earliest arrival time at the filtered location.
    # GetFastestDepartures(crs: ns2:CRSType, filterList: {crs: ns2:
    #    CRSType[]}, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> DeparturesBoard: ns4:DeparturesBoard
    def get_fastest_departures(self, crs, filterList, timeOffset=0, timeWindow=120):

        self._validate_crs(crs)
        self._validate_filterList(filterList)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetFastestDepartures(crs=crs,
                                                             filterList=filterList,
                                                             timeOffset=timeOffset,
                                                             timeWindow=timeWindow,
                                                             _soapheaders=self._header)

            speed = started - datetime.now()

            if data is not None:
                result = {"fastest_departures": data}
                return self._create_success_payload("fastest_departures", started, speed, result)

            return self._create_failure_payload("fastest_departures", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("fastest_departures", started, speed, error)


    # Returns the public departure for the supplied CRS code within a defined time window to the locations specified in the filter with the earliest arrival time at the filtered location, including service details.
    # GetFastestDeparturesWithDetails(crs: ns2:CRSType, filterList: {crs: ns2:
    #    CRSType[]}, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> DeparturesBoard: ns4:DeparturesBoardWithDetails
    def get_fastest_departures_with_details(self, crs, filterList, timeOffset=0, timeWindow=120):

        self._validate_crs(crs)
        self._validate_filterList(filterList)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetFastestDeparturesWithDetails(crs=crs,
                                                                        filterList=filterList,
                                                                        timeOffset=timeOffset,
                                                                        timeWindow=timeWindow,
                                                                        _soapheaders=self._header)
            speed = started - datetime.now()

            if data is not None:
                result = {"fastest_departures_with_details": data}
                return self._create_success_payload("fastest_departures_with_details", started, speed, result)

            return self._create_failure_payload("fastest_departures_with_details", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("fastest_departures_with_details", started, speed, error)

    # Returns the next public departure for the supplied CRS code within a defined time window to the locations specified in the filter.
    # GetNextDepartures(crs: ns2:CRSType, filterList: {crs: ns2:
    #    CRSType[]}, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> DeparturesBoard: ns4:DeparturesBoard
    def get_next_departures(self, crs, filterList, timeOffset=0, timeWindow=120):

        self._validate_crs(crs)
        self._validate_filterList(filterList)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetNextDepartures(crs=crs,
                                                          filterList=filterList,
                                                          timeOffset=timeOffset,
                                                          timeWindow=timeWindow,
                                                          _soapheaders=self._header)

            speed = started - datetime.now()

            if data is not None:
                result = {"next_departures": data}
                return self._create_success_payload("next_departures", started, speed, result)

            return self._create_failure_payload("next_departures", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("next_departures", started, speed, error)

    # Returns the next public departure for the supplied CRS code within a defined time window to the locations specified in the filter, including service details.
    # GetNextDeparturesWithDetails(crs: ns2:CRSType, filterList: {crs: ns2:
    #    CRSType[]}, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> DeparturesBoard: ns4:DeparturesBoardWithDetails
    def get_next_departures_with_details(self, crs, filterList, timeOffset=0, timeWindow=120):

        self._validate_crs(crs)
        self._validate_filterList(filterList)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetNextDeparturesWithDetails(crs=crs,
                                                                     filterList=filterList,
                                                                     timeOffset=timeOffset,
                                                                     timeWindow=timeWindow,
                                                                     _soapheaders=self._header)

            speed = started - datetime.now()

            if data is not None:
                result = {"next_departures_with_details": data}
                return self._create_success_payload("next_departures_with_details", started, speed, result)

            return self._create_failure_payload("next_departures_with_details", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("next_departures_with_details", started, speed, error)

    # Returns service details for a specific service identified by a station board. These details are supplied relative
    # to the station board from which the serviceID field value was generated. Service details are only available while
    # the service appears on the station board from which it was obtained. This is normally for two minutes after it is
    # expected to have departed, or after a terminal arrival. If a request is made for a service that is no longer
    # available then a null value is returned.
    # GetServiceDetails(serviceID: ns3:ServiceIDType, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetServiceDetailsResult: ns4:ServiceDetails
    def get_service_details(self, serviceID):

        self._validate_serviceID(serviceID)

        started = datetime.now()
        speed = None
        try:
            data = self._client.service.GetServiceDetails(serviceID=serviceID,
                                                          _soapheaders=self._header)

            speed = started - datetime.now()

            if data is not None:
                result = {"service_details": data}
                return self._create_success_payload("next_departures_with_details", started, speed, result)

            return self._create_failure_payload("service_details", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("service_details", started, speed, error)

    def get_station_name_from_code(self, code):
        started = datetime.now()
        speed = None

        if code in self._stations_to_codes:
            result = {"station_name": self._stations_to_codes[code]}
            speed = started - datetime.now()
            return self._create_success_payload("station_name_from_code", started, speed, result)

        return self._create_failure_payload("station_name_from_code", started, speed)

    def get_station_code_from_name(self, name):
        started = datetime.now()
        speed = None

        name = name.upper()
        if name in self._codes_to_stations:
            result = {"station_code": self._codes_to_stations[name]}
            return self._create_success_payload("get_station_code_from_name", started, speed, result)

        return self._create_failure_payload("get_station_code_from_name", started, speed)

    def get_station_code_from_fuzzy_name(self, name, limit=3, threshold=80):
        if name in self._codes_to_stations:
            return self._codes_to_stations[name]

        codes = []
        matches = self._match_station(name, limit, threshold)
        for name in matches:
            codes.append(self._codes_to_stations[name])

        if codes:
            return ", ".join(codes)

        return None

    def _match_station(self, candidate, limit=3, threshold=80):
        results = process.extract(candidate, self._stations_cache, limit=limit)
        matches = []
        for station, match in results:
            if match >= threshold:
                matches.append(station)
        return matches

    def _response_to_json(self, api, response):
        return response

    def next_trains_from_station(self, station, platform=None, origin=None, destination=None):

        started = datetime.now()
        speed = None

        try:
            if len(station) != 3:
                response = self.get_station_code_from_name(station)
                station = response['response']['payload']['station_code']

            if station is None:
                raise Exception ("Unknown station")

            if origin:
                if len(origin) != 3:
                    response = self.get_station_code_from_name(origin)
                    origin = response['response']['payload']['station_code']

            if destination:
                if len(destination) != 3:
                    response = self.get_station_code_from_name(destination)
                    destination = response['response']['payload']['station_code']

            departure_board = self.get_departure_board(10, station)

            response = departure_board.get('response')
            if response is None:
                raise Exception("no response in get_departure_board")

            if response.get('status', 'failure') == 'failure':
                raise Exception("Service called failed")

            payload = response.get('payload')
            if payload is None:
                raise Exception("no payload in get_departure_board")

            data = payload.get('departure_board')
            if data is None:
                raise Exception("no departure_board in get_departure_board")

            trainServices = data['trainServices']
            if trainServices is None:
                raise Exception("no trainServices in get_departure_board")

            services = trainServices.service
            if not services:
                raise Exception("no services in get_departure_board")

            result = {'platforms': {}}

            for service in services:
                service_operator = service.operator
                service_std = service.std
                service_etd = service.etd
                service_platform = service.platform
                service_origin = service.origin.location[0].locationName
                service_origin_crs = service.origin.location[0].crs
                service_destination = service.destination.location[0].locationName
                service_destination_crs = service.destination.location[0].crs

                if platform is not None:
                    if platform != service_platform:
                        continue

                if origin is not None:
                    if origin != service_origin_crs:
                        continue

                if destination is not None:
                    if destination != service_destination_crs:
                        continue

                if service_platform not in result.get('platforms'):
                    result['platforms'][service_platform] = []

                result['platforms'][service_platform].append({'operator': service_operator,
                                                              'std': service_std,
                                                              'eta': service_etd,
                                                              'origin': service_origin,
                                                              'destination': service_destination})

            speed = started - datetime.now()

            return self._create_success_payload("next_trains_from_station", started, speed, {'departures': result})

        except Exception as error:
            return self._create_exception_failure_payload("next_trains_from_station", started, speed, error)
