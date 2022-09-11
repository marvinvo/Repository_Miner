import json
import os
from repository_fetcher.Github_Request import Github_Request, _GITHUB_MAX_PAGE_RESULTS, _GITHUB_MAX_SEARCH_RESULTS, _GITHUB_SEACH
from settings import FILENAME_REPO_JSON
import settings
from repository_fetcher.Filter import Filter




class Get_Repositories(Github_Request):
        
    #
    # GET REPOSITORIES
    #

    def _getRepositories(self, last_sort=str(9999999), per_page=_GITHUB_MAX_PAGE_RESULTS, page="0"):
        data = {
            "q": "language:Java+{}:{}{}".format(self.s[settings.ARG_SORT], "<" if self.s[settings.ARG_ORDER]=="desc" else ">", last_sort),
            "order": self.s[settings.ARG_ORDER],
            "sort": self.s[settings.ARG_SORT],
            "per_page": per_page,
            "page": page,
            "fork" : self.s[settings.ARG_FORK]
        }
        # TODO
        url = "{}?{}".format(_GITHUB_SEACH, Github_Request._createUrlParams(data))
        print(url)
        return self._get(url)

    # def getRepositories(self, repository_count=1000):
    #     items = []
    #     page = 0
    #     while(repository_count > 0):
    #         count = _GITHUB_MAX_PAGE_RESULTS if repository_count > _GITHUB_MAX_PAGE_RESULTS else repository_count
    #         response = self._getRepositories(per_page=count, page=page)
    #         items += json.loads(response.text)["items"]
    #         repository_count -= count
    #         page += 1
    #     return items


    def getRepositoriesGenerator(self):
        last_sort=self.s[settings.ARG_LAST_SORT]
        page = 0
        while True:
            try:
                for _ in range(5):
                    repos = self._getRepositories(last_sort=last_sort, per_page=_GITHUB_MAX_PAGE_RESULTS, page=str(page))["items"]
                    for repo in repos:
                        yield repo

                page += 1

                # search api is limited to 1000 results
                # this provides a workaround to gain more
                if(page*_GITHUB_MAX_PAGE_RESULTS >= _GITHUB_MAX_SEARCH_RESULTS):
                    last_sort = repos[int(len(repos)/3)]["stargazers_count"]
                    page=0

            except KeyError:
                # only for debugging
                print(self._getRepositories(last_sort=last_sort, per_page=_GITHUB_MAX_PAGE_RESULTS, page=str(page)))

            

    def getRepositoriesGeneratorWithFilter(self, filter_list):
        if len(filter_list) <= 0:
            return self.getRepositoriesGenerator()
        else:
            return filter(filter_list[-1], self.getRepositoriesGeneratorWithFilter(filter_list[:-1]))

    
    def getRepositoryGeneratorFromSettings(self):
        # TODO filters should be parsed from command line
        filt = [Filter(self.s).last_commit_not_older_than("22/02/22", "22/08/22")]

        repo_gen = self.getRepositoriesGeneratorWithFilter(filt)
        while True:
            repo = next(repo_gen)
            project_path = os.path.join(self.s[settings.ARG_RESULTFOLDER], repo["full_name"].replace("/", "_"))

            try:
                # create a folder to store project
                os.makedirs(project_path, exist_ok=False)
            except OSError:
                # project has already been fetched
                continue

            # create file with github properties
            with open(os.path.join(project_path, FILENAME_REPO_JSON), 'w') as g:
                g.write(json.dumps(repo))

            yield project_path

    




