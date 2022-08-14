
def download_worker_func(download_queue, downloaded_projects, download_result_queue, iolock, settings):
    from time import sleep
    import subprocess
    import json

    with iolock as lock:
        result_path = settings.result_path

    while True:
        repo, i = download_queue.get()
        if repo is None:
            download_result_queue.put(None)
            return

        local_project_path = "{}/{}_{}".format(result_path, i, repo["full_name"].replace("/", "_"))

        # create a folder to store project
        cmd_create_folder = "mkdir {}".format(local_project_path)
        process_create = subprocess.Popen(cmd_create_folder.split())
        process_create.communicate()

        # clone project with git
        cmd_clone_repo = "git clone {}".format(repo["html_url"])
        process_clone = subprocess.Popen(cmd_clone_repo.split(), cwd=local_project_path, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        process_clone.communicate()

        # create file with github properties
        with open("{}/github.json".format(local_project_path), 'w') as g:
            g.write(json.dumps(repo))

        with iolock:
            print("Download Finished For Project {}:\t\t{}".format(downloaded_projects.value, local_project_path))
            downloaded_projects.value += 1

        # add to result cue
        if download_result_queue:
            download_result_queue.put(local_project_path)
       
        
