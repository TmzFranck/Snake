# Snake Game

A classic snake game built using Python and Pygame.

## Features

- **Snake Movement**: Control the snake using arrow keys (`Up`, `Down`, `Left`, `Right`).
- **Food Collision**: Collect food to grow the snake and increase your score.
- **Dynamic Graphics**: Unique graphics for the snake's head, body, and tail for a polished appearance.
- **Difficulty Levels**: Choose between Easy, Medium, and Hard modes.
- **Score Tracking**: Save your high scores with player names in a database.
- **Game Over Conditions**:
  - Collision with the snake's own body.
  - Moving outside the game boundaries.
- **Pause/Resume**: Pause and resume the game with the `Spacebar`.
- **Mouse Support**: Select difficulty levels using mouse clicks.

## Requirements

- Python 3.8 or later
- Pygame library

Install the requirements using:

```bash
pip install -r requirements.txt
```

## Folder Structure

Ensure the following files are available:

```
project_directory/
│
├── graphics/
│   ├── apple.png
│   ├── head_up.png
│   ├── head_down.png
│   ├── head_right.png
│   ├── head_left.png
│   ├── tail_up.png
│   ├── tail_down.png
│   ├── tail_right.png
│   ├── tail_left.png
│   ├── body_horizontal.png
│   ├── body_vertical.png
│   ├── body_tr.png
│   ├── body_tl.png
│   ├── body_br.png
│   ├── body_bl.png
│
├── Font/
│   ├── PoetsenOne-Regular.ttf
│
├── main.py
```

## How to Run

1. Navigate to the project directory:
   ```bash
   cd project_directory
   ```
2. Run the game:
   ```bash
   python main.py
   ```

## Controls

| Key/Action   | Description       |
| ------------ | ----------------- |
| Arrow Keys   | Move the snake    |
| Spacebar     | Pause/Resume      |
| Mouse Click  | Select options    |
| R Key        | Restart game      |
| Q Key        | Quit game         |
| 1/2/3 Keys   | Select difficulty |
| Close Button | Exit the game     |

## Game Mechanics

1. Select a difficulty level at the start (Easy, Medium, or Hard).
2. The snake starts moving in the right direction by default.
3. When the snake eats the food, it grows, and the score increases.
4. If the snake collides with itself or the wall, the game ends.
5. After game over, you can:
   - Press R to restart the game
   - Press Q to quit and save your score
6. Enter your name to save your score in the database.

## Customization

- **Speed**: Adjust the snake's speed by changing the `pygame.time.set_timer(SCREEN_UPDATE, 150)` value in the `Game.run()` method. Lower values increase speed.
- **Grid Size**: Modify `HEIGHT` and `WIDTH` for a larger or smaller grid.

## Credits

- Graphics from the `graphics` folder.
- Font: PoetsenOne-Regular.ttf

Enjoy the game! 🎮
