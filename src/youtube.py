import datetime
from .google import create_service
from googleapiclient.http import MediaFileUpload


API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


class Youtube():

    def __init__(self, secret_file):
        self.client_secret_file = secret_file

    
    def upload(self, file, title, description, tags=[], privacyStatus='private'):
        service = create_service(self.client_secret_file, API_NAME, API_VERSION, SCOPES)

        upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'

        request_body = {
            'snippet': {
                'categoryI': 19,
                'title': title,
                'description': description,
                'tags': tags
            },
            'status': {
                'privacyStatus': privacyStatus,
                'publishAt': upload_date_time,
                'selfDeclaredMadeForKids': False, 
            },
            'notifySubscribers': True
        }

        mediaFile = MediaFileUpload(file)

        response_upload = service.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=mediaFile
        ).execute()

        """
        service.thumbnails().set(
            videoId=response_upload.get('id'),
            media_body=MediaFileUpload('thumbnails/thumb.jpg')
        ).execute()
        """
    
        return response_upload
