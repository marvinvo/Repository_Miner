import os
import subprocess
from settings import FILENAME_DOWNLOAD_LOG, TIMEOUT_DOWNLOAD, FILENAME_EXTENSION_FOR_ERRORS
from repository_worker.WorkerError import WorkerError


def download_worker_func(repo, repo_path, s, iolock) -> str:
    try:
        with open(os.path.join(repo_path, FILENAME_EXTENSION_FOR_ERRORS + FILENAME_DOWNLOAD_LOG), "w+") as f:
            #execute git clone
            cmd = "git clone {}".format(repo["html_url"])
            output = subprocess.check_output(cmd.split(), cwd=repo_path, timeout=TIMEOUT_DOWNLOAD, stderr=f).decode("utf-8")

            # execute git checkout to latest commit within the commit filter time range
            # this is actually not possible if no filter on commits have been set
            if "commits" in repo:
                cmd = "git checkout {}".format(repo["commits"][0]["sha"])
                clone_path = os.path.join(repo_path, repo["name"])
                output += subprocess.check_output(cmd.split(), cwd=clone_path, timeout=TIMEOUT_DOWNLOAD, stderr=f).decode("utf-8")

        with open(os.path.join(repo_path, FILENAME_DOWNLOAD_LOG), "w+") as f:    
            # write log
            f.write(output)
       
        return "Download Success"
    except subprocess.CalledProcessError as e:
        raise WorkerError("Download Failed")
    except subprocess.TimeoutExpired  as e:
        raise WorkerError("Download Timeout")


       
        
