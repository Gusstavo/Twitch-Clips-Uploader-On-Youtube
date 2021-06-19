import requests
import os
import sys
import urllib.request

class Twitch():

    def __init__(self, client_id, client_secret, grant_type="client_credentials"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.token = self._get_token()
        self._validate_token()


    def _get_token(self):
        url = ("https://id.twitch.tv/oauth2/token?"
            f"client_id={self.client_id}&"
            f"client_secret={self.client_secret}&"
            f"grant_type={self.grant_type}")
        response = requests.post(url)
        if response.status_code != 200:
            raise Exception("Token cannot be generated")
        token = response.json()
        return token["access_token"]

    
    def _validate_token(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        response = requests.get("https://id.twitch.tv/oauth2/validate", 
                                headers=headers)
        if response.status_code != 200:
            raise Exception("Token cannot be validated")
        return True


    def search_channels(self, query):
        headers = {
            "client-id": self.client_id,
            "Authorization":  f"Bearer {self.token}",
        }
        params = (
            ('query', query),
        )
        response = requests.get("https://api.twitch.tv/helix/search/channels",
                                headers=headers,
                                params=params)
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return False
        return response.json()
    

    def search_streams(self, query, limit=10):
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            "Client-ID": self.client_id,
            "Authorization":  f"Bearer {self.token}",
        }
        params = (
            ('game', query),
            ('limit', limit)
        )
        response = requests.get("https://api.twitch.tv/kraken/streams/",
                                headers=headers,
                                params=params)
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return False
        return response.json()


    def search_clips(self, channel, period="all", limit=4):
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            "Client-ID": self.client_id,
            "Authorization":  f"Bearer {self.token}",
        }
        params = (
            ('channel', channel),
            ('period', period),
            ('limit', limit)
        )
        response = requests.get("https://api.twitch.tv/kraken/clips/top",
                                headers=headers,
                                params=params)
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return False
        return response.json()

    
    def download_clip(self, slug, basepath="./clips/"):
        headers = {
            "Client-ID": self.client_id,
            "Authorization":  f"Bearer {self.token}",
        }
        clip_info = requests.get(f"https://api.twitch.tv/helix/clips?id={slug}",
                                   headers=headers).json()
        data = clip_info['data'][0]
        thumb_url = data['thumbnail_url']
        mp4_url = thumb_url.split("-preview",1)[0] + ".mp4"
        out_filename = f"{data['broadcaster_name']}#{data['title']}.mp4"
        output_path = (basepath + out_filename)

        def dl_progress(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\r...%d%% - {data['title']}" % percent)
            sys.stdout.flush()

        if not os.path.exists(basepath):
            os.makedirs(basepath)

        try:
            urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
            print(f"\r...100% - {data['title']} - OK")
        except:
            print(f"\r...100% - {data['title']} - ERROR")
