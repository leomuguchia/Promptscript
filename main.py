# main.py
import sys
from promptscript.parser import parse_promptscript
from promptscript.context import build_context
from promptscript.translator import build_chain_of_thought_prompt
from promptscript.ai_compiler import generate_code
from promptscript.aggregator import aggregate_code

def main(dsl_file):
    with open(dsl_file, "r") as f:
        dsl_text = f.read()

    # Parse the DSL into an AST and then build our hierarchical context
    program = parse_promptscript(dsl_text)
    context = build_context(program)

    code_fragments = []
    blueprint_context = context["blueprint"]
    for prompt in context["prompts"]:
        for task in prompt["tasks"]:
            prompt_text = build_chain_of_thought_prompt(blueprint_context, task)
            code = generate_code(prompt_text)
            code_fragments.append(code)

    final_code = aggregate_code(code_fragments)
    with open("generated_code.py", "w") as f:
        f.write(final_code)
    print("MVP complete! Generated code written to generated_code.py")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_dsl_file>")
    else:
        main(sys.argv[1])
