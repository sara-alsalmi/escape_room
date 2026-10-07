# The Last Door (آخر باب) — Escape Room Project

An interactive escape room game built with Python and Streamlit. The player wakes up in the basement of a house in Riyadh and moves through the house by finding clues, solving puzzles, and entering the correct answers to unlock the next room.

Two senders text the player along the way: a saved contact named "Fahad — Brother" and an unknown number. They give conflicting advice, and neither is labeled good or bad. At the courtyard gate the player must decide whom to trust. Solving every puzzle is not enough: a wrong decision still loses the game.

## Technologies Used

* **Python** — Game logic and backend functionality
* **Streamlit** — Interactive web interface
* **Git & GitHub** — Version control and project collaboration

## How to Run

```
python -m pip install -r requirements.txt
streamlit run app_try.py
```


The game loads its backgrounds from the `static/` folder, so static file serving must be enabled. Create `.streamlit/config.toml` with:

```
[server]
enableStaticServing = true
```

## Project Structure

* `app_try.py` — Runs the Streamlit interface: the intro screen, the story message screens, and every room page.
* `navigations.py` — Shared game state (current page, current room, solved puzzles), saving and restoring progress through the URL, and the Map, Phone and Notebook popups.
* `story.py` — The story text and the two senders' messages for each room.
* `room_1.py` — Basement: puzzle logic and popups.
*  `room_2.py` — majilis: puzzle logic and popups.
* `room_3.py` — Study: puzzle logic and popups.
* `room_4.py` — Courtyard: the final decision popup and the two endings.
* `assets/images/` — Puzzle pictures, one folder per room.
* `static/` — Room backgrounds, maps, and navigation icons.
* `requirements.txt` — Lists the Python packages needed to run the project.
* `.gitignore` — Lists files Git should ignore.

## Rooms

| Room | What the player does |
|---|---|
| Basement | Restores power, solves the storage box puzzle, repairs the mirror, and opens the key cabinet to find the way upstairs. |
| Majlis | 	Examines the coffee table and family photograph, solves the bookshelf and programming-book puzzles, unlocks the drawer, and finds the key to the Study. |
| Study | Solves three linked puzzles that open a wall safe. Each puzzle unlocks only after the previous one. |
| Courtyard | Makes the final decision at the gate. |

## How to Play

1. Launch the game using Streamlit and enter your first name.
2. Read the two messages on your phone at the start of each room.
3. Click objects in the room to open puzzles and read the clues carefully.
4. Enter your answers in the input fields. Use the hint button if you are stuck; hints only explain the puzzle and never favor either sender.
5. Use the Notebook to review your discoveries, the Map to see where you are, and the Phone to reread the messages.
6. A correct answer unlocks the next puzzle, and finishing a room's puzzles lets you move on.
7. At the courtyard gate, decide whether to open the door or keep it locked. Your choice decides the ending.


# Reflection

**What we built.** We turned an idea, an escape room where the player can solve every puzzle and still lose by trusting the wrong person, into a working multi-room game. The story, the puzzles, and the final decision all had to support that one idea.

**Working separately was the hardest part.** Each of us built our own part alone, and the parts did not fit together. One room created its own page, state, and links, while the main app used shared state and its own navigation. Bringing them together taught us that a team project needs an agreed structure before anyone writes code: how pages are named, where progress is stored, and what each file is responsible for.

**Understanding how Streamlit works.** We learned that Streamlit reruns the whole script on every interaction, so values must live in `st.session_state` and be created safely. Links that reload the page lose that state, so we saved progress in the URL to survive a refresh. We also learned to use dialogs for popups, to give every button a unique key, and to place clickable objects over a background image with CSS.

**Debugging real errors.** We fixed a syntax error, a missing session value, pictures that could not be found because of file paths, and a puzzle that was unfair because its answer did not match the real map of Saudi Arabia. These taught us to run the game often and to check our content, not just our code.

**Designing for the story.** Puzzles unlock evidence and access instead of telling the player whom to trust, the notebook records facts in neutral wording, and the hints never push the player toward either sender. Keeping the player's choice fair mattered as much as keeping the code correct.

**Collaboration with Git and GitHub.** Sharing the project through version control showed us how easily separate changes can conflict, and why small, frequent updates and clear file ownership help.


