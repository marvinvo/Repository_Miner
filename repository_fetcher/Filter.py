import datetime
import json
import os
from settings import FILENAME_REPO_JSON
from repository_fetcher.Github_Request import Github_Request
from repository_fetcher.Github_Request import _GITHUB_COMMITS

class Filter(Github_Request):

    
    # returns the filter function
    def last_commit_not_older_than(self, since, until):
        _since = datetime.datetime.strptime(since, '%d/%m/%y').isoformat()
        _until = datetime.datetime.strptime(until, '%d/%m/%y').isoformat()
        def filter(repo):
            # with open(os.path.join(repo, FILENAME_REPO_JSON), "r") as g:
            #     repo = json.loads(g.read())
            repo["commits"] = self.get_commits(repo, _since, _until)
            repo["commits_since"] = str(_since)
            repo["commits_until"] = str(_until)
            return len(repo["commits"]) > 0
        return filter


    def get_commits(self, repo, since, until):
        url = "{}?{}".format(_GITHUB_COMMITS.format(repo["full_name"]), self._createUrlParams({"since": str(since), "until": str(until)}))
        return self._get(url)
