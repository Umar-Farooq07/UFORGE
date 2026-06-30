import ast
import logging

from app.workspace.workspace import Workspace
from app.parsers.python.models import (
    ClassInfo,
    FunctionInfo,
    FileSymbols,
    ImportInfo

)

logger = logging.getLogger(__name__)


class PythonParser:

    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        

    def _extract_classes(self,tree: ast.AST,relative_path: str,) -> list[ClassInfo]:

        logger.info("Extracting classes from %s", relative_path)

        classes: list[ClassInfo] = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                logger.debug(
                    "Found class '%s' at line %d",
                    node.name,
                    node.lineno,
                )

                classes.append(
                    ClassInfo(
                        name=node.name,
                        file_path=relative_path,
                        line_number=node.lineno,
                    )
                )

        logger.info(
            "Extracted %d classes from %s",
            len(classes),
            relative_path,
        )

        return classes

    def _extract_functions(self,tree: ast.AST,relative_path: str,) -> list[FunctionInfo]:

        logger.info("Extracting functions from %s", relative_path)

        functions: list[FunctionInfo] = []

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                logger.debug(
                    "Found function '%s' at line %d",
                    node.name,
                    node.lineno,
                )

                functions.append(
                    FunctionInfo(
                        name=node.name,
                        file_path=relative_path,
                        line_number=node.lineno,
                    )
                )

        logger.info(
            "Extracted %d functions from %s",
            len(functions),
            relative_path,
        )

        return functions
    

    def _extract_imports(self,tree: ast.AST,relative_path: str,) -> list[ImportInfo]:

        logger.info("Extracting imports from %s", relative_path)

        imports: list[ImportInfo] = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:

                    logger.debug(
                        "Found import '%s' at line %d",
                        alias.name,
                        node.lineno,
                    )

                    imports.append(
                        ImportInfo(
                            module_name=alias.name,
                            symbol_name=None,
                            alias=alias.asname,
                            file_path=relative_path,
                            line_number=node.lineno,
                        )
                    )

            elif isinstance(node, ast.ImportFrom):

                module = node.module or ""

                for alias in node.names:

                    logger.debug(
                        "Found import '%s' from '%s' at line %d",
                        alias.name,
                        module,
                        node.lineno,
                    )

                    imports.append(
                        ImportInfo(
                            module_name=module,
                            symbol_name=alias.name,
                            alias=alias.asname,
                            file_path=relative_path,
                            line_number=node.lineno,
                        )
                    )

        logger.info(
            "Extracted %d imports from %s",
            len(imports),
            relative_path,
        )

        return imports


    def parse_file(self, relative_path: str) -> FileSymbols:

        logger.info("Parsing file %s", relative_path)

        source_code = self.workspace.read_file(relative_path)

        logger.debug("Successfully read %s", relative_path)

        tree = ast.parse(source_code)

        logger.debug("Successfully generated AST for %s", relative_path)

        classes = self._extract_classes(tree, relative_path)
        functions = self._extract_functions(tree, relative_path)
        imports = self._extract_imports(tree, relative_path)

        logger.info(
            "Completed parsing %s (%d classes, %d functions %d imports)",
            relative_path,
            len(classes),
            len(functions),
            len(imports)
        )

        return FileSymbols(
            classes=classes,
            functions=functions,
            imports= imports
        )

    def parse_directory(self) -> dict[str,FileSymbols]:

        logger.info("Starting workspace parsing")

        parsed_files: dict[str, FileSymbols] = {}

        python_files = self.workspace.find_files_by_extension(".py")

        logger.info(
            "Found %d Python files to parse",
            len(python_files),
        )

        for file in python_files:

            logger.info("Parsing %s", file)

            parsed_files[file] = self.parse_file(file)

        logger.info(
            "Completed parsing workspace (%d Python files)",
            len(parsed_files),
        )

        return parsed_files
    
    
    