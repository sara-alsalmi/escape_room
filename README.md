# Escape Room Project (Python Project)

An interactive escape room game built with Python and Streamlit. Players start in the basement and progress through multiple rooms by finding clues, solving puzzles, and entering the correct answers to unlock the next level and ultimately escape.

## Technologies Used

- **Python** — Game logic and backend functionality
- **Streamlit** — Interactive web interface
- **Git & GitHub** — Version control and project collaboration


## How to Run 

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Project structure

- `app.py` — Runs the Streamlit interface.
- `game/rooms/` — Contains the python files for each room in the game. 
- `game_logic.py` — Holds the game logic that will be shared across rooms.
- `assets/` — Stores game images and other assets.
- `requirements.txt` — Lists the Python packages needed to run the project.
- `.gitignore` — Lists files Git should ignore.


## How to Play

1. Launch the game using Streamlit.
2. Start from the basement and read the clues carefully.
3. Solve the puzzle in each room.
4. Enter your answer in the provided input field.
5. A correct answer allows you to move to the next level.
6. Complete all rooms and puzzles to escape!


