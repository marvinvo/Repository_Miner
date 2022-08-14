from datetime import datetime
import json
from time import sleep
import requests

from settings import Settings

# adresses
_GITHUB_API = "https://api.github.com"
_GITHUB_SEACH = "{}/search/repositories".format(_GITHUB_API)
_GITHUB_COMMITS = "{}/repos/{}/commits".format(_GITHUB_API, "{}")


_GITHUB_MAX_PAGE_RESULTS = 100
_GITHUB_MAX_SEARCH_RESULTS = 1000
_GITHUB_TIMEOUT_ON_EXCEEDED_RATE = 65 #seconds

class Github_Request:

    def __init__(self):
        self.settings = Settings()

    def _get(self, url, data={}):
        utq = self.settings.user_token_queue
        req = requests.get(url, data, auth=(utq[0][0], utq[0][1]))
        response = json.loads(req.text)

        # try with other tokens when exceeded rate limit
        if "message" in response and "rate limit" in response["message"]:
            # update time when exceeded rate limit occur
            utq[0][2] = datetime.now().isoformat()
            # change current token
            utq = utq[1:] + [utq[0]]

            if(utq[0][2] != None and (datetime.now() - datetime.fromisoformat(utq[0][2])).total_seconds() < _GITHUB_TIMEOUT_ON_EXCEEDED_RATE):
                # all access tokens exceeded rate limit
                # wait till first may request again
                time_to_wait = _GITHUB_TIMEOUT_ON_EXCEEDED_RATE - (datetime.now() - datetime.fromisoformat(utq[0][2])).total_seconds()
                print("Exceeded rate for all tokens. Time to wait: {}".format(time_to_wait))
                sleep(time_to_wait)

            # retry
            response = self._get(url, data)

        # return parsed response
        return response
    
    @staticmethod
    def _createUrlParams(params={}):
        return "&".join(["{}={}".format(key, params[key]) for key in params])
