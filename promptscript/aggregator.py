# promptscript/aggregator.py
def aggregate_code(code_fragments: list) -> str:
    header = "# --- Aggregated Code ---\n\n"
    return header + "\n\n".join(code_fragments)
