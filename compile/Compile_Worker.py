
from unittest import result


def compile_worker_func(compile_queue, compiled_projects, iolock, settings):

    while True:
        local_project_path = compile_queue.get()
        if local_project_path is None:
            return
        
        print(local_project_path)
