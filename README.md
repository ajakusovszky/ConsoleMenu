# ConsoleMenu

## TDD approach
This project was created using Test-Driven Development (TDD) style.

Writing down the necessary steps, if you want to start a similar project of your own.

### Step 1: Set Up Your Development Environment

Before you start, make sure you have Python installed on your system. You'll also need a code editor or IDE of your choice. Additionally, you can create a virtual environment to isolate your project dependencies:

```sh
# Create a virtual environment (optional but recommended)
python -m venv myenv

# Activate the virtual environment
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install necessary development tools
pip install pytest
```

### Step 2: Project Structure

Create a directory for your Python package and organize it with the following structure:
```
my_menu_package/
    ├── console_menu/
    │   ├── __init__.py
    │   ├── menu.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_menu.py
    ├── setup.py
    └── README.md
```

| Dir/Filename | Description |
| ------ | ------ |
| console_menu/ | This is your package directory where you'll put the code for your menu system. |
| tests/ | This directory is for your unit tests. |
| setup.py | This file is used for package distribution (optional if you're not planning to distribute your package). |
| README.md | Document your package and its usage. |

### Step 3: Write the First Test

Now, let's start with the first test for your multi-level console menu. In the test_menu.py file, you can write something like this:

```python
import pytest
from my_menu.menu import Menu

def test_create_menu():
    menu = Menu()
    assert menu is not None
```

### Step 4: Write the Minimum Code

In the menu.py file, start with the minimum code to make the test pass:

```python
class Menu:
    pass
```

### Step 5: Run the Test

Execute the test using pytest:

```bash
pytest
```

The test should pass since you've implemented the minimum code.

### Step 6: Expand Your Test Cases

Now, you can continue writing more test cases to specify the behavior of your menu system. For example:

```python
def test_add_option():
    menu = Menu()
    menu.add_option("Option 1", lambda: print("Selected Option 1"))
    assert len(menu.options) == 1

def test_select_option():
    menu = Menu()
    menu.add_option("Option 1", lambda: print("Selected Option 1"))
    menu.select_option(0)  # Select the first option
    # You can add assertions here to check the printed output or other expected behavior
```

### Step 7: Implement the Code

Now, you can implement the code in the Menu class to make these tests pass. Expand your menu.py file with the necessary code to handle options and user input.

### Step 8: Refactor and Continue

Continue writing test cases and implementing code, refactoring as needed to make your multi-level console menu system more feature-rich and robust.

### Step 9: Documentation

Don't forget to add docstrings and comments to your code for better maintainability and usability.

### Step 10: Packaging (Optional)

If you want to distribute your package, you can create a distribution package using tools like setuptools. Consult the Python documentation on packaging for more details.

That's a high-level overview of creating a Python package using TDD for a multi-level console menu. Remember to write tests before implementing code, and iterate on your design and tests as needed to achieve your desired functionality.
