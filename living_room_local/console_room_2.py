# A terminal version using the same game logic.
# Run this file with: python console_room_2.py

import room_2 as room

game = room.new_game()
player_name = input("Enter your name: ").strip()

if player_name == "":
    player_name = "Player"

print("Welcome to the living room,", player_name)

while game["current_room"] == "living_room":
    print("\nCompleted:", room.get_progress(game), "/ 4")
    print("1. Inspect coffee table")
    print("2. Solve bookshelf")
    print("3. Read programming book")
    print("4. Open drawer")
    print("5. Read notebook")
    print("6. Get a hint")
    print("7. Continue to study")
    print("0. Quit")

    choice = input("Choose a number: ").strip()

    if choice == "1":
        print(room.coffee_observation)
        save = input("Save this observation? (yes/no): ").strip().lower()

        if save == "yes":
            success, message = room.save_coffee(game)
            print(message)

    elif choice == "2":
        for title in room.book_titles:
            print(title)

        print("Left to right. One letter from each title.")
        print("Bookmark:", room.bookmark_numbers)
        answer = input("Enter the six-letter word: ")
        success, message = room.submit_word(answer, game)
        print(message)

    elif choice == "3":
        print("Uppercase letters and decimal Unicode codes:")

        for letter, code in room.letter_codes.items():
            print(letter, "->", code)

        print("One digit per letter. Keep the last digit.")

        if game["bookshelf_solved"]:
            print("Recovered word:", game["recovered_word"])
            answer = input("Enter the six-digit PIN: ")
            success, message = room.submit_book_pin(answer, game)
            print(message)
        else:
            print("Recover the bookshelf word first.")

    elif choice == "4":
        answer = input("Enter the drawer PIN: ")
        success, message = room.unlock_drawer(answer, game)
        print(message)

        if game["drawer_unlocked"]:
            print("A family photograph lies beneath the study key.")
            print(room.photo_observation)
            save = input("Save the photograph? (yes/no): ").strip().lower()

            if save == "yes":
                success, message = room.save_photo(game)
                print(message)

    elif choice == "5":
        if len(game["notebook"]) == 0:
            print("Your notebook is empty.")
        else:
            for clue, text in game["notebook"].items():
                print(room.clue_names[clue] + ":", text)

        print("Inventory:", game["inventory"])

    elif choice == "6":
        puzzle = input("Hint for bookshelf, book, or drawer? ")
        puzzle = puzzle.strip().lower()

        if puzzle in room.hints:
            print(room.get_hint(puzzle, game))
        else:
            print("Choose bookshelf, book, or drawer.")

    elif choice == "7":
        success, message = room.enter_study(game)
        print(message)

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Choose a number from the menu.")

if game["current_room"] == "study":
    print("Living room complete. This local version ends at the study door.")
