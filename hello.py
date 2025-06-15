# hello.py

def greet(name="World"):
    """
    This function greets the given name.
    If no name is provided, it greets "World".
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    message = greet("AI Learner")
    print(message)
    print(greet()) # This will greet "Hello, World!"