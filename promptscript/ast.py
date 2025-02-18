# promptscript/ast.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class BlueprintNode:
    name: str
    version: str
    author: str
    goal: str

@dataclass
class DefineNode:
    name: str
    definition: str

@dataclass
class TaskNode:
    name: str
    input: str
    instruction: str
    output: str

@dataclass
class PromptNode:
    name: str
    defines: List[DefineNode] = field(default_factory=list)
    tasks: List[TaskNode] = field(default_factory=list)

@dataclass
class InvocationNode:
    module: str
    function: str
    arguments: List[str]

@dataclass
class StepNode:
    label: str
    invocation: InvocationNode

@dataclass
class WorkflowNode:
    name: str
    steps: List[StepNode] = field(default_factory=list)

@dataclass
class ProgramNode:
    blueprint: BlueprintNode
    prompts: List[PromptNode]
    workflow: Optional[WorkflowNode]
