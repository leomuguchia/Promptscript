# promptscript/parser.py
from lark import Lark, Transformer
from promptscript.ast import BlueprintNode, DefineNode, TaskNode, PromptNode, InvocationNode, StepNode, WorkflowNode, ProgramNode

GRAMMAR = r"""
?start: blueprint prompt* workflow?

blueprint: "blueprint" NAME "{" blueprint_body "}"
blueprint_body: (version | author | goal)*
version: "version:" STRING
author: "author:" STRING
goal: "goal:" STRING

prompt: "prompt" NAME "{" prompt_body "}"
prompt_body: (define | task)+
define: "define" NAME ":" definition_body
definition_body: /[^{\n]+/ 

task: "task" NAME ":" task_body
task_body: task_field+
task_field: "input:" /[^\n]+/ 
          | "instruction:" STRING 
          | "output:" STRING

workflow: "workflow" NAME "{" workflow_body "}"
workflow_body: step+
step: "step" NAME "->" invocation
invocation: NAME "." NAME "(" [arguments] ")"
arguments: NAME ("," NAME)*

NAME: /[a-zA-Z_]\w*/
STRING: /"(?:\\.|[^"\\])*"/

%import common.WS
%ignore WS
"""

class PromptScriptTransformer(Transformer):
    def NAME(self, token):
        return str(token)

    def STRING(self, token):
        # Remove the surrounding quotes
        return str(token)[1:-1]

    def blueprint(self, items):
        name = items[0]
        # items[1:] are tuples like ("version", value), ("author", value), ("goal", value)
        version = ""
        author = ""
        goal = ""
        for item in items[1:]:
            key, value = item
            if key == "version":
                version = value
            elif key == "author":
                author = value
            elif key == "goal":
                goal = value
        return BlueprintNode(name=name, version=version, author=author, goal=goal)

    def version(self, items):
        return ("version", items[0])

    def author(self, items):
        return ("author", items[0])

    def goal(self, items):
        return ("goal", items[0])

    def prompt(self, items):
        name = items[0]
        defines = []
        tasks = []
        for item in items[1:]:
            if isinstance(item, DefineNode):
                defines.append(item)
            elif isinstance(item, TaskNode):
                tasks.append(item)
        return PromptNode(name=name, defines=defines, tasks=tasks)

    def define(self, items):
        name = items[0]
        definition = items[1].strip()
        return DefineNode(name=name, definition=definition)

    def task(self, items):
        name = items[0]
        input_field = ""
        instruction_field = ""
        output_field = ""
        for key, value in items[1:]:
            if key == "input":
                input_field = value.strip()
            elif key == "instruction":
                instruction_field = value
            elif key == "output":
                output_field = value
        return TaskNode(name=name, input=input_field, instruction=instruction_field, output=output_field)

    def task_field(self, items):
        # The entire line as a string (e.g., "input: User user")
        text = items[0].strip()
        if text.startswith("input:"):
            return ("input", text[len("input:"):].strip())
        elif text.startswith("instruction:"):
            # Remove the keyword and trim quotes if present.
            val = text[len("instruction:"):].strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            return ("instruction", val)
        elif text.startswith("output:"):
            val = text[len("output:"):].strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            return ("output", val)
        return ("unknown", text)

    def task_body(self, items):
        return items

    def prompt_body(self, items):
        return items

    def blueprint_body(self, items):
        return items

    def definition_body(self, items):
        return str(items[0])

    def workflow(self, items):
        name = items[0]
        steps = items[1:]
        return WorkflowNode(name=name, steps=steps)

    def step(self, items):
        label = items[0]
        invocation = items[1]
        return StepNode(label=label, invocation=invocation)

    def invocation(self, items):
        module = items[0]
        function = items[1]
        arguments = items[2] if len(items) > 2 else []
        return InvocationNode(module=module, function=function, arguments=arguments)

    def arguments(self, items):
        return items

def parse_promptscript(dsl_text: str) -> ProgramNode:
    parser = Lark(GRAMMAR, parser='lalr', transformer=PromptScriptTransformer())
    return parser.parse(dsl_text)
