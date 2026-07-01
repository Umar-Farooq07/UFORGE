from pathlib import Path

from app.workspace.workspace import Workspace
from app.workspace_analyzer.models import ProjectAnalysis
from app.core.config import CONFIG_FILES

import logging

logger = logging.getLogger(__name__)


class WorkspaceAnalyzer:

    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.project_analysis: ProjectAnalysis | None = None

    def analyze_workspace(self) -> ProjectAnalysis:

        logger.info("Analyzing workspace")

        languages: set[str] = set()
        configuration_files: list[str] = []
        readme_path: str | None = None
        docker_enabled = False

        project_name = self.workspace.root_path.name

        
        for file in self.workspace.list_files():

            path = Path(file)

            match path.suffix:

                case ".py":
                    languages.add("Python")

                case ".js":
                    languages.add("JavaScript")

                case ".ts":
                    languages.add("TypeScript")

                case ".tsx":
                    languages.add("TypeScript")

                case ".jsx":
                    languages.add("JavaScript")

                case ".java":
                    languages.add("Java")

                case ".cpp" | ".cc" | ".cxx":
                    languages.add("C++")

                case ".c":
                    languages.add("C")

                case ".go":
                    languages.add("Go")

                case ".rs":
                    languages.add("Rust")

                case ".php":
                    languages.add("PHP")

                case ".cs":
                    languages.add("C#")

                case ".html":
                    languages.add("HTML")

                case ".css":
                    languages.add("CSS")

            #
            # Detect configuration files
            #

            if path.name in CONFIG_FILES:
                configuration_files.append(file)

            #
            # Detect README
            #

            if path.name.lower().startswith("readme"):
                readme_path = file

            #
            # Detect Docker
            #

            if path.name == "Dockerfile":
                docker_enabled = True

        self.project_analysis = ProjectAnalysis(
            project_name=project_name,
            languages=sorted(languages),
            frameworks=[],
            configuration_files=configuration_files,
            readme_path=readme_path,
            docker_enabled=docker_enabled,
        )

        logger.info(
            "Workspace analysis completed. Languages=%s ConfigFiles=%d Docker=%s",
            self.project_analysis.languages,
            len(configuration_files),
            docker_enabled,
        )

        return self.project_analysis