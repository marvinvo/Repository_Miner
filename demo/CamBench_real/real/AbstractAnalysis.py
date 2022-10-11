import os
import pathlib


class AbstractAnalysis():

    def tool_name() -> str:
        pass

    def __init__(self, project):
        pass

    def execute(self):
        pass

    def get_path_for_tool(self, tool_name):
        root_path = pathlib.Path(__file__).parent.parent.resolve()
        print(root_path)
        tool_path = os.path.join(root_path, "tools", tool_name)
        if os.path.exists(tool_path):
            return tool_path
        raise FileNotFoundError(tool_path)
