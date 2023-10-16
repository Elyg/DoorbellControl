import requests

def send_telegram_message(message=None):
    if message:
        token = "***REMOVED***"
        userID = ***REMOVED***

        # Create url
        url = f'https://api.telegram.org/bot{token}/sendMessage'

        # Create json link with message
        data = {'chat_id': userID, 'text': message}

        # POST the message
        requests.post(url, data)
