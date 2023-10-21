import requests
import json
import os

def get_other_tokens(name):
    json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "other_tokens.json")
    if json_file_path:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            return data[name]
    return None
 
def send_telegram_message(message=None, token=None, chat_id=None):
    """Sends a message to the telegram chat

    Args:
        message (str, optional): Message to send to the chat. Defaults to None.
    """
    if message:
        token = token
        userID = chat_id

        # Create url
        url = f'https://api.telegram.org/bot{token}/sendMessage'

        # Create json link with message
        data = {'chat_id': userID, 'text': message}

        # POST the message
        requests.post(url, data)
