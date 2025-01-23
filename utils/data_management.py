import json

def load_from_file(file_name, data):
    """
    Load data from a JSON files.
    """
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            print(f"Loaded data from {file_name}.")
    except FileNotFoundError:
        print(f"{file_name} not found. Using default.")
    except json.JSONDecodeError:
        print(f"Error decoding {file_name}. Using default.")

def save_to_file(file_name):
    """
    Save data to a JSON files.
    """
    try:
        with open(file_name, "w") as file:
            json.dump(file_name, file, indent=4)
            print(f"Saved data to {file_name}.")
    except Exception as e:
        print(f"Error saving data: {e}")