import json
import requests
from django.conf import settings

def verify_firebase_token(id_token):
    """
    Verify the Firebase ID token using Firebase Auth REST API
    
    Args:
        id_token: The ID token to verify
        
    Returns:
        The decoded token claims if validation is successful, None otherwise
    """
    firebase_api_key = settings.FIREBASE_AUTH.get('WEB_API_KEY')
    
    if not firebase_api_key:
        return None
    
    # Use Firebase Auth REST API to verify the token
    verify_url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={firebase_api_key}"
    
    try:
        response = requests.post(
            verify_url,
            data=json.dumps({"idToken": id_token})
        )
        
        if response.status_code == 200:
            data = response.json()
            if "users" in data and len(data["users"]) > 0:
                user_data = data["users"][0]
                return {
                    "email": user_data.get("email"),
                    "name": user_data.get("displayName", ""),
                    "user_id": user_data.get("localId")
                }
    except Exception as e:
        print(f"Firebase token verification error: {str(e)}")
    
    return None 