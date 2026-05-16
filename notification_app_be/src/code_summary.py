def summarize_code(file_path):
    with open(file_path, "r") as f:
        code = f.read()
    
    # Step 1: Basic summary (lines of code, functions, classes)
    summary = f"File has {code.count('def ')} functions and {code.count('class ')} classes."
    
    # Step 2: Plain-language explanation (simplified example)
    explanation = "This code defines functions and classes for some tasks."
    
    # Step 3: Basic error checks
    errors = []
    if "import" not in code:
        errors.append("No imports found – check dependencies.")
    
    # Step 4: Suggestions
    suggestions = []
    if "print(" in code:
        suggestions.append("Consider using logging instead of print for better debugging.")
    
    return summary, explanation, errors, suggestions
