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
token = 'ya29.a0Ad52N3-VWvkIBbIOJrz24YRn-u5O6oDJG8jCwUWYQFGH3lmyBi9XCBQYIvQJ-L7oF3GPUQhkp8zP-Ykb7W8D27W5qXAPkBccx3Bi4713CBv0GjAFgzcs7su9eQ-0qQVEU2z0TRlaIOx-p6a-7ppANDKynAvdKCndmQaCgYKAU0SARESFQHGX2MiYTKcw8yp_oWM4dFCq-T8bA0169'

# Token validieren und decodieren
user_info = validate_and_decode_google_token(token)
if user_info:
    print("User Info:", user_info)
else:
    print("Invalid token.")
