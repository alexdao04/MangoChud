import json
import os

def load_tracked_messages():
    """Load tracked messages from JSON file"""
    if os.path.exists('tracked_messages.json'):
        try:
            with open('tracked_messages.json', 'r') as f:
                data = json.load(f)
                return {int(k): v for k, v in data.items()}
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading tracked messages: {e}")
            return {}
    return {}

def save_tracked_messages(tracked_messages):
    """Save tracked messages to JSON file"""
    try:
        with open('tracked_messages.json', 'w') as f:
            data = {str(k): v for k, v in tracked_messages.items()}
            json.dump(data, f, indent=2)
        print("Tracked messages saved successfully")
    except Exception as e:
        print(f"Error saving tracked messages: {e}")

# Initialize the global variable
TRACKED_REACTION_MESSAGES = load_tracked_messages()