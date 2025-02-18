# promptscript/translator.py
def build_chain_of_thought_prompt(blueprint: dict, task: dict) -> str:
    prompt = (
        f"Project Blueprint:\n"
        f"  Name: {blueprint['name']}\n"
        f"  Version: {blueprint['version']}\n"
        f"  Author: {blueprint['author']}\n"
        f"  Goal: {blueprint['goal']}\n\n"
        f"Task Details:\n"
        f"  Task Name: {task['name']}\n"
        f"  Input: {task['input']}\n"
        f"  Instruction: {task['instruction']}\n"
        f"  Expected Output: {task['output']}\n\n"
        "Generate robust, production-level code that implements the above task. "
        "Include proper error handling, security practices, and inline comments explaining the logic."
    )
    return prompt
