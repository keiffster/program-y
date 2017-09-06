# Emulating the following curl request in locust
#  curl 'http://localhost:5000/api/v1.0/ask?question=hello+world&sessionid=1234567890'

import random
from urllib.parse import urlencode
from locust import HttpLocust, TaskSet

questions = [
    "ASKWIKIPEDIA KEITH STERLING",
    "ASKWIKIPEDIA AIML",
    "ASKWIKIPEDIA PYTHON PROGRAMMING",
    "ASKWIKIPEDIA Edinburgh Festival Fringe",
    "ASKWIKIPEDIA FanDuel"
]

sessionids = [
    "111111111",
    "222222222",
    "333333333",
    "444444444",
    "555555555",
    "666666666",
    "777777777"
]

def ask(l):
    question_no = random.randint(0, len(questions)-1)
    sessionid_no = random.randint(0, len(sessionids)-1)

    data = {"question": questions[question_no],
            "sessionid":sessionids[sessionid_no]
            }
    url = "/api/v1.0/ask?" + urlencode(data)

    with l.client.get(url) as response:
        print("[%d] - [%s]"%(response.status_code, response.content))
        if response.status_code != 200:
            response.failure("Invalid bot response")

class UserBehavior(TaskSet):
    tasks = {ask: 1}

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000