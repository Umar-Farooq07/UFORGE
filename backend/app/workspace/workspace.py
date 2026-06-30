import os
from pathlib import Path
import copy

from app.workspace.exceptions import (InvalidWorkspaceError, WorkspaceFileNotFoundError,FileDoesNotExistError,ExtentionDoesNotExistError,   TextDoesNotExistError)
from app.core.config import DEFAULT_IGNORED_PATHS

import logging
logger = logging.getLogger(__name__)



class Workspace():

    def __init__(self, root_path):
        
        logger.info("Validating %s", root_path)

        if not os.path.isdir(root_path):

            logger.error("Workspace at %s not found", root_path)
            raise InvalidWorkspaceError(root_path)
        
        logger.info("Found the workspace at %s ",root_path)

        self.root_path = Path(root_path)             #stores aboslute path 
        self.files: list[str] = []                   #stores relative path 
        self.project_tree = {}

        self._scan_workspace()
        self._build_project_tree()


    def _scan_workspace(self):

        logger.info("Scanning workspace at %s", self.root_path)

        for root, dirs, files in os.walk(self.root_path):

            dirs[:] = [
                directory
                for directory in dirs
                if directory not in DEFAULT_IGNORED_PATHS       
            ]

            for file in files:

                if file in DEFAULT_IGNORED_PATHS:
                    continue

                full_path = Path(root) / file

                relative_path = full_path.relative_to(self.root_path)

                self.files.append(str(relative_path))

        logger.info(
            "Completed workspace scan at %s. Found %d files.",
            self.root_path,
            len(self.files),
        )
        

    def list_files(self)-> list[str]:
        return self.files.copy()


    def _build_project_tree(self):

        self.project_tree = {}

        for file_path in self.files:

            levels = file_path.split("/")

            current = self.project_tree

            for index, level in enumerate(levels):

                # Last level => file
                if index == len(levels) - 1:
                    current[level] = None

                # Directory
                else:
                    if level not in current:
                        current[level] = {}

                    current = current[level]
            
    
    def get_project_tree(self)->dict:
        return copy.deepcopy(self.project_tree)


    def read_file(self, filepath)->str:
        
        logger.info("Reading file at %s", filepath)

        absolute_file_path = self.root_path / filepath
        
        if not absolute_file_path.is_file():
            logger.error("%s does not exist in the workspace",filepath)
            raise WorkspaceFileNotFoundError(filepath)
        
        with open(absolute_file_path , 'r' , encoding="utf-8") as f:
            data = f.read()

        logger.info("completed file reading at %s",filepath)
        return data
    

    def read_files(self,filepaths : list[str])-> dict[str, str]:


        data = {}

        logger.info("reading %d files", len(filepaths))

        for filepath in filepaths:
            data[filepath] = self.read_file(filepath)

        logger.info("completed reading %d files", len(filepaths))

        return data

    def add_file(self, relative_filepath: str):
        self.files.append(relative_filepath)
        self._build_project_tree()


    def get_absolute_path(self, relative_path)->Path:
        return self.root_path / relative_path
    

    def remove_file(self, relative_filepath : str):
        self.files.remove(relative_filepath)
        self._build_project_tree()


    def find_file(self, filename)-> list[str]:

        temp_list = []
        logger.info("searching file %s filename", filename)
        for file in self.files:
            if(Path(file).name == filename):
                temp_list.append(file)

        if not temp_list:
            logger.warning("did not get file with file name %s", filename)
        else :
            logger.info("got the %d files with file name %s filename", len(temp_list), filename)
        return temp_list


    def find_files_by_extension(self, extension)->list[str]:
        
        temp_list = []
        logger.info("searching for file with extension %s", extension)
        for file in self.files:
            if(Path(file).suffix== extension):
                temp_list.append(file)

        if not temp_list:
            logger.warning("Did not get any file with extension %s", extension)
        else:
            logger.info("Got %d files with extension %s", len(temp_list), extension)
        return temp_list


    def search_text(self, text: str)->dict[str,list[int]]:
        
        temp_dict = {}

        logger.info("Searching for %s text in workspace", text)

        for file in self.files:

            line_numbers = []

            content = self.read_file(file)
            lines = content.splitlines()

            for line_index, line in enumerate(lines):
                if(text in line):
                    line_numbers.append(line_index+1)

            if(line_numbers):
                temp_dict[file] = line_numbers
        
        if not temp_dict:
            logger.warning("No file contains %s text ", text)
        else:
            logger.info("got %d files containing %s", len(temp_dict), text)

        return temp_dict
    
    
    def resolve_module(self, module_name: str) -> str | None:
        """
        Converts:
            app.workspace.workspace
        into:
            app/workspace/workspace.py

        Returns None if the module is not part of the workspace.
        """

        relative_path = module_name.replace(".", "/") + ".py"

        if relative_path in self.files:
            return relative_path

        return None
    

    
