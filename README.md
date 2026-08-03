# YADM
Yet Another Dotfiles Manager

An interactive TUI for picking dotfiles and copying them into a separate `~/Dotfiles` folder, which you can then push to GitHub. Helps you reproduce your setup on a new machine: browse, select what you need, copy.

## Install

Requires [pipx](https://pipx.pypa.io/) (or `pip`).

```bash
pipx install git+https://github.com/xTeel-Code/YADM.git
```

Then run it from anywhere:

```bash
yadm
```

## Usage

- Arrow keys: move focus between directories
- Space: toggle selection (marked with `[x]`)
- Enter: copy all selected directories into `~/Dotfiles`
- `q`: quit
