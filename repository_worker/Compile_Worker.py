import os
import subprocess
from settings import FILENAME_COMPILE_LOG, TIMEOUT_COMPILE, FILENAME_EXTENSION_FOR_ERRORS
from repository_worker.WorkerError import WorkerError


def compile_worker_func(repo, repo_path, s, iolock, func, locks):

    # get path of git clone
    project_path = os.path.join(repo_path, repo["name"])
    if not os.path.exists(project_path):
        raise WorkerError("Project Not Exists")


    def run_build(cmd):
        try:
            with open(os.path.join(repo_path, FILENAME_EXTENSION_FOR_ERRORS + FILENAME_COMPILE_LOG), "w+") as f:
                # execute build command
                process_out = subprocess.check_output(str(cmd).split(), cwd=project_path, timeout=TIMEOUT_COMPILE, stderr=f).decode("utf-8")

            with open(os.path.join(repo_path, FILENAME_COMPILE_LOG), "w+") as f:
                # write log
                f.write(process_out)
            return "Compile Success"
        except subprocess.CalledProcessError:
            raise WorkerError("Compile Failed")
        except subprocess.TimeoutExpired:
            raise WorkerError("Compile Timeout")

    # make (only use in container)
    # make_file = os.path.join(project_path, "make")
    # if os.path.exists(make_file):
    #     return run_build("make")

    # maven
    mvn_pom = os.path.join(project_path, "pom.xml") 
    if os.path.exists(mvn_pom):
        return run_build("mvn clean package -DskipTests='True'")

    # gradle
    build_gradle = os.path.join(project_path, "build.gradle")
    if os.path.exists(build_gradle):
        with locks["gradle"]:
            if os.path.exists(os.path.join(project_path, "gradlew")):
                run_build("chmod 777 ./gradlew") # make gradlew executable
                return run_build("./gradlew")
            return run_build("gradle assemble")
    
    # ivy
    ivy_file = os.path.join(project_path, "ivy.xml")
    if os.path.exists(ivy_file):
        raise WorkerError("Ivy Build not implemented yet")

    raise WorkerError("Unknown Build Tool")
        

