from flask import Flask, render_template, request, jsonify, session
import markdown
import subprocess
import sys
import tempfile
import os
import json
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from functools import wraps
import signal
import traceback
import platform

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.tailwindcss.com cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' fonts.googleapis.com cdnjs.cloudflare.com; font-src 'self' fonts.gstatic.com; img-src 'self' data: lh3.googleusercontent.com;"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8000'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Timeout handler for Unix systems
def timeout_handler(signum, frame):
    raise TimeoutError("Code execution timed out")

# Restricted Python builtins
ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'chr',
    'complex', 'dict', 'divmod', 'enumerate', 'filter', 'float', 'format',
    'frozenset', 'hash', 'hex', 'int', 'isinstance', 'issubclass', 'iter',
    'len', 'list', 'map', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'print',
    'range', 'repr', 'reversed', 'round', 'set', 'slice', 'sorted', 'str',
    'sum', 'tuple', 'type', 'zip'
}

# Python lessons content
LESSONS = {
    'basics': {
        'title': 'Python Basics',
        'topics': [
            {
                'id': 'variables',
                'title': 'Variables and Data Types',
                'content': '''
# Variables and Data Types in Python

In Python, you can store data in variables. Here are some examples:

```python
# Numbers
age = 25              # Integer
height = 1.75         # Float
complex_num = 3 + 4j  # Complex number

# Strings
name = "Alice"
greeting = 'Hello, World!'
multi_line = """This is a
multi-line string"""

# Booleans
is_student = True
is_working = False

# Lists (ordered, mutable)
fruits = ["apple", "banana", "orange"]
mixed_list = [1, "hello", True, 3.14]

# Tuples (ordered, immutable)
coordinates = (10, 20)
rgb = (255, 128, 0)

# Dictionaries (key-value pairs)
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}
```

Try it yourself! Create some variables of different types and print them.
''',
                'exercise': '''# Create variables of different types and print them
name = "Your Name"
age = 25
height = 1.75
is_student = True

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height}m")
print(f"Student: {is_student}")''',
            },
            {
                'id': 'control_flow',
                'title': 'Control Flow',
                'content': '''
# Control Flow in Python

Python uses indentation to define blocks of code. Here are the main control flow structures:

```python
# If statements
age = 18
if age >= 18:
    print("You are an adult")
elif age >= 13:
    print("You are a teenager")
else:
    print("You are a child")

# For loops
# Looping through a list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(fruit)

# Looping with range
for i in range(5):  # 0 to 4
    print(i)

# While loops
count = 0
while count < 3:
    print(count)
    count += 1

# Break and Continue
for i in range(10):
    if i == 3:
        continue  # Skip 3
    if i == 8:
        break    # Stop at 8
    print(i)
```

Try writing your own control flow statements!
''',
                'exercise': '''# Write a program that prints numbers 1-10
# but prints "Fizz" for multiples of 3
# and "Buzz" for multiples of 5
# and "FizzBuzz" for multiples of both

for num in range(1, 11):
    # Your code here
    pass''',
            },
            {
                'id': 'functions',
                'title': 'Functions',
                'content': '''
# Functions in Python

Functions are reusable blocks of code that perform specific tasks.

```python
# Basic function
def greet(name):
    return f"Hello, {name}!"

# Function with default parameter
def power(base, exponent=2):
    return base ** exponent

# Function with multiple parameters
def calculate_total(items, tax_rate=0.1):
    subtotal = sum(items)
    tax = subtotal * tax_rate
    return subtotal + tax

# Lambda function (anonymous function)
square = lambda x: x * x

# Example usage:
print(greet("Alice"))  # Output: Hello, Alice!
print(power(3))        # Output: 9 (3^2)
print(power(2, 3))     # Output: 8 (2^3)
print(square(4))       # Output: 16
```

Try creating your own functions!
''',
                'exercise': '''# Create a function that takes a list of numbers
# and returns the average (mean) value

def calculate_average(numbers):
    # Your code here
    pass

# Test your function
test_numbers = [10, 20, 30, 40, 50]
result = calculate_average(test_numbers)
print(f"The average is: {result}")''',
            }
        ]
    },
    'intermediate': {
        'title': 'Intermediate Python',
        'topics': [
            {
                'id': 'list_comprehension',
                'title': 'List Comprehension',
                'content': '''
# List Comprehension in Python

List comprehension provides a concise way to create lists based on existing lists or other sequences.

```python
# Basic list comprehension
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]

# List comprehension with condition
even_squares = [x**2 for x in numbers if x % 2 == 0]

# Nested list comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]

# Dictionary comprehension
names = ['Alice', 'Bob', 'Charlie']
name_lengths = {name: len(name) for name in names}
```

Try creating your own list comprehensions!
''',
                'exercise': '''# Create a list of squares of even numbers from 1 to 10
# using list comprehension

# Your code here
squares_of_evens = []

print(squares_of_evens)''',
            }
        ]
    }
}

# User progress tracking
def init_progress():
    if 'progress' not in session:
        session['progress'] = {
            'completed_lessons': set(),
            'exercises_completed': 0,
            'total_code_runs': 0
        }

# After the LESSONS dictionary, add:

LESSON_VALIDATORS = {
    'basics': {
        'variables': {
            'check': lambda code: all(x in code for x in ['name', 'age', 'height', 'is_student']),
            'hint': "Make sure to create all required variables: name, age, height, and is_student"
        },
        'control_flow': {
            'check': lambda code: 'for' in code and ('Fizz' in code and 'Buzz' in code),
            'hint': "Remember to use a for loop and check for both Fizz (multiples of 3) and Buzz (multiples of 5)"
        },
        'functions': {
            'check': lambda code: 'def calculate_average' in code and 'return' in code and 'sum' in code,
            'hint': "Define the calculate_average function and use sum() to calculate the average"
        }
    },
    'intermediate': {
        'list_comprehension': {
            'check': lambda code: '[' in code and 'for' in code and 'if' in code,
            'hint': "Use list comprehension syntax: [expression for item in list if condition]"
        }
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/lessons')
def get_lessons():
    return jsonify(LESSONS)

@app.route('/api/lesson/<category>/<topic_id>')
def get_lesson(category, topic_id):
    if category in LESSONS:
        for topic in LESSONS[category]['topics']:
            if topic['id'] == topic_id:
                # Convert markdown content to HTML
                topic['content_html'] = markdown.markdown(
                    topic['content'],
                    extensions=['fenced_code', 'codehilite']
                )
                return jsonify(topic)
    return jsonify({'error': 'Lesson not found'}), 404

@app.route('/api/progress')
def get_progress():
    init_progress()
    return jsonify(list(session['progress']['completed_lessons']))

@app.route('/api/complete_lesson', methods=['POST'])
def complete_lesson():
    init_progress()
    data = request.get_json()
    lesson_id = data.get('lesson_id')
    if lesson_id:
        session['progress']['completed_lessons'].add(lesson_id)
        session['progress']['exercises_completed'] += 1
        session.modified = True
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/api/validate_code', methods=['POST'])
def validate_code():
    data = request.get_json()
    code = data.get('code', '')
    lesson_category = data.get('category')
    lesson_id = data.get('lesson_id')
    
    if not all([code, lesson_category, lesson_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
        
    validator = LESSON_VALIDATORS.get(lesson_category, {}).get(lesson_id)
    if not validator:
        return jsonify({'success': True})  # No validation required
        
    is_valid = validator['check'](code)
    return jsonify({
        'success': is_valid,
        'hint': validator['hint'] if not is_valid else None
    })

@app.route('/api/run_code', methods=['POST'])
def run_code():
    init_progress()  # Initialize progress if not exists
    session['progress']['total_code_runs'] += 1
    session.modified = True
    
    data = request.get_json()
    code = data.get('code', '')
    lesson_category = data.get('category')
    lesson_id = data.get('lesson_id')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    # Validate code if lesson info provided
    if lesson_category and lesson_id:
        validator = LESSON_VALIDATORS.get(lesson_category, {}).get(lesson_id)
        if validator and not validator['check'](code):
            return jsonify({
                'error': 'Your solution might not be complete. ' + validator['hint'],
                'success': False,
                'is_hint': True
            })

    # Create a temporary file to run the code
    temp_file = None
    try:
        # Add restricted builtins
        restricted_code = """
__builtins__ = {name: __builtins__[name] for name in %s if name in __builtins__}
%s
""" % (repr(ALLOWED_BUILTINS), code)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(restricted_code)
            temp_file = f.name

        # Set up timeout handler (Unix only)
        if platform.system() != 'Windows':
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)  # 5 seconds timeout

        try:
            # Run the code in a separate process
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=5  # Timeout handled by subprocess on Windows
            )
            
            output = result.stdout
            error = result.stderr

            # Check for specific error patterns
            if error:
                # Clean up error message for display
                error_lines = error.split('\n')
                cleaned_error = '\n'.join(line for line in error_lines 
                                        if 'File "<string>"' not in line 
                                        and temp_file not in line)
                return jsonify({
                    'error': cleaned_error,
                    'success': False
                })

            return jsonify({
                'output': output,
                'success': True
            })

        except subprocess.TimeoutExpired:
            return jsonify({
                'error': 'Code execution timed out (limit: 5 seconds)',
                'success': False
            })
        except Exception as e:
            return jsonify({
                'error': f"Error executing code: {str(e)}",
                'success': False
            })

    except Exception as e:
        return jsonify({
            'error': f"Server error: {str(e)}",
            'success': False
        })
    finally:
        # Clean up the temporary file
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except:
                pass
        # Reset the alarm (Unix only)
        if platform.system() != 'Windows':
            signal.alarm(0)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True) 