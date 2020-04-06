"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
import os
import json
import urllib.parse
from datetime import datetime
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException


class GetGuidelinesAllServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GetGuidelinesAllServiceQuery(service)

    def parse_matched(self, matched):
        conditions = ServiceQuery._get_matched_var(matched, 0, "conditions")
        self._conditions = ",".join([x.lower() for x in conditions.split(" ")])

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._conditions = None

    def execute(self):
        return self._service.all(self._conditions)

    def aiml_response(self, response):
        payload = response['response']['payload']
        data = payload['data']
        data2 = [x['Recommendation'] for x in data]
        recommends = ["<li>{0}</li>\n".format(x) for x in data2]
        result = 'ALL <ol>{0}</ol>'.format("".join(recommends))
        YLogger.debug(self, result)
        return result


class GetGuidelinesVacServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GetGuidelinesVacServiceQuery(service)

    def parse_matched(self, matched):
        conditions = ServiceQuery._get_matched_var(matched, 0, "conditions")
        self._conditions = ",".join([x.lower() for x in conditions.split(" ")])

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._conditions = None

    def execute(self):
        return self._service.vac(self._conditions)

    def aiml_response(self, response):
        payload = response['response']['payload']
        result = 'CONDITIONS {0}'.format(str(payload))
        YLogger.debug(self, result)
        return result


class GetGuidelinesConditionsServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GetGuidelinesConditionsServiceQuery(service)

    def __init__(self, service):
        ServiceQuery.__init__(self, service)

    def execute(self):
        return self._service.conditions()

    def aiml_response(self, response):
        payload = response['response']['payload']

        result = "<ul><li>Key - Description</li>\n"
        for key, descr in payload.items():
            result += "<li>{0} - {1}</li>\n".format(key, descr)
        result += "</ul>"

        result = 'CONDITIONS {0}'.format(result)
        YLogger.debug(self, result)
        return result


class GetGuidelinesServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class GetGuidelinesService(RESTService):
    """
    """
    PATTERNS = [
        [r"ALL\s(.+)", GetGuidelinesAllServiceQuery],
        [r"VAC", GetGuidelinesVacServiceQuery],
        [r"CONDITIONS",GetGuidelinesConditionsServiceQuery]
    ]

    # conditions: Disease-specific recs. E.g. Congestive heart failure, chf Diabetes, dm. Sign in to see all conditions (too many to list here).
    CONDITIONS = {
        "dm": "Diabetes",
        "obese": "Overweight or Obesity",
        "hiv": "HIV",
        "sti": "Sexually transmitted infection",
        "postmenopause": "Postmenopause",
        "ivda": "Intravenous drug abuse",
        "msm": "Men who have sex with men",
        "hca": "Healthcare-associated",
        "liver": "Liver disease",
        "prison": "Incarceration history",
        "dialysis": "Dialysis (any type)",
        "asplenia": "Functional or anatomic asplenia",
        "scd": "Sickle cell disease or trait",
        "htn": "Hypertension",
        "heart": "Chronic heart disease",
        "lung": "Chronic lung disease",
        "csf": "Cerebrospinal fluid leak",
        "cochlear": "Cochlear implant",
        "ckd": "Chronic kidney disease",
        "ca": "Cancer / malignancy",
        "smoker": "Smoking status",
        "alcohol": "Alcohol abuse",
        "transplant": "Transplant status",
        "hypothyroid": "Hypothyroidism",
        "chf": "Congestive Heart Failure"
    }

    ALL_BASE_URL = "https://getguidelines.com/all"
    VAC_BASE_URL = "https://getguidelines.com/vac"
    
    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_token = None

    def patterns(self) -> list:
        return GetGuidelinesService.PATTERNS

    def initialise(self, client):
        self._api_token = client.license_keys.get_key('GETGUIDELINES')
        if self._api_token is None:
            YLogger.error(self, "GETGUIDELINES missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "getguidelines.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "getguidelines.conf"

    def _build_all_url(self,
                   conditions,
                   bmi=None,
                   age=None,
                   pack_years=None,
                   tst=None,
                   sbp=None,
                   dbp=None,
                   ldl=None,
                   trigs=None,
                   sex=None,
                   ethnicity=None,
                   pregnant=None,
                   cac=None,
                   broad=None,
                   ):
        url = GetGuidelinesService.ALL_BASE_URL
        url += "?api_token={0}".format(self._api_token)
        url += "&conditions={0}".format(conditions)
        return url

    def _build_vac_url(self,
                   conditions,
                   bmi=None,
                   age=None,
                   pack_years=None,
                   tst=None,
                   sbp=None,
                   dbp=None,
                   ldl=None,
                   trigs=None,
                   sex=None,
                   ethnicity=None,
                   pregnant=None,
                   cac=None,
                   broad=None,
                   ):
        url = GetGuidelinesService.VAC_BASE_URL
        url += "?api_token={0}".format(self._api_token)
        url += "&conditions={0}".format(urllib.parse.quote(conditions))
        return url

    def _check_query_data(self,
                          conditions,
                          bmi,
                          age,
                          pack_years,
                          tst,
                          sbp,
                          dbp,
                          ldl,
                          trigs,
                          sex,
                          ethnicity,
                          pregnant,
                          cac,
                          broad):

        # bmi: Body mass index. Alternatively, set kg and m, or lbs and inches to have bmi calculated and applied to corresponding guidelines.
        # tst: TB skin test, measured in millimeters of induration. E.g. tst=6
        # ldl & trigs: Cholesterol profile, LDL and triglyceride.
        # pregnant: Set =1, or specificy the number of weeks pregnant for prenatal guidelines.
        # sbp: Systolic blood pressure, I.e. "The top number. So, for 135/80, sbp=135."
        # sex: Female, male: f m
        # cac: Coronary artery calcium score.
        # dbp: Diastolic blood pressure, I.e. "The bottom number. So, for 135/80, dbp=80."
        # ethnicity: African American (aa), hispanic, white.
        # broad: Flag to expand results to broad match (default is exact).

        splits_conditions = conditions.split(",")
        for condition in splits_conditions:
            if condition not in GetGuidelinesService.CONDITIONS:
                raise GetGuidelinesServiceException(
                    "Unknown condition [{0} (lowercase and no spaces!)".format(condition))

    def all(self,
            conditions,
            bmi=None,
            age=None,
            pack_years=None,
            tst=None,
            sbp=None,
            dbp=None,
            ldl=None,
            trigs=None,
            sex=None,
            ethnicity=None,
            pregnant=None,
            cac=None,
            broad=None,
            ):
        self._check_query_data(
            conditions,
            bmi,
            age,
            pack_years,
            tst,
            sbp,
            dbp,
            ldl,
            trigs,
            sex,
            ethnicity,
            pregnant,
            cac,
            broad)
        url = self._build_all_url(
            conditions,
            bmi,
            age,
            pack_years,
            tst,
            sbp,
            dbp,
            ldl,
            trigs,
            sex,
            ethnicity,
            pregnant,
            cac,
            broad)
        response = self.query('all', url)
        return response

    def vac(self,
            conditions,
            bmi=None,
            age=None,
            pack_years=None,
            tst=None,
            sbp=None,
            dbp=None,
            ldl=None,
            trigs=None,
            sex=None,
            ethnicity=None,
            pregnant=None,
            cac=None,
            broad=None,
            ):
        self._check_query_data(
            conditions,
            bmi,
            age,
            pack_years,
            tst,
            sbp,
            dbp,
            ldl,
            trigs,
            sex,
            ethnicity,
            pregnant,
            cac,
            broad)
        url = self._build_vac_url(
            conditions,
            bmi,
            age,
            pack_years,
            tst,
            sbp,
            dbp,
            ldl,
            trigs,
            sex,
            ethnicity,
            pregnant,
            cac,
            broad)
        response = self.query('vac', url)
        return response

    def conditions(self):
        started = datetime.now()
        speed = started - datetime.now()
        return self._create_success_payload("conditions", "", "DIRECT", retries=0, started=started, speed=speed, response=GetGuidelinesService.CONDITIONS)

    def _response_to_json(self, api, response):

        if api == 'conditions':
            return response

        elif api == 'all' or api == 'vac':
            return json.loads(response.text)

        return None