# FlappyBird Game Second

A modernized Flappy Bird clone built in Python using Pygame.

> This folder is a sample of the files included in the installer package created with Inno Setup.

## Overview

This project includes:
- English UI and menu screens
- Main menu with Play, Options, and Exit
- Game over screen with high score tracking
- Persistent high score storage
- Background music and sound support
- PyInstaller-ready packaging logic

## Requirements

- Python 3.8+ (tested on Windows)
- Pygame

## Installation

1. Activate your Python virtual environment if you have one.
2. Install dependencies:

```powershell
pip install pygame
```

## Run the game

```powershell
python FlappyBird-Original.py
```

## Controls

- `Space`: Jump
- `Up` / `Down`: Navigate menus
- `Enter`: Select menu option
- `Left` / `Right`: Toggle sound in Options
- `Escape`: Return to menu or exit dialogs

## Project Structure

- `FlappyBird-Original.py` - main game script
- `imgs/` - image assets
- `README.md` - project documentation
- `*.mp3` - background music files

## Notes

The project includes a helper for PyInstaller asset bundling using `resource_path` for bundled execution.

Feel free to push this repository to GitHub with the same structure.
 
