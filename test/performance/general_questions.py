# Emulating the following curl request in locust
#  curl 'http://localhost:5000/api/v1.0/ask?question=hello+world&sessionid=1234567890'

import random
from urllib.parse import urlencode
from locust import HttpLocust, TaskSet

questions = [
"MY FAVORITE COLOR IS RED",
"MY FAVORITE COLOR IS GREEN",
"MY FAVORITE COLOR IS DIRTY GREY",
"I LIKE RED",
"I DO NOT LIKE COURGETTES",
"I HAVE A CAR",
"I HAVE AN EGG",
"I HAVE THE WORLD",
"I HAVE 12 COWS",
"I AM MARRIED",
"I AM A DOCTOR",
"I AM FROM SCOTLAND",
"I LIKE CHIPS",
"I LIKE TO PLAY RUGBY",
"I WOULD RATHER BE IN BED",
"MY SIGN IS PISCES",
"MY ORIENTATION IS STRAIGHT",
"MY ORIENTATION",
"MY LATITUDE IS RELAXED",
"MY LATITUDE",
"MY BOYFRIEND IS UNKNOWN",
"MY BOYFRIEND",
"MY GIRLFRIEND IS UNKNOWN",
"MY GIRLFRIEND",
"MY NAME",
"MY FIRST NAME IS PROGRAM",
"MY MIDDLE NAME IS Y",
"MY LAST NAME IS BOT",
"MY FULL NAME",
"MY TOWN IS KINGHORN",
"MY TOWN",
"MY LAST NAME IS SMITH",
"MY BIRTHPLACE",
"MY BIRTHPLACE IS SCOTLAND",
"MY NATIONALITY IS SCOTTISH"
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