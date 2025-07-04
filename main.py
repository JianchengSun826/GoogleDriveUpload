from __future__ import print_function
import os.path
import mimetypes
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these SCOPES, delete the token.json file
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def upload_file(file_path, drive_folder_id=None):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': os.path.basename(file_path)}
    if drive_folder_id:
        file_metadata['parents'] = [drive_folder_id]

    mime_type, _ = mimetypes.guess_type(file_path)
    media = MediaFileUpload(file_path, mimetype=mime_type)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name'
    ).execute()

    print(f"File '{file.get('name')}' uploaded with ID: {file.get('id')}")


if __name__ == '__main__':
    upload_file('example.txt')  # Replace with your file path
