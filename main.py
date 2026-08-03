import curses
import shutil
import os
from pathlib import Path
def msgbox(stdscr, message: str):
    max_y, max_x = stdscr.getmaxyx()
    h, w = 5, max(len(message) + 4, 20)
    y, x = (max_y - h) // 2, (max_x - w) // 2

    win = curses.newwin(h, w, y, x)
    win.box()
    win.addstr(2, (w - len(message)) // 2, message)
    win.addstr(h - 2, (w - len("Press any key")) // 2, "Press any key", curses.A_DIM)
    win.refresh()
    win.getch()

    del win
    stdscr.touchwin()
    stdscr.refresh()

def get_entries() -> list:
    p = Path(".")
    return [d.name for d in p.iterdir() if d.is_dir()]


def get_child_entries(filename: str):
    p = Path("./" + filename)
    return [d.name for d in p.iterdir()]


def render_files(screen: curses.window, items: list):
    screen.clear()
    for i, entry in enumerate(items):
        screen.addstr(i + 1, 1, entry)
    screen.box()
    screen.refresh()


def ui_render(stdscr):
    curses.curs_set(0)
    max_y, max_x = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.refresh()

    file_win = curses.newwin(max_y - 1, max_x // 3, 0, 0)
    entries = get_entries()
    focused = 0
    selected = set()  # indices toggled on with Enter

    content_win = curses.newwin(max_y - 1, max_x - (max_x // 3), 0, max_x // 3)
    content_win.box()
    render_files(content_win, get_child_entries(entries[focused]))
    content_win.refresh()

    while True:
        file_win.clear()
        file_win.box()
        for i, item in enumerate(entries):
            attr = curses.A_REVERSE if i == focused else curses.A_NORMAL
            mark = "[x] " if i in selected else "[ ] "
            file_win.addstr(i + 1, 1, mark + item, attr)
        file_win.refresh()

        key = stdscr.getch()
        if not entries:
            continue
        if key == curses.KEY_UP:
            focused = (focused - 1) % len(entries)
            render_files(content_win, get_child_entries(entries[focused]))
        elif key == curses.KEY_DOWN:
            focused = (focused + 1) % len(entries)
            render_files(content_win, get_child_entries(entries[focused]))
        elif key == ord(" "):
            if focused in selected:
                selected.remove(focused)
            else:
                selected.add(focused)
        elif key in (curses.KEY_ENTER, ord('\n')):
            os.makedirs("./Dotfiles", exist_ok=True)
            for idx in selected:
                name = entries[idx]
                shutil.copytree(name, os.path.join("Dotfiles", name), dirs_exist_ok=True)
            msgbox(stdscr, f"Copied {len(selected)} item(s) to Dotfiles")
            return
        elif key == ord("q"):
            return


if __name__ == "__main__":
    curses.wrapper(ui_render)
