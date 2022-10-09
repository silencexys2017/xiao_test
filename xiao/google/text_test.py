import hashlib
import requests as requests_urllib
import os
from google_auth_oauthlib import flow
from google.oauth2 import credentials, id_token
from googleapiclient import discovery
from google.auth.transport import requests

api_secret = "AIzaSyBqBmYI10dRSU6W_VlB0gwGpsn32RG6xuM"
redirect_uri = "https://mall.api.kilimall.ke/google/oauth2callback"
#  https://www.jianshu.com/p/995ca7739fb2
""" google token"""
uri = "https://oauth2.googleapis.com/tokeninfo?id_token={idToken}"

"https://mall.api.kilimall.ke/google/oauth2callback?" \
"state=a021232397fbb8e6164269ddbf95b2dab1dc836ff5feced1480cfb0ae93ce96b&" \
"code=4/0AX4XfWiTZxsDVb0gwIduLg2cbCzcr2-hUoYOIVAios9-4NJELSGpwa6u33FgSCA6Sw3tKQ&" \
"scope=email%20openid%20https://www.googleapis.com/auth/userinfo.email&" \
"authuser=0&prompt=consent"

CLIENT_IDS = [
    "642666820862-8jeg3qrd2u14j1bapn11ma7mhrli6i4q.apps.googleusercontent.com",
    "642666820862-rgp620nav944qulcbg88lbjikt5q0hsi.apps.googleusercontent.com"]


def get_authorization_url():
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required
    flow_obj = flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/drive.metadata.readonly',
                'https://www.googleapis.com/auth/userinfo.email'])

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow_obj.redirect_uri = redirect_uri
    random_state = hashlib.sha256(os.urandom(1024)).hexdigest()
    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow_obj.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='online',  # online,  offline
        state=random_state,
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true',
        login_hint='xianshengx860@gmail.com',
        prompt='consent',  # none, consent, select_account
        )

    print(authorization_url, state)
    return authorization_url


def verify_id_token(token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        # id_info = id_token.verify_oauth2_token(
        #     token, requests.Request(), CLIENT_IDS[0])

        # Or, if multiple clients access the backend server:
        id_info = id_token.verify_oauth2_token(token, requests.Request())
        print(id_info)
        if id_info['aud'] not in CLIENT_IDS:
            raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        print(id_info)
        user_id = id_info['sub']
    except ValueError:
        # Invalid token
        pass


def get_account_info_by_id_token(id_token):
    res = requests_urllib.get(
        url="https://oauth2.googleapis.com/tokeninfo",
        params={"id_token": id_token})
    print(res.request.url)
    print(res.status_code)
    google_account = res.json()
    print(google_account)


if __name__ == "__main__":
    # get_authorization_url()
    # verify_id_token("343243k43k")
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImJhMDc5YjQyMDI2NDFlNTRhYmNlZDhmYjEzNTRjZTAzOTE5ZmIyOTQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI5Njk2NDQ0NzAyMS1tMTFyNTRwNmM0aXBnN3FnZ2tyNmluOWEyZW5mbGEwOS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6Ijk2OTY0NDQ3MDIxLTJoaWNzZzNhYzJkb2NwMDA2c29oNHFpY20xN2czYWs4LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAwNjU4NTA5MjM4MjkzOTI0NzcxIiwiZW1haWwiOiJudW9udW8xNzIwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiTGVvIGxpdSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BTG01d3UzZjNBLXRtUDV5UjBJYWdyTzd3Y1RNdWYxSHJzZEsxVDhoU19KTj1zOTYtYyIsImdpdmVuX25hbWUiOiJMZW8iLCJmYW1pbHlfbmFtZSI6ImxpdSIsImxvY2FsZSI6InpoLUNOIiwiaWF0IjoxNjY0NTAyOTU5LCJleHAiOjE2NjQ1MDY1NTl9.k70ELwIRJAzRrjf1oJzVvW1q8vCbFlX2fhyayACIGO_4O9MhUSi0Y1rMQQeKXoeI_l_ZNAvRBdf7jqKKshuCHfqvzM-Z_IbielgBSHgcoj6A8s7EVca3qqaIbq5PHY8Mhk_YJI5JBkTnIg3TPxLbz65dAdGq51T5mLVLoiOdjnYh-AgyeidUNyzKAOv8SIsNRrvGd0si56qFxZidUIuU3c1NcH1GAWtHp1p5PdX0IqIw88tKu_tdujvgi7zM7_4MlOxvkLO2hpdgoUnEW42FJFc39ALWK04DcxPwg4qcOc7MBB6w2T0g8lRBnSfx8yFiSij0kzKqqhsl487cQA7OUw"
    # get_account_info_by_id_token(token)
    verify_id_token(token)