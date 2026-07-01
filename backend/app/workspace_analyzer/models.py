from dataclasses import dataclass
from pathlib import Path

@dataclass
class ProjectAnalysis():
    project_name : str
    languages : list[str]
    frameworks : list[str]
    configuration_files : list[str]
    entry_point : list[str]
    readme_path : Path | None
    files : list[Path] 
    docker_enabled : bool

