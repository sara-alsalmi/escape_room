class Story:
    def __init__(self, player):
        self.player = player

        # one entry per room
        self.rooms = {
            "basement": {
                "background": "Basement_dark.jpeg",
                "text": f"{player}, you wake in the basement. You remember helping Fahad "
                        "with the boxes. The stairwell door is locked, and the house above "
                        "you is silent. Your phone lights up. Two senders. Two different "
                        "instructions.",
                "fahad": f"“{player}, stay calm. Find the emergency key. I can help you get outside.”",
                "unknown": f"“{player}, it's Fahad. I don't have my phone. You can come upstairs, but keep the outside gate closed.”",
                "button": "Start in the basement",
            },

            "majlis": {
                "background": "Majlis_dark.jpeg",
                "text": "The spare key turns, and the stairwell door opens. The house above "
                        "is quiet. Your phone lights up again.",
                "fahad": f"“Good, {player}. Go through the majlis. The study has the courtyard key.”",
                "unknown": "“You can move through the house. Keep the street gate locked. The security tablet is in the study box.”",
                "button": "Enter the majlis",
            },

            "study": {
                "background": "Study_dark.jpeg",
                "text": "The drawer slides open, and the study key is inside. Down the hall, "
                        "the study door waits. Your phone lights up again.",
                "fahad": "“Don't let that other number delay you. Find the key and meet me outside.”",
                "unknown": "“Check the blue case in the drawer. You'll recognize it in the gate records.”",
                "button": "Enter the study",
            },

            "courtyard": {
                "background": "Courtyard_dark.jpeg",
                "text": "The document box is open. You hold the security tablet and the "
                        "courtyard key. The courtyard door is ahead. Your phone lights up again.",
                "fahad": "“Those images are from earlier. I'm outside now. Bring the key.”",
                "unknown": "“Keep the gate closed. I'm bringing help.”",
                "button": "Go to the courtyard",
            },
        }

    def get(self, room):
        return self.rooms[room]