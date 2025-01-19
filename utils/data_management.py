import json
import os

from libraries.player_library import character_library

# File to store character data
SAVE_DIR = "savedata"
CHARACTER_FILE = os.path.join(SAVE_DIR, "characters.json")

def load_characters_from_file():
    """
    Load character data from a JSON file.
    """
    try:
        with open(CHARACTER_FILE, "r") as file:
            character_library = json.load(file)
            print(f"Loaded character data from {CHARACTER_FILE}.")
    except FileNotFoundError:
        print(f"{CHARACTER_FILE} not found. Using default character library.")
    except json.JSONDecodeError:
        print(f"Error decoding {CHARACTER_FILE}. Using default character library.")

def save_characters_to_file():
    """
    Save character data to a JSON file.
    """
    try:
        with open(CHARACTER_FILE, "w") as file:
            json.dump(character_library, file, indent=4)
            print(f"Saved character data to {CHARACTER_FILE}.")
    except Exception as e:
        print(f"Error saving character data: {e}")