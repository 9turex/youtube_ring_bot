import copy

import xmltodict
import datetime
import requests
import settings
import json


class YouTubeRequest:

    last_video = {'name': '', 'link': ''}
    new_video = {'name': '', 'link': ''}

    def __init__(self, channel_id: str):
        self.channel_id = channel_id

    def request_youtube_rss(self):
        if self.channel_id:
            url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + self.channel_id
            try:
                rss_response_xml = requests.get(url, timeout=20)
                rss_response_json = xmltodict.parse(rss_response_xml.text)
                #print(datetime.datetime.now(), rss_response_json['feed']['entry'][0]['title'])
                return rss_response_json
            except BaseException:
                return 'Not find URL'
        else:
            return False

    def check_write_rss(self, rss_response_json: str):
        self.new_video['name'] = rss_response_json['feed']['entry'][0]['title']
        self.new_video['link'] = rss_response_json['feed']['entry'][0]['link']['@href']

        print(datetime.datetime.now(), '\nlast request video: ', self.new_video, '\n storage video:', self.last_video)
        if self.new_video['name'] == self.last_video['name'] and self.new_video['link'] == self.last_video['link']:
            return False
        else:
            self.last_video['name'] = rss_response_json['feed']['entry'][0]['title']
            self.last_video['link'] = rss_response_json['feed']['entry'][0]['link']['@href']
            return self.new_video

