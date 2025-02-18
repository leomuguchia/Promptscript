# promptscript/repl.py
def start_repl():
    print("Welcome to the PromptScript REPL. Type 'exit' to quit.")
    while True:
        user_input = input(">>> ")
        if user_input.strip().lower() == "exit":
            break
        # Here you could integrate parsing and evaluation of DSL snippets.
        print("Received:", user_input)
