from libraries.player_library import character_library

def get_character_stats(name: str) -> dict:
    """
    Retrieve stats for a character by name.
    """
    return character_library.get(name, None)

def update_character_stat(name: str, stat: str, value):
    """
    Update a specific stat for a character.
    """
    if name in character_library and stat in character_library[name]:
        character_library[name][stat] = value
        return True
    return False
