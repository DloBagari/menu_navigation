import json
import curses
import os
import subprocess
from time import sleep


KEY_RETURN = {curses.KEY_ENTER, ord("\n"), 13}
KEY_ONE = ord("1")
KEY_ZERO = ord("0")


class DrawMenu:
    # create a static amount of memory at object creation to store the specified attributes
    #_slots__ = ["__menu", "__previous_options", "__opt_color", "__selected_opt_color", "__stdscr"]

    def __init__(self, json_file_path):
        self.__menu = None
        self.__json_path = json_file_path
        self.__previous_options = None
        self.__opt_color = None
        self.__selected_opt_color = None
        self.__stdscr = None

    def __enter__(self):
        with open(self.__json_path) as f:
            self.__menu = json.load(f)
        # initialize a screen, which will represent the entire screen
        os.system("reset")

        self.__stdscr = curses.initscr()
        # disable automatic echoing of keys to the screen
        # turn on coloring
        try:
            curses.start_color()
        except:
            pass
        curses.noecho()
        # react to keys instantly.
        curses.cbreak()
        # activate returning keys's special values such as KEY_LEFT an this screen
        self.__stdscr.keypad(1)
        # disable border for
        self.__stdscr.border(0)
        # set colors
        self.__opt_color = curses.A_NORMAL
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.__selected_opt_color = curses.color_pair(1)
        curses.curs_set(1)
        curses.curs_set(0)
        curses.use_default_colors()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _draw_menu(self, menu, previous_menu):
        number_of_options = len(menu["options"])
        selected_opt = 0
        previous_opt = None
        last_option = "Go Back to {}".format(previous_menu["title"]) if previous_menu else "Exit"
        user_selection = None
        while user_selection not in KEY_RETURN:
            if selected_opt != previous_opt:
                previous_opt = selected_opt
                # display the program title
                self.__stdscr.addstr(1, 0, menu["title"], curses.A_UNDERLINE)
                # move cursor to next two line
                # display an order to user
                self.__stdscr.addstr(2, 0, menu["subtitle"], curses.A_BOLD)
                # move cursor to next line
                # display options
                for option in range(number_of_options):
                    opt_color = self.__selected_opt_color if selected_opt == option else self.__opt_color
                    # display the option on screen
                    self.__stdscr.addstr(3 + option, 0, "{}. {}".format(option + 1, menu["options"][option]["title"]), opt_color)
                    # if selected option is the last option, set coloring attribute to highlighting
                    # else set coloring attribute to normal
                    opt_color = self.__opt_color
                    # display last option
                if selected_opt == number_of_options:
                    opt_color = self.__selected_opt_color
                self.__stdscr.addstr(3 + number_of_options, 0,
                                         "{}. {}".format(number_of_options + 1, last_option), opt_color)
                # transmit all displays to the terminal, by refreshing the screen
                self.__stdscr.refresh()
            # ask for user input
            user_selection = self.__stdscr.getch()
            # convert users input to a number and update the selected position value
            if KEY_ONE <= user_selection <= ord(str(number_of_options + 1)):
                selected_opt = user_selection - KEY_ZERO - 1
               
            elif user_selection == curses.KEY_DOWN:
                selected_opt = selected_opt + 1 if selected_opt < number_of_options else 0
            elif user_selection == curses.KEY_UP:
                selected_opt = selected_opt - 1 if selected_opt > 0 else number_of_options
        return selected_opt

    def navigate(self, menu=None, previous_menu=None):
        if menu is None:
            menu = self.__menu
        number_of_options = len(menu["options"])
        exit_menu = False
        while exit_menu == 0:
            user_selection = self._draw_menu(menu, previous_menu)
            if user_selection == number_of_options:
                exit_menu = 1
            elif menu["options"][user_selection]["type"] == "menu":
                self.__stdscr.clear()
                self.navigate(menu["options"][user_selection], menu)
                self.__stdscr.clear()
            elif menu["options"][user_selection]["type"] == "exitmenu":
                exit_menu = 1
            elif menu["options"][user_selection]["type"] == "command":
                curses.def_prog_mode()
                os.system("reset")
                self.__stdscr.clear()
                os.system(menu["options"][user_selection]["command"])
                self.__stdscr.clear()
                curses.reset_prog_mode()
                curses.curs_set(1)
                curses.curs_set(0)




          
    

