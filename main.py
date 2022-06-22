"""
Script to retrieve Spotify info and write it to a local file
"""
import asyncio
import time
from pprint import pprint

from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

TARGET_ID: str = "Spotify.exe"
FILE_NAME: str = "song_info.txt"
INTERVAL:  int = 1


async def get_media_info() -> dict:
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()

    if current_session: 
        if current_session.source_app_user_model_id == TARGET_ID:
            info = await current_session.try_get_media_properties_async()
            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
            info_dict["genres"] = list(info_dict["genres"])
            return info_dict

    raise Exception(f"{TARGET_ID} is not the current media session")


def write_to_file(txt):
    with open(FILE_NAME, "w") as f:
        f.write(txt)


if __name__ == "__main__":

    while True:

        try:
            info = asyncio.run(get_media_info())
            pprint(info)
            artist = info.get("artist", "")
            song = info.get("title", "")
            write_to_file(" - ".join([artist, song]))

        except KeyboardInterrupt:
            break

        except Exception as excp:
            print(f"Skipping! The following error occurred => {str(excp)}")

        time.sleep(INTERVAL)
