import datetime
import json
import os
from settings import FILENAME_REPO_JSON
from repository_fetcher.Github_Request import Github_Request
from repository_fetcher.Github_Request import _GITHUB_COMMITS

class Filter(Github_Request):

    
    # returns the filter function
    def last_commit_not_older_than(self, days):
        since = (datetime.datetime.now() - datetime.timedelta(days)).isoformat()
        def filter(repo):
            # with open(os.path.join(repo, FILENAME_REPO_JSON), "r") as g:
            #     repo = json.loads(g.read())
            return len(self.get_commit_since(repo, since)) > 0
        return filter


    def get_commit_since(self, repo, since):
        url = "{}?{}".format(_GITHUB_COMMITS.format(repo["full_name"]), self._createUrlParams({"since": str(since)}))
        return self._get(url)
