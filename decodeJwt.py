import requests


def validate_and_decode_google_token(token):
    userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    
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
token = 'ya29.a0Ad52N3-xj0zbYfYdzL9IkKqFWCrxmCo626r1_LFW8oWK6HJFieM0OkRXeWgtXvTZWXDRs6OeIoLDV0rKAHcRxH-CDy8x2YFtfg4gDPMmR_HIsil33tmLrKAbnVxBZiJtNqNAlg0HpYUJnRqqhkEH-M8i9l_H07hCsWoaCgYKAQUSARISFQHGX2Miuuvr4p_Vd1QfQosa-K8ZXQ0170'

# Token validieren und decodieren
user_info = validate_and_decode_google_token(token)
if user_info:
    print("User Info:", user_info)
else:
    print("Invalid token.")
