
import datetime
from utils.Github_Request import Github_Request, _GITHUB_COMMITS

class Filter(Github_Request):
    
    # returns the filter function
    def last_commit_not_older_than(self, days):
        since = (datetime.datetime.now() - datetime.timedelta(days)).isoformat()
        def filter(repo):
            return len(self.get_commit_since(repo, since)) > 0
        return filter


    def get_commit_since(self, repo, since):
        url = "{}?{}".format(_GITHUB_COMMITS.format(repo["full_name"]), self._createUrlParams({"since": since}))
        return self._get(url)
