# from google.oauth2 import id_token
# from google.auth.transport import requests
import requests



# CLIENT_ID="836212664164-9qe1rvnjdo7bjaes585a0fc18haaod1j.apps.googleusercontent.com"


url="https://oauth2.googleapis.com/tokeninfo?id_token="

def google_verify_oauth2_token(token):
    try:
        r = requests.post(url+token)
        r_json=r.json()

        # idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        # print("idinfo",idinfo)

        gmail_member_name = r_json['name']
        gmail_member_email = r_json['email']
        gmail_member_password = r_json['sub']
        gmail_member_src = r_json['picture']
        # print(gmail_member_name,gmail_member_email,gmail_member_password,gmail_member_src)
        return gmail_member_name,gmail_member_email,gmail_member_password,gmail_member_src
    except ValueError:
        print("Error")
        # Invalid token
        pass

#