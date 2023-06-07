from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import io
import os

CLIENT_SECRETS_FILE = "secret.json"

SCOPES = ['https://www.googleapis.com/auth/youtubepartner']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def list_captions(youtube, video_id):
    captions_request = youtube.captions().list(
        part="snippet",
        videoId=video_id
    )
    captions_response = captions_request.execute()

    return captions_response['items']


def download_caption(youtube, caption_id, output_file):
    caption_request = youtube.captions().download(id=caption_id)
    caption_file_content = caption_request.execute()

    with open(output_file, 'w') as file:
        file.write(caption_file_content)


if __name__ == '__main__':
    youtube = get_authenticated_service()
    video_id = ''
    captions = list_captions(youtube, video_id)
    for caption in captions:
        caption_id = caption['id']
        output_file = f"{caption_id}.txt"
        download_caption(youtube, caption_id, output_file)
