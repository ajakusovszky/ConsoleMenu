from console_menu.menu import Menu, MenuOption


def main():
    main_menu = Menu(
        title="My menu",
        options=[
            {
                "title": """  Help:
This is a help text of the menu
and it is multiline too!"""
            },
            {"title": "========="},
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
                    {
                        "title": "Submenu 3rd level",
                        "submenu": [
                            {
                                "title": "Submenu Option 3",
                                "function": lambda: print("Submenu Option 3 selected"),
                            },
                            {
                                "title": "Submenu Option 4",
                                "function": lambda: print("Submenu Option 4 selected"),
                            },
                        ],
                    },
                ],
            },
            {"title": "Decoration"},
        ],
    )

    main_menu.open_nested = False
    main_menu.add_frame = True
    main_menu.start()


if __name__ == "__main__":
    main()
