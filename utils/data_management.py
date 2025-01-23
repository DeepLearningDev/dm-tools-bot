import json
import os

def load_from_file(file_name, data):
    """
    Load data from a JSON file and update the provided dictionary.
    """
    try:
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                data.update(json.load(file))  # Update the existing dictionary
                print(f"Loaded data from {file_name}.")
        else:
            print(f"{file_name} not found. Using default.")
    except json.JSONDecodeError:
        print(f"Error decoding {file_name}. Using default.")

def save_to_file(file_name, data):
    """
    Save data to a JSON file.
    """
    try:
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)  # Serialize the actual data
            print(f"Saved data to {file_name}.")
    except Exception as e:
        print(f"Error saving data: {e}")
