# GoogleDriveUpload

This project contains a small Python script for uploading files from the local
`uploads/` directory to Google Drive.  It uses the Google Drive API and stores a
`token.json` file after the first authorization so subsequent runs do not
require re-authentication.

## Installation

1. Ensure you have Python 3 available.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Obtaining `credentials.json`

The script expects a Google API OAuth client secret named
`credentials.json` in the project directory. To create it:

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Enable the **Google Drive API** for the project.
4. In **APIs & Services → Credentials**, create an **OAuth client ID** of type
   **Desktop application**.
5. Download the JSON file and save it as `credentials.json` next to
   `main.py`.

When you run the script for the first time it will open a browser window to
complete authorization and generate `token.json` for subsequent runs.

## Usage

Place the files you want to upload inside the `uploads/` folder and run:

```bash
python main.py
```

To upload the files into a specific Drive folder you can pass its ID with the
optional `--folder_id` argument:

```bash
python main.py --folder_id YOUR_FOLDER_ID
```

The folder ID can be found in the URL when viewing a folder in Google Drive.
