from __future__ import print_function
import os.path
import mimetypes
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import argparse

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

def get_drive_folder_id_by_name(service, folder_name):
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    if not folders:
        raise ValueError(f"No folder found with name: {folder_name}")
    if len(folders) > 1:
        print(f"Warning: Multiple folders named '{folder_name}' found. Using the first one.")
    return folders[0]['id']


if __name__ == '__main__':
    # Set your local folder path here
    folder_path = 'uploads'  # Change to your actual folder name

    # Allow optional drive_folder_id from command line
    parser = argparse.ArgumentParser(description='Upload all files in a folder to Google Drive.')
    parser.add_argument('--folder_id', default=None, help='Google Drive folder ID (optional)')
    args = parser.parse_args()

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            upload_file(file_path, drive_folder_id=args.folder_id)