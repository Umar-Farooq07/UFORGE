import subprocess

from app.workspace.workspace import Workspace
from app.terminal.models import CommandResult

import logging
logger = logging.getLogger(__name__)




class Terminal():

    def __init__(self, workspace : Workspace):
        self.workspace = workspace

    def run(self, command:str)->CommandResult:

        logger.info("running command on terminal %s", command)
        result = subprocess.run(command,
                            shell = True,
                            capture_output =True,
                            cwd = self.workspace.root_path,
                            text = True)
        logger.info("command finished with return code %d", result.returncode)
        command_result = CommandResult(
                            stdout=result.stdout,
                            stderr=result.stderr,
                            returncode=result.returncode,
                        )
        return command_result