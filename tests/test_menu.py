from io import StringIO
import sys

from console_menu.menu import Menu, MenuOption


def capture_output(func, *args, **kwargs):
    # Redirect stdout to a StringIO buffer
    original_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        func(*args, **kwargs)  # Call the function that generates output
        captured_output = sys.stdout.getvalue()
    finally:
        sys.stdout.close()
        sys.stdout = original_stdout  # Restore the original stdout

    return captured_output


"""
Lets start with TDD approach, meaning writing test first, then code.
"""


def test_create_menu():
    """First, need a Menu object
    new: Menu class"""
    menu = Menu()
    assert menu is not None


def test_add_option():
    """If I add 1 option to it, the choice list should equal to 1
    new: Menu.options, Menu.add_option(title, function, submenu)
    """
    menu = Menu()
    option = MenuOption(title="Option 1")
    menu.add_option(option)
    assert len(menu.options) == 1


def test_add_option_all_types():
    """it should accept a function, a submenu, or a decorator
    new: storing parameters for add_option"""
    menu = Menu()
    # decorator
    menu.add_option(MenuOption(title="Option 2"))
    # function
    menu.add_option(
        MenuOption(title="Option 1", function=lambda: print("Selected Option 1"))
    )
    # submenu
    submenu = Menu()
    submenu.add_option(
        MenuOption(title="SubOption 1", function=lambda: print("Selected SubOption 1"))
    )
    menu.add_option(MenuOption(title="SubMenu", submenu=submenu))
    assert len(menu.options) == 3


def test_output_without_option():
    """Get options back for displaying it. An empty list with a title should have 1 row with a title at the top and 1 at the bottom for "exit"
    new: display_options() to put title and exit to it"""
    menu = Menu(title="Console Menu")
    display_options = menu.display_options()
    assert len(display_options) == 2
    assert display_options[0].title == "Console Menu"
    assert display_options[-1].title == "Exit menu"


def test_output_without_option_no_title():
    """Get options back for displaying it. An empty list with a title should have 1 row with a title at the top and 1 at the bottom for "exit"
    new: display_options() with empty title should return only the Exit menu"""
    menu = Menu()
    display_options = menu.display_options()
    assert len(display_options) == 1
    assert display_options[-1].title == "Exit menu"


def test_output_simple_option():
    """When got a decoration (function=None) line, don't write out a hotkey
    new: display_options() should handle decorators"""
    menu = Menu(title="Console Menu")
    menu.add_option(MenuOption(title="--decoration--"))

    display_options = menu.display_options()
    assert len(display_options) == 3
    assert display_options[1].title == "--decoration--"
    assert display_options[1].hotkey == ""


def get_example_submenu() -> Menu:
    """An example object for testing"""
    menu = Menu(title="Main menu", add_frame=False, open_nested=True)
    menu.add_option(
        MenuOption(title="Option 1", function=lambda: print("Selected Option 1"))
    )
    menu.add_option(MenuOption(title="--decoration--"))

    # notice that submenu's title and the option for it in the main menu is different
    submenu = Menu(title="You are at 2nd level")
    submenu.add_option(
        MenuOption(title="SubOption 1", function=lambda: print("Selected SubOption 1"))
    )
    submenu.add_option(
        MenuOption(title="SubOption 2", function=lambda: print("Selected SubOption 2"))
    )
    menu.add_option(MenuOption(title="SubMenu", submenu=submenu))
    return menu


def test_output_multioption_closedsubmenu():
    """If I add a submenu with closed state, it should display its name only
    new: display_options() should handle functions and submenus. Test closed state first for hotkeys
    """
    menu = get_example_submenu()
    menu.open_nested = False

    display_options = menu.display_options()
    assert (
        len(display_options) == 5
    )  # 5 options: 1 main menu title, 1 function, 1 decorator, 1 submenu, 1 exit menu
    hotkeys = list(filter(lambda x: x.hotkey != "", display_options))
    assert len(hotkeys) == 3  # 3 options: function, submenu, exit menu
    assert display_options[-2].title == "SubMenu"


def test_output_multioption_openedsubmenu():
    """If I add a submenu with opened state (default), it should display the flattened tree
    new: test nested submenu"""
    menu = get_example_submenu()

    display_options = menu.display_options()
    assert (
        len(display_options) == 7
    )  # 5 options: 1 main menu title, 1 function, 1 decorator, 1 submenu title, 2 functions from submenu, 1 exit menu
    hotkeys = list(filter(lambda x: x.hotkey != "", display_options))
    assert (
        len(hotkeys) == 5
    )  # 4 options: 1 function at main menu, 2 in submenu, 1 exit menu at bottom
    assert display_options[3].title == "SubMenu"


def test_output_multioption_submenu():
    """Test what is inside the submenu, if it only that displayed"""
    menu = get_example_submenu()
    menu.open_nested = False
    display_options = menu.display_options()

    submenu_display_options = display_options[-2].submenu.display_options()
    assert (
        len(submenu_display_options) == 4
    )  # 4 options: 1 title, 2 functions, 1 exit menu at bottom
    hotkeys = list(filter(lambda x: x.hotkey != "", submenu_display_options))
    assert (
        len(hotkeys) == 3
    )  # 3 options: 2 functions in submenu, 1 exit sub menu at bottom
    assert submenu_display_options[0].title == "You are at 2nd level"
    assert submenu_display_options[-1].title == "Back to previous menu"


def test_display():
    """It should display line by line what were in the options"""
    menu = get_example_submenu()
    display_options = menu.display_options()
    display = menu.display().splitlines()
    assert len(display) == len(display_options)


def test_menu_state():
    """I need to store where I'm in the menu system. A path variable?"""
    menu = get_example_submenu()
    display_options = menu.display_options()
    assert menu.parent is None
    assert id(menu) == id(display_options[3].submenu.parent)


if __name__ == "__main__":
    pass
