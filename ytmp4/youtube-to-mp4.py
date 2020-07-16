import json
import re
import urllib.request
import io

from pytube import YouTube

class Helper:
    def __init__(self):
        pass

    def id_from_url(self, url: str):
        return url.rsplit("/", 1)[1]

    def title_to_underscore(self, title: str):
        title = re.sub('[\W_]+', "_", title)
        return title.lower()


class YoutubeStats:
    def __init__(self, url: str):
        self.json_url = urllib.request.urlopen(url)
        self.data = json.loads(self.json_url.read())

    def print_data(self):
        print(self.data)

    def get_video_title(self):
        return self.data["items"][0]["snippet"]["title"]
    
    def get_video_description(self):
        return self.data["items"][0]["snippet"]["description"]
    
    def download_video(self, youtube_url: str, title: str):
        YouTube(youtube_url).streams.first().download(filename=title)

api_key = "AIzaSyCjSH_3pYyCSSc0p2NYkKKJqRjt-UJ2Lc8"

u_vid = "INPUT VIDEO URL HERE.csv"

with open(u_vid, "r") as f:
    content = f.readlines()

content = list(map(lambda s: s.strip(), content))
content = list(map(lambda s: s.strip(','), content))


helper = Helper()
for youtube_url in content:
    video_id = helper.id_from_url(youtube_url)
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    yt_stats = YoutubeStats(url)
    #yt_stats.print_data()
    title = yt_stats.get_video_title()
    title = helper.title_to_underscore(title)

    description = yt_stats.get_video_description()

    with io.open(f"{title}_description.txt", "w", encoding="utf-8") as f:
        f.write(description)

    yt_stats.download_video(youtube_url, title)

    print(title)

# s = "N\A"
# t = "N\A"
# print(helper.id_from_url(s))
# print(helper.title_to_underscore(t))

# video_id = "N\A"
# json_url = urllib.request.urlopen(url)
# data = json.loads(json_url.read())

# print(data)