import os
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scope specifically for managing drafts (safer than full send permissions)
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../res/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_gmail_draft(service, to_email, subject, message_text):
    message = EmailMessage()
    message.set_content(message_text)
    message['To'] = to_email
    message['Subject'] = subject

    # Encode the message as base64url string
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'message': {'raw': encoded_message}}

    # Create the draft
    draft = service.users().drafts().create(userId="me", body=create_message).execute()
    print(f"Draft created successfully. Draft ID: {draft['id']}")

if __name__ == "__main__":
    print("Authenticating with Gmail...")
    try:
        # Step 1: Initialize the service
        gmail_service = authenticate_gmail()
        
        # Step 2: Define test variables
        test_recipient = "chaturadilshankuruppu@gmail.com"
        test_subject = "Test Draft: API Integration Verification"
        test_body = "If you are reading this in your Gmail drafts folder, the python script is working perfectly!"
        
        # Step 3: Run the creation function
        print("Creating a test draft...")
        create_gmail_draft(gmail_service, test_recipient, test_subject, test_body)
        
        print("\nSuccess! Open your Gmail 'Drafts' folder in your browser to verify it is there.")
        
    except FileNotFoundError as e:
        if "../res/credentials.json" in str(e):
            print("\nError: Could not find 'credentials.json'.")
            print("Please ensure you have downloaded your OAuth client ID credentials from the Google Cloud Console and placed the file in this directory.")
        else:
            print(f"\nFile not found error: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
