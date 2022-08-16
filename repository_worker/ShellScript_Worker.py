import os
import subprocess
from settings import FILENAME_SHELL_LOG, TIMEOUT_SHELL
import settings
from repository_worker.WorkerError import WorkerError

def script_worker_func(repo, repo_path, s, iolock) -> str:

    # get path of git clone
    project_path = os.path.join(repo_path, repo["name"])
    if not os.path.exists(project_path):
        raise WorkerError("Project Not Exists")

    with iolock:
        path_to_script = s[settings.ARG_SHELL_SCRIPT]

    if not path_to_script:
        return

    try:
        with open(os.path.join(repo_path, FILENAME_SHELL_LOG), "w+") as f:
            #execute script
            cmd = "sh {} {} {}".format(path_to_script, repo_path, project_path)
            output = subprocess.check_output(cmd.split(), timeout=TIMEOUT_SHELL, stderr=f).decode("utf-8")
             # write log
            f.write(output)
       
        return "Download Success"
    except subprocess.CalledProcessError as e:
        raise WorkerError("Shell Failed")
    except subprocess.TimeoutExpired  as e:
        raise WorkerError("Shell Timeout")