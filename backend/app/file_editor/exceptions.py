class FileNotFoundError(Exception):
    def __init__(self, filepath):
        super().__init__(f"File not available at {filepath}")

class FileAlreadyExistError(Exception):
    def __init__(self, filepath):
        super().__init__(f"File already exists at {filepath}")

class FileDoesNotExistError(Exception):
    def __init__(self,filepath):
        super().__init__(f"File does not exists at {filepath}")
