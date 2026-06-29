from dataclasses import dataclass


@dataclass
class CommandResult():
    stdout : str
    stderr : str
    returncode : int