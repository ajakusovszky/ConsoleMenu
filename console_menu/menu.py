from dataclasses import dataclass, field
import os
from typing import Union, Callable


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class ConsoleMenuException(ValueError):
    def __init__(self, message="Custom error occurred"):
        self.message = message
        super().__init__(value=self.value, message=self.message)


@dataclass
class MenuOption:
    hotkey: str = field(init=False, default="")
    title: str
    function: Callable = None
    submenu: "Menu" = None


class Menu:
    def __init__(
        self,
        title: str = "",
        open_nested: bool = True,
        add_frame: bool = False,
        options: list[dict] = None,
    ):
        self.title = title
        self.open_nested = open_nested
        self.add_frame = add_frame
        self.options: list[MenuOption] = []
        # to know where we are in the menu tree, need to store the parent Menu
        self.parent: Menu = None
        # depth_level will be automatically adjusted by every display_options() call
        self.depth_level: int = 0
        if options is not None:
            for option_data in options:
                title = option_data.get("title")
                function = option_data.get("function")
                submenu = option_data.get("submenu")
                if submenu:
                    submenu_instance = Menu(
                        title=title, open_nested=self.open_nested, options=submenu
                    )
                    self.add_option(MenuOption(title=title, submenu=submenu_instance))
                else:
                    self.add_option(MenuOption(title=title, function=function))

    def add_option(self, item: MenuOption) -> None:
        """Adds an option to the Menu"""
        if item.function and item.submenu:
            raise ConsoleMenuException(
                message="Please only write a function or menu at an option."
            )
        self.options.append(item)

    def __init_menu_structure(
        self, depth_level: int = 0, menu_prechars: str = "", parent: "Menu" = None
    ):
        """Fills hotkey, depth_level, parent"""
        index = 1
        self.depth_level = depth_level
        self.parent = parent
        for option in self.options:
            if option.function or option.submenu:
                hotkey = (menu_prechars + "." if menu_prechars else "") + str(index)
                index += 1
                option.hotkey = hotkey
                if option.submenu:
                    option.submenu.open_nested = self.open_nested
                    option.submenu.add_frame = self.add_frame
                    option.submenu.__init_menu_structure(
                        depth_level=self.depth_level + 1,
                        menu_prechars=hotkey,
                        parent=self,
                    )

    def display_options(self) -> list[MenuOption]:
        """Creates a single level option list with hotkeys from the Menu.options, based on open_nested."""
        if self.parent is None:
            self.__init_menu_structure()
        lines: list[MenuOption] = []

        # at top level or any sublevel when the menu is not opened
        if (not self.open_nested or self.parent is None) and len(self.title) > 0:
            lines.append(MenuOption(title=self.title))

        for option in self.options:
            lines.append(option)
            # if it is in open_nested mode then pass the control at a submenu
            if option.submenu and self.open_nested:
                submenu_options = option.submenu.display_options()
                lines.extend(submenu_options)

        # finally attach the "exit" to the end
        if self.depth_level == 0:
            lines.append(MenuOption(title="Exit menu"))
            lines[-1].hotkey = "0"
        elif self.depth_level > 0 and not self.open_nested:
            lines.append(MenuOption(title="Back to previous menu"))
            lines[-1].hotkey = "0"

        return lines

    def display(self) -> str:
        """Write the menu into a string"""
        display_options = self.display_options()
        hotkey_format = (
            lambda x: x.hotkey
            if self.open_nested or x.hotkey == ""
            else x.hotkey.split(".")[-1]
        )
        hotkey_maxlen = max(
            [len(hotkey_format(x)) for x in display_options if x.hotkey != ""]
        )

        result: str = ""
        if not self.add_frame:
            for option in display_options:
                hotkey = f"{hotkey_format(option):>{hotkey_maxlen}}"
                if self.open_nested and option.submenu is not None:
                    hotkey = " " * hotkey_maxlen
                title = option.title.splitlines()
                result += f"{hotkey} {" "*self.depth_level*2}{title[0]}\n"
                for i in range(1, len(title)):
                    result += (
                        f"{" " * hotkey_maxlen} {" "*self.depth_level*2}{title[i]}\n"
                    )
        else:
            # get the lengthiest displayed line
            maxlen = 0
            for o in display_options:
                line_lengths = max([len(x) for x in o.title.splitlines()])
                maxlen = max(maxlen, line_lengths)
            border = "*" + ("-" * (maxlen + hotkey_maxlen + 4)) + "*\n"
            under_title = "*" + ("-" * (maxlen + hotkey_maxlen + 4)) + "*\n"

            result += border
            for index, option in enumerate(display_options):
                hotkey = f"{hotkey_format(option):>{hotkey_maxlen}}"
                if self.open_nested and option.submenu is not None:
                    hotkey = " " * hotkey_maxlen
                title = option.title.splitlines()
                line = f"{hotkey} {" "*self.depth_level*2}{title[0]}"
                result += f"| {line:<{maxlen + hotkey_maxlen + 2}} |\n"
                for i in range(1, len(title)):
                    line = f"{" " * hotkey_maxlen} {" "*self.depth_level*2}{title[i]}"
                    result += f"| {line:<{maxlen + hotkey_maxlen + 2}} |\n"
                if option.title != "" and index in [
                    0,
                    len(display_options) - 2,
                ]:  # after title of menu and exit
                    result += under_title
            result += border
        return result

    def start(self):
        """Writes the menu and wait for a hotkey, supports submenus"""
        while True:
            clear_screen()
            print(self.display())
            choice = input(f"Select an option: ").strip()
            if choice == "0":
                break

            # if in a submenu, attach the previous points before the choice
            if not self.parent is None:
                for x in self.parent.options:
                    if x.submenu and id(self) == id(x.submenu):
                        choice = x.hotkey + "." + choice
                        print(choice)
                        break

            option = [x for x in self.display_options() if x.hotkey == choice]

            if not option:
                input("Invalid choice. Press Enter to continue...")
            elif option[0].submenu:
                print(option[0].submenu.start())
            elif option[0].function:
                clear_screen()
                print(option[0].title)
                print("-------------")
                option[0].function()
                input("Press Enter to continue...")


if __name__ == "__main__":
    pass
