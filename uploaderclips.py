import argparse
import sys
from os import listdir, remove
from time import sleep

from src import Twitch, Youtube
from src.utils import get_secrets


def main(channel, limit):

    secrets = get_secrets("credentials/twitch.json")
    twitch = Twitch(secrets["CLIENT_ID"], secrets["CLIENT_SECRET"])
    youtube = Youtube("credentials/youtube.json")

    response = twitch.search_clips(channel,limit=limit)
    slugs = []
    if response:
        slugs = [x["slug"] for x in response["clips"]]
    
    # Download Clips from Twitch
    print(f"[+] Downloading clips from channel: {channel}")
    for x in slugs:
        twitch.download_clip(x)
    
    # Upload Clips on Youtube
    clips = [f for f in listdir("clips") if ".gitkeep" not in f]
    print(f"[+] Uploading clips on Youtube...")
    for index, clip in enumerate(clips):
        title = clip.split("#")[1].replace(".mp4","").strip()
        response = youtube.upload(
            f"clips/{clip}",
            title,
            "Descrição genérica",
            ["LOL", "League of Legends", "clips"]
        )
        print(f"[+] Clip '{title}' status: {response.get('status').get('uploadStatus')}")
        if index != len(clips) - 1:
            print('[+] Waiting a time to not exceeded quota limit...')
            sleep(60)
    
    # Removes Downloaded Clips from directory
    for clip in clips:
        remove(f"clips/{clip}")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--channel")
    parser.add_argument("-l", "--limit")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        print(f"Usage: python3 {sys.argv[0]} --channel <name_channel_here> --limit <number_of_clips>" )
        sys.exit()
    
    args_dict = vars(args)
    channel = args_dict.get("channel")
    limit = args_dict.get("limit", 4)
    main(channel, limit)
