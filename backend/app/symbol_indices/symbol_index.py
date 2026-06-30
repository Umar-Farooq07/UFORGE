
from app.parsers.python.parser import PythonParser
from app.parsers.python.models import ClassInfo, FunctionInfo, FileSymbols

import logging
logger = logging.getLogger(__name__)


class SymbolIndex:

    def __init__(self, parser: PythonParser):

        self.parser = parser

        self.files = {}

        self.classes = {}

        self.functions = {}

        self.dependencies = {}
        
        self.reverse_dependencies = {}

        self._build_index()

        self._create_dependency_graph()
    

    def _build_index(self):
        
        logger.info("Building symbol index")
        for file in self.parser.workspace.find_files_by_extension(".py"):
            
            file_symbols = self.parser.parse_file(file)

            self.files[file] = file_symbols
            for class_item in file_symbols.classes:
                if(class_item.name not in self.classes ):
                    self.classes[class_item.name] = []
                self.classes[class_item.name].append(class_item)
                
            for function_item in file_symbols.functions:
                if(function_item.name not in self.functions):
                    self.functions[function_item.name] = []
                self.functions[function_item.name].append(function_item)
            

        logger.info(
                    "Indexed %d files, %d classes, %d functions",
                    len(self.files),
                    sum(len(v) for v in self.classes.values()),
                    sum(len(v) for v in self.functions.values()),
                )
        
    def find_function(self, function_name: str)->list[FunctionInfo]:
        return self.functions.get(function_name, [])

    def find_class(self, class_name:str)->list[ClassInfo]:
        return self.classes.get(class_name,[])

    def get_file_symbols(self, relative_path:str)->FileSymbols:
        return self.files.get(relative_path)
    
    def _create_dependency_graph(self):

        logger.info("Building dependencies graph")

        self.dependencies = {}

        self.reverse_dependencies = {}

        for file_path, file_symbols in self.files.items():

            self.dependencies[file_path] = []

            for import_info in file_symbols.imports:

                dependency_file = self.parser.workspace.resolve_module(
                    import_info.module_name
                )

                if dependency_file is None:
                    continue

                self.dependencies[file_path].append(dependency_file)

                if dependency_file not in self.reverse_dependencies:
                    self.reverse_dependencies[dependency_file] = []

                self.reverse_dependencies[dependency_file].append(file_path)

        logger.info(
            "Built dependencies graph for %d files",
            len(self.dependencies),
        )


