class InvalidWorkspaceError(Exception):
    def __init__(self, root_path):
        super().__init__(f"{root_path}' is not a valid workspace directory.")

class WorkspaceFileNotFoundError(Exception):
    def __init__(self, file_path):
        super().__init__(f"{file_path} does not  exist in the workspace")

class FileDoesNotExistError(Exception):
    def __init__(self, filename):
        super().__init__(f"{filename} does not  exist in the workspace")

class ExtentionDoesNotExistError(Exception):
    def __init__(self, extention):
        super().__init__(f"file with {extention} does not  exist in the workspace")

class TextDoesNotExistError(Exception):
    def __init__(self, text):
        super().__init__(f"{text} does not exist in the workspace")
