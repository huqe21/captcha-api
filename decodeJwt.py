import requests


def validate_and_decode_google_token(token):
    userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    
    # Header für die Anfrage, einschließlich des Access Tokens
    headers = {'Authorization': f'Bearer {token}'}

    # Führe den GET-Request aus
    response = requests.get(userinfo_url, headers=headers)

    # Überprüfe den Status-Code der Antwort
    if response.status_code == 200:
        # Anfrage war erfolgreich, parse die Antwort als JSON
        user_info = response.json()
        return user_info
    else:
        # Es gab ein Problem mit der Anfrage
        print(f"Failed to retrieve user info, status code: {response.status_code}")
        return None

# Beispiel Token
token = 'ya29.a0Ad52N39uu2FQzpsbUxUIXX7gYz8YJnndxmpqj44aWsKVfXsTC-1aQdURlrFoRNYGPGln5wen4RE00wTxyWIY2Y7UPtXoahwXdhB5paAhvmnLnRxY8jvHHf5bb3gXWl9T8fIo0vQNeMkBYQy3GzHbdAF1CQ0TpFKXbZwaCgYKAaoSARESFQHGX2MiZXUiphNOAYoc5NV_IBdf_A0170'

# Token validieren und decodieren
user_info = validate_and_decode_google_token(token)
if user_info:
    print("User Info:", user_info)
else:
    print("Invalid token.")
