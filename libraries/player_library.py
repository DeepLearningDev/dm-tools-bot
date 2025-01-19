# A dictionary to store characters and their stats
character_library = {
    "Azalea": {
        "initiative_modifier": 3,
        "proficiency_bonus": 2,
        "armor_class": 14,
        "hit_points": 21,
        "str": 13,
        "str_mod": 1,
        "str_save": 1,
        "dex": 13,
        "dex_mod": 3,
        "dex_save": 3,
        "const": 13,
        "const_mod": 1,
        "const_save": 1,
        "int": 13,
        "int_mod": 1,
        "int_save": 1,
        "wis": 13,
        "wis_mod": 1,
        "wis_save": 3,
        "chr": 16,
        "chr_mod": 4,
        "chr_save": 6,
        "inventory": []

    },
    "Gorwick": {
        "initiative_modifier": 1,
        "proficiency_bonus": 2,
        "armor_class": 14,
        "hit_points": 36,
        "str": 17,
        "str_mod": 3,
        "str_save": 3,
        "dex": 13,
        "dex_mod": 1,
        "dex_save": 1,
        "const": 14,
        "const_mod": 2,
        "const_save": 2,
        "int": 11,
        "int_mod": 0,
        "int_save": 0,
        "wis": 14,
        "wis_mod": 2,
        "wis_save": 4,
        "chr": 10,
        "chr_mod": 0,
        "chr_save": 2,
        "inventory": []
        
    },
    "Globius": {
        "initiative_modifier": 1,
        "proficiency_bonus": 2,
        "armor_class": 11,
        "hit_points": 20,
        "str": 12,
        "str_mod": 1,
        "str_save": 1,
        "dex": 12,
        "dex_mod": 3,
        "dex_save": 3,
        "const": 14,
        "const_mod": 2,
        "const_save": 2,
        "int": 18,
        "int_mod": 4,
        "int_save": 6,
        "wis": 15,
        "wis_mod": 2,
        "wis_save": 4,
        "chr": 8,
        "chr_mod": -1,
        "chr_save": -1,
        "inventory": []
        
    },
        "Klud": {
        "initiative_modifier": 1,
        "proficiency_bonus": 2,
        "armor_class": 15,
        "hit_points": 32,
        "str": 18,
        "str_mod": 4,
        "str_save": 6,
        "dex": 12,
        "dex_mod": 1,
        "dex_save": 1,
        "const": 14,
        "const_mod": 2,
        "const_save": 4,
        "int": 12,
        "int_mod": 1,
        "int_save": 1,
        "wis": 11,
        "wis_mod": 0,
        "wis_save": 0,
        "chr": 7,
        "chr_mod": -2,
        "chr_save": -2,
        "inventory": []
        
    },
        "Mesmir": {
        "initiative_modifier": 4,
        "proficiency_bonus": 2,
        "armor_class": 15,
        "hit_points": 24,
        "str": 15,
        "str_mod": 2,
        "str_save": 2,
        "dex": 19,
        "dex_mod": 4,
        "dex_save": 6,
        "const": 16,
        "const_mod": 3,
        "const_save": 3,
        "int": 12,
        "int_mod": 0,
        "int_save": 2,
        "wis": 12,
        "wis_mod": 1,
        "wis_save": 1,
        "chr": 11,
        "chr_mod": 0,
        "chr_save": 0,
        "inventory": []
        
    },
        "Rogath": {
        "initiative_modifier": 2,
        "proficiency_bonus": 2,
        "armor_class": 16,
        "hit_points": 35,
        "str": 19,
        "str_mod": 4,
        "str_save": 6,
        "dex": 14,
        "dex_mod": 2,
        "dex_save": 2,
        "const": 16,
        "const_mod": 3,
        "const_save": 5,
        "int": 18,
        "int_mod": 4,
        "int_save": 4,
        "wis": 10,
        "wis_mod": 0,
        "wis_save": 0,
        "chr": 8,
        "chr_mod": -1,
        "chr_save": -1,
        "inventory": []
        
    },
}

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
