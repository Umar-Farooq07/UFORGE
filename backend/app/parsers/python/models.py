from dataclasses import dataclass, field


@dataclass
class ClassInfo:
    name: str
    file_path : str
    line_number: int


@dataclass
class FunctionInfo:
    name: str
    file_path: str
    line_number: int

@dataclass
class ImportInfo:
    module_name: str
    symbol_name: str
    alias: str | None
    file_path: str
    line_number: int


@dataclass
class ParsedFile:
    classes: list[ClassInfo] = field(default_factory=list)
    functions: list[FunctionInfo] = field(default_factory=list)
    imports : list[ImportInfo] = field(default_factory=list)