# Living room game logic

book_titles = [
    "SILENT", "NIGHTFALL", "SECRETS", "HIDDEN", "DOORWAYS", "ECHOES"
]
bookmark_numbers = [2, 1, 1, 2, 1, 1]

letter_codes = {
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70,
    "G": 71, "H": 72, "I": 73, "J": 74, "K": 75, "L": 76,
    "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82,
    "S": 83, "T": 84, "U": 85, "V": 86, "W": 87, "X": 88,
    "Y": 89, "Z": 90
}

milestones = [
    "coffee_saved", "bookshelf_solved", "book_solved", "drawer_unlocked"
]

clue_names = {
    "coffee": "Coffee table",
    "word": "Bookmark word",
    "pin": "Drawer PIN",
    "photo": "Family photograph"
}

coffee_observation = (
    "Coffee has soaked into the napkin. "
    "The charging cable has no phone attached. "
    "The chair is pushed back."
)

photo_observation = (
    "The photograph shows a phone with a dark blue case "
    "and a pale diagonal scratch."
)

hints = {
    "bookshelf": [
        "Read the titles from left to right.",
        "Each bookmark number is a letter position, starting at 1.",
        "For example, the second letter of SILENT is I."
    ],
    "book": [
        "Use the uppercase letters in the recovered word.",
        "Find each letter's decimal code in the table.",
        "Keep only the last digit. For example, A is 65, so keep 5."
    ],
    "drawer": [
        "The open programming book helps you find the drawer PIN.",
        "Check the PIN you recorded in your notebook."
    ]
}


def new_game():
    game = {
        "coffee_saved": False,
        "bookshelf_solved": False,
        "book_solved": False,
        "drawer_unlocked": False,
        "photo_saved": False,
        "recovered_word": "",
        "recovered_pin": "",
        "inventory": [],
        "notebook": {},
        "hint_counts": {"bookshelf": 0, "book": 0, "drawer": 0},
        "phone_messages": [],
        "current_room": "living_room"
    }
    return game


def decode_books(titles, numbers):
    word = ""

    for i in range(len(titles)):
        # The bookmark starts at 1, but Python indexes start at 0.
        position = numbers[i] - 1
        word = word + titles[i][position]

    return word


def decode_pin(word, codes):
    pin = ""
    last_digit = lambda number: number % 10

    for letter in word:
        code = codes[letter]
        digit = last_digit(code)
        pin = pin + str(digit)

    return pin


def get_progress(game):
    completed = 0

    for item in milestones:
        if game[item]:
            completed = completed + 1

    return completed


def save_coffee(game):
    if game["coffee_saved"]:
        return True, "This observation is already in your notebook."
    else:
        game["coffee_saved"] = True
        game["notebook"]["coffee"] = coffee_observation
        return True, "Observation saved to your notebook."


def submit_word(answer, game):
    answer = answer.strip().upper()

    if game["bookshelf_solved"]:
        return True, "You already recovered the word."
    elif answer == "":
        return False, "Enter a word first."
    elif len(answer) != 6:
        return False, "Enter a six-letter word."

    for letter in answer:
        if letter not in letter_codes:
            return False, "Use English letters only."

    correct_word = decode_books(book_titles, bookmark_numbers)

    if answer == correct_word:
        game["bookshelf_solved"] = True
        game["recovered_word"] = correct_word
        game["notebook"]["word"] = correct_word
        return True, "Word recovered."
    else:
        return False, "Not quite, try again."


def validate_pin(answer):
    answer = answer.strip()

    if answer == "":
        return False, "Enter a PIN first."
    elif len(answer) != 6:
        return False, "Enter exactly six digits."

    for digit in answer:
        if digit not in "0123456789":
            return False, "Use digits from 0 to 9 only."

    return True, ""


def submit_book_pin(answer, game):
    if game["book_solved"]:
        return True, "The PIN is already in your notebook."
    elif not game["bookshelf_solved"]:
        return False, "Try harder.."

    valid, message = validate_pin(answer)
    if not valid:
        return False, message

    correct_pin = decode_pin(game["recovered_word"], letter_codes)

    if answer.strip() == correct_pin:
        game["book_solved"] = True
        game["recovered_pin"] = correct_pin
        game["notebook"]["pin"] = correct_pin
        return True, "PIN recorded."
    else:
        return False, "Check the last digit of each letter's code."


def unlock_drawer(answer, game):
    if game["drawer_unlocked"]:
        return True, "The drawer is already open."
    elif not game["bookshelf_solved"] or not game["book_solved"]:
        return False, "Work out the PIN using the books first."

    valid, message = validate_pin(answer)
    if not valid:
        return False, message

    correct_pin = decode_pin(game["recovered_word"], letter_codes)

    if answer.strip() == correct_pin:
        game["drawer_unlocked"] = True

        if "study_key" not in game["inventory"]:
            game["inventory"].append("study_key")

        return True, "The drawer opens. A key and photograph are inside."
    else:
        return False, "The drawer stays locked. Try again."


def save_photo(game):
    if not game["drawer_unlocked"]:
        return False, "The drawer is still locked."
    elif game["photo_saved"]:
        return True, "The photograph is already in your notebook."
    else:
        game["photo_saved"] = True
        game["notebook"]["photo"] = photo_observation
        return True, "Photograph saved to your notebook."


def get_hint(puzzle, game):
    number = game["hint_counts"][puzzle]

    if number >= len(hints[puzzle]):
        number = len(hints[puzzle]) - 1
    else:
        game["hint_counts"][puzzle] = number + 1

    return hints[puzzle][number]


def can_enter_study(game):
    if get_progress(game) == 4 and "study_key" in game["inventory"]:
        return True
    else:
        return False


def enter_study(game):
    if can_enter_study(game):
        # Keep the photograph even if the player did not press Save.
        save_photo(game)
        game["current_room"] = "study"
        return True, "The study door is unlocked."
    else:
        return False, "Finish the remaining living-room interactions first."


# Reflection prompts: write your own answers after trying the level.
# What was the most challenging part?
# Which Python concept did you enjoy using?
# What would you improve with more time?
