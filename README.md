# ConsoleMenu
A console menu for Python3.x scripts

## Use it
I needed a proper looking Console Menu for a simple project and carried away a bit while did this.
You can programatically load items into it, or simply use a tuplet at creation to load options.
Options contain either Decorations (like title, help), Submenus or functions to call.

Example: [example.py](example.py)

```python
from console_menu.menu import Menu

main_menu = Menu(
    title="My menu",
    options=[
        {
            "title": """  Help:
This is a help text of the menu
and it is multiline too!"""
        },
        {"title": "----"},
        {"title": "Option 1", "function": lambda: print("Option 1 selected")},
        {"title": "Option 2", "function": lambda: print("Option 2 selected")},
        {
            "title": "Submenu",
            "submenu": [
                {
                    "title": "Submenu Option 1",
                    "function": lambda: print("Submenu Option 1 selected"),
                },
                {
                    "title": "Submenu Option 2",
                    "function": lambda: print("Submenu Option 2 selected"),
                },
            ],
        },
    ],
)


main_menu.start()
```

The output will be:
```
    My menu
      Help:
    This is a help text of the menu
    and it is multiline too!       
    ----
  1 Option 1
  2 Option 2
    Submenu
3.1 Submenu Option 1
3.2 Submenu Option 2
  0 Exit menu

Select an option:
```

If you add open_nested=False and add_frame=True to the constructor, then this is the result:

```
*------------------------------------*
|   My menu                          |
*------------------------------------*
|     Help:                          |
|   This is a help text of the menu  |
|   and it is multiline too!         |
|   =========                        |
| 1 Option 1                         |
| 2 Option 2                         |
| 3 Submenu                          |
|   Decoration                       |
*------------------------------------*
| 0 Exit menu                        |
*------------------------------------*

Select an option:
```
