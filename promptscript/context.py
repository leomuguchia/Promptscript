# promptscript/context.py
from promptscript.ast import ProgramNode

def build_context(program: ProgramNode) -> dict:
    context = {
        "blueprint": {
            "name": program.blueprint.name,
            "version": program.blueprint.version,
            "author": program.blueprint.author,
            "goal": program.blueprint.goal,
        },
        "prompts": [],
        "workflow": None,
    }
    for prompt in program.prompts:
        prompt_context = {
            "name": prompt.name,
            "defines": [{"name": d.name, "definition": d.definition} for d in prompt.defines],
            "tasks": [],
        }
        for task in prompt.tasks:
            prompt_context["tasks"].append({
                "name": task.name,
                "input": task.input,
                "instruction": task.instruction,
                "output": task.output,
            })
        context["prompts"].append(prompt_context)
    if program.workflow:
        workflow_context = {
            "name": program.workflow.name,
            "steps": [],
        }
        for step in program.workflow.steps:
            workflow_context["steps"].append({
                "label": step.label,
                "invocation": {
                    "module": step.invocation.module,
                    "function": step.invocation.function,
                    "arguments": step.invocation.arguments,
                }
            })
        context["workflow"] = workflow_context
    return context
