

import json
from utils.Github_Request import Github_Request
from utils.Github_Request import _GITHUB_MAX_PAGE_RESULTS, _GITHUB_MAX_SEARCH_RESULTS, _GITHUB_SEACH
from multiprocessing import Value


class Get_Repositories(Github_Request):

    def __init__(self):
        self._sort = 'stars'
        self._order = 'desc'
        self._fork = 'false'
        self._language = 'Java'

    #
    # GET REPOSITORIES
    #

    def _getRepositories(self, last_sort=str(9999999), per_page=_GITHUB_MAX_PAGE_RESULTS, page="0"):
        data = {
            "q": "language:{}+{}:{}{}".format(self._language, self._sort, "<" if self._order=="desc" else ">", last_sort),
            "order": self._order,
            "sort": self._sort,
            "per_page": per_page,
            "page": page,
            "fork" : self._fork
        }
        url = "{}?{}".format(_GITHUB_SEACH, Github_Request._createUrlParams(data))
        print(url)
        return self._get(url)

    def getRepositories(self, repository_count=1000):
        items = []
        page = 0
        while(repository_count > 0):
            count = _GITHUB_MAX_PAGE_RESULTS if repository_count > _GITHUB_MAX_PAGE_RESULTS else repository_count
            response = self._getRepositories(per_page=count, page=page)
            items += json.loads(response.text)["items"]
            repository_count -= count
            page += 1
        return items

    def getRepositoriesGenerator(self):
        last_sort=str(9999999)
        page = 0
        while True:
            try:
                repos = self._getRepositories(last_sort=last_sort, per_page=_GITHUB_MAX_PAGE_RESULTS, page=str(page))["items"]
                for repo in repos:
                    yield repo
                
                page += 1

                # search api is limited to 1000 results
                # this provides a workaround to gain more
                if(page*_GITHUB_MAX_PAGE_RESULTS >= _GITHUB_MAX_SEARCH_RESULTS):
                    last_sort = repos[-1]["stargazers_count"]
                    page=0

            except KeyError:
                # only for debugging
                print(self._getRepositories(last_sort=last_sort, per_page=_GITHUB_MAX_PAGE_RESULTS, page=str(page)))

    def getRepositoriesGeneratorWithFilter(self, *args):
        print(args)
        if len(args) == 0:
            return self.getRepositoriesGenerator()
        else:
            return filter(args[-1], self.getRepositoriesGeneratorWithFilter(args[:-1]))

