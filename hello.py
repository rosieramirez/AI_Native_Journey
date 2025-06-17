# hello.py

def greet(name="World"):
    """
    This function greets the given name.
    If no name is provided, it greets "World".
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Ask for user's name
    user_name = input("Please enter your name (or press Enter for default): ")
    
    # Use the entered name if provided, otherwise use default
    if user_name:
        message = greet(user_name)
    else:
        message = greet()
    
    print(message)