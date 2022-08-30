import os
import subprocess
from settings import FILENAME_SHELL_LOG, TIMEOUT_SHELL, FILENAME_EXTENSION_FOR_ERRORS
import settings
from repository_worker.WorkerError import WorkerError

def script_worker_func(repo, repo_path, s, iolock, func, locks) -> str:

    # get path of git clone
    project_path = os.path.join(repo_path, repo["name"])
    if not os.path.exists(project_path):
       raise WorkerError("Project Not Exists")

    with iolock:
        path_to_script = func["name"]

    if not path_to_script:
        return

    
    try:
        with open(os.path.join(repo_path, FILENAME_EXTENSION_FOR_ERRORS + FILENAME_SHELL_LOG), "a+") as f:
            #execute script
            cmd = "{} {} {}".format(path_to_script, repo_path, project_path)
            output = subprocess.check_output(cmd.split(), timeout=TIMEOUT_SHELL, stderr=f).decode("utf-8")

        with open(os.path.join(repo_path, FILENAME_SHELL_LOG), "a+") as f:
             # write log
            f.write("Execute: {}".format(path_to_script))
            f.write(output)
       
        return "{} Success".format(path_to_script)
    except subprocess.CalledProcessError as e:
        raise WorkerError("{} Failed".format(path_to_script))
    except subprocess.TimeoutExpired  as e:
        raise WorkerError("{} Timeout".format(path_to_script))