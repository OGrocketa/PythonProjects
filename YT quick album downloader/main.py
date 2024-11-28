from pytubefix import Playlist
import json
import os

links_json = {}



link_to_playlist = ('https://www.youtube.com/playlist?list=OLAK5uy_nkff1O-MDh3A0zxDXCCG6c2-IQqpLdIgg')

p = Playlist(link_to_playlist)


playlsit_title = p.title

if not os.path.exists(f'./{playlsit_title}'):
    os.mkdir(f'./{playlsit_title}')

for vid in p.videos:
    video_title = vid.title
    vid.streams.filter(only_audio=True).first().download(output_path=f'./{playlsit_title}', filename=f'{video_title}.mp3')


