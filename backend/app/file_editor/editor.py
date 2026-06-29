import os

from app.workspace.workspace import Workspace
from app.file_editor.exceptions import FileNotFoundError, FileAlreadyExistError, FileDoesNotExistError

import logging
logger= logging.getLogger(__name__)


class FileEditor():

    def __init__(self, workspace:Workspace):
        self.workspace = workspace


    def create_file(self, relative_filepath : str, content : str):
        
        absolute_filepath = self.workspace.get_absolute_path(relative_filepath)
        if(absolute_filepath.exists()):
            logger.error("file already exists at %s", relative_filepath)
            raise FileAlreadyExistError(relative_filepath)
        
        logger.info("writing into file at %s", absolute_filepath)

        absolute_filepath.parent.mkdir(parents=True, exist_ok=True)

        
        with open(absolute_filepath, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info("completed writing file inot %s", absolute_filepath)
        self.workspace.add_file(relative_filepath)

        
        

    def update_file(self, relative_filepath : str, content : str ):

        absolute_filepath = self.workspace.get_absolute_path(relative_filepath)

        logger.info("updating into file at %s", relative_filepath)

        if(not absolute_filepath.exists()):
            logger.info("File does not exist at %s", relative_filepath)
            raise FileDoesNotExistError(relative_filepath)
        
        with open(absolute_filepath,"w", encoding="utf-8") as f:
            f.write(content)

        logger.info("writing completed into file %s", relative_filepath)
        

    def delete_file(self, relative_filepath : str):
        
        absolute_filepath = self.workspace.get_absolute_path(relative_filepath)
        if(not absolute_filepath.exists()):
            logger.error("File does not exist at %s", relative_filepath)
            raise FileDoesNotExistError(relative_filepath)
        absolute_filepath.unlink()
        self.workspace.remove_file(relative_filepath)
        logger.info("deleted file at %s", relative_filepath)

    