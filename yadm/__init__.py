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
    win_h, win_w = screen.getmaxyx()
    visible_rows = max(win_h - 2, 0)
    usable_width = max(win_w - 2, 0)
    for i, entry in enumerate(items[:visible_rows]):
        screen.addstr(i + 1, 1, entry[:usable_width])
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
    scroll = 0

    content_win = curses.newwin(max_y - 1, max_x - (max_x // 3), 0, max_x // 3)
    content_win.box()
    if entries:
        render_files(content_win, get_child_entries(entries[focused]))
    content_win.refresh()

    while True:
        file_win.clear()
        file_win.box()
        win_h, win_w = file_win.getmaxyx()
        visible_rows = max(win_h - 2, 0)
        usable_width = max(win_w - 2, 0)

        if entries:
            if focused < scroll:
                scroll = focused
            elif focused >= scroll + visible_rows:
                scroll = focused - visible_rows + 1

        for row, i in enumerate(range(scroll, min(scroll + visible_rows, len(entries)))):
            item = entries[i]
            attr = curses.A_REVERSE if i == focused else curses.A_NORMAL
            mark = "[x] " if i in selected else "[ ] "
            text = (mark + item)[:usable_width]
            file_win.addstr(row + 1, 1, text, attr)
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
            dotfiles_dir = Path.home() / "Dotfiles"
            dotfiles_dir.mkdir(exist_ok=True)
            for idx in selected:
                name = entries[idx]
                dest = dotfiles_dir / name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(name, dest)
            msgbox(stdscr, f"Copied {len(selected)} item(s) to {dotfiles_dir}")
            return
        elif key == ord("q"):
            return


def main():
    curses.wrapper(ui_render)


if __name__ == "__main__":
    main()
