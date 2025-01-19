from libraries.player_library import character_library

def add_to_inventory(name: str, item: str) -> bool:
    """
    Add an item to a character's inventory.
    """
    if name in character_library:
        character_library[name]["inventory"].append(item)
        return True
    return False

def remove_from_inventory(name: str, item: str) -> bool:
    """
    Remove an item from a character's inventory.
    """
    if name in character_library and item in character_library[name]["inventory"]:
        character_library[name]["inventory"].remove(item)
        return True
    return False