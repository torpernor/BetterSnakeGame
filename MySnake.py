import curses, time, random


def update_game(win: curses.window, game_dict):
    # note these are lists, therefore mutable
    loc_list: list[list] = game_dict["loc_list"]
    max_size = game_dict["max_size"]
    key = game_dict["key"]
    recent_key_list: list[str] = game_dict["recent_key_list"]
    loc_apple = game_dict["loc_apple"]

    # helper function, DO NOT MODIFY!!!!!!1!!
    def print(obj):
        win.clrtoeol()
        win.addstr(str(obj))

    # update recent key: must iterate through backwards to avoid overwriting
    for i in range(len(recent_key_list) - 1, 0, -1):
        recent_key_list[i] = recent_key_list[i - 1]
    opposites = {
        "w": "s",
        "a": "d",
        "s": "w",
        "d": "a",
    }
    # prevent dying by going backwards if snake is longer than 1
    if key in opposites and (len(recent_key_list) < 2 or recent_key_list[0] != opposites[key]):
        recent_key_list[0] = key

    # store tail cell for later
    tail = loc_list[-1].copy()

    for i, loc in enumerate(loc_list):
        recent_key = recent_key_list[i]

        # move snake cells
        if recent_key == "d":
            loc[0] += 1
        elif recent_key == "a":
            loc[0] -= 1
        elif recent_key == "w":
            loc[1] -= 1
        elif recent_key == "s":
            loc[1] += 1

        # wrap around if necessary
        if loc[0] >= max_size[0]:
            loc[0] = 0
        if loc[0] < 0:
            loc[0] = max_size[0] - 1
        if loc[1] >= max_size[1]:
            loc[1] = 0
        if loc[1] < 0:
            loc[1] = max_size[1] - 1

    # end game if snake head hits any other part of snake
    for loc in loc_list[1:]:
        if loc_list[0] == loc:
            game_dict["game_over"] = True
            break

    # if eat apple, grow one cell
    if loc_list[0] == loc_apple:
        while loc_apple in loc_list:
            loc_apple = [random.randint(0, max_size[0] - 1), random.randint(0, max_size[1] - 1)]
        loc_list.append(tail)
        recent_key_list.append(None)

    game_dict["recent_key_list"] = recent_key_list
    game_dict["loc_apple"] = loc_apple


def setup_terminal(win: curses.window):
    curses.cbreak()
    curses.noecho()
    win.nodelay(True)


def reset_terminal():
    curses.endwin()


def display_game(win: curses.window, game_dict):
    loc_list = game_dict["loc_list"]
    max_size = game_dict["max_size"]
    key = game_dict["key"]
    loc_apple = game_dict["loc_apple"]

    # ncurses package allows us to move cursor => we avoid
    # flickering by never actually clearing the screen

    # draw game board
    win.move(0, 0)
    win.addstr(" " + "-" * max_size[0] * 2 + " \n")
    for _ in range(max_size[1]):
        win.addstr("|" + " " * max_size[0] * 2 + "|\n")
    win.addstr(" " + "-" * max_size[0] * 2 + " \n")
    win.addstr(f"Key pressed: {key}\n")
    final_y, final_x = win.getyx()

    def print_at_game_loc(loc, obj):
        win.addstr(loc[1] + 1, loc[0] * 2 + 1, str(obj))

    # draw snake
    print_at_game_loc(loc_apple, "🍎")
    for loc in loc_list:
        print_at_game_loc(loc, "██")
    win.move(final_y, final_x)
    win.refresh()

def main():
    win = curses.initscr()
    # helper code for reading key input
    setup_terminal(win)

    max_size = [30, 10]
    game_dict = {
        "loc_list": [[5, 5]],
        "max_size": max_size,
        "key": None,
        "recent_key_list": [None],
        "loc_apple": [random.randint(0, max_size[0] - 1), random.randint(0, max_size[1] - 1)],
        "game_over": False,
    }

    try:
        for _ in range(0, 100000):
            # display grid (separate function)
            display_game(win, game_dict)
            if game_dict["game_over"]:
                score = len(game_dict["loc_list"])
                win.addstr(f"Game over! Final length: {score}\n")
                win.refresh()
                break

            # read input key as char
            try:
                game_dict["key"] = curses.keyname(win.getch()).decode("utf-8")
            except ValueError:
                game_dict["key"] = None

            if game_dict["key"] == "q":
                win.addstr("Game exited\n")
                win.refresh()
                break

            update_game(win, game_dict)
            time.sleep(0.1)
    finally:
        # this must run even if code is interrupted
        reset_terminal()

# sus

if __name__ == "__main__":
    main()