# Tetris
Classic Tetris game implemented in Python using Pygame.

## Features
- Pure English interface, using built-in bitmap font (no external font files required)
- Cross-platform (Windows / Linux / macOS)
- Ghost piece preview, next piece preview, scoring and level system
- Supports both **WASD** and **arrow keys** for control

## Installation & Run
1. Make sure Python 3.6+ and pip are installed.
2. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```
   or just:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python tetris.py
   ```

## Controls
| Key(s)          | Action          |
|-----------------|-----------------|
| `A` / `←`       | Move left       |
| `D` / `→`       | Move right      |
| `S` / `↓`       | Soft drop       |
| `W` / `↑`       | Rotate          |
| `Space`         | Hard drop       |
| `R`             | Restart         |

## Scoring
- 1 line: 100 × level
- 2 lines: 300 × level
- 3 lines: 500 × level
- 4 lines: 800 × level
- Level increases every 10 cleared lines, which speeds up the falling.

## License
MIT License (optional)
