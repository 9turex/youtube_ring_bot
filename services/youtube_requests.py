import xmltodict
import requests
import json

from typing import Union

from settings import save_in_local_storage, path_rss


class YouTubeRequest:
    """
    Class for work with youtube requests. And save information about last video on channel

    :argument
    last_video (dict): Dict for save last video with notification
    new_video (dict): Dict for new video
    channel_id (string): Channel id for monitoring
    """

    last_video = {'name': '', 'link': ''}
    new_video = {'name': '', 'link': ''}

    def __init__(self, channel_id: str):
        self.channel_id = channel_id

    def request_youtube_rss(self) -> Union[bool, str]:
        """
        Method for request RSS feed from YouTube channel
        :return:
        False: if self.channel is empty
        Not find URL: if a request error has appeared

        """
        if self.channel_id:
            url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + self.channel_id
            try:
                rss_response_xml = requests.get(url, timeout=20)
                rss_response_json = xmltodict.parse(rss_response_xml.text)
                return rss_response_json
            except requests.ConnectionError:
                return 'Not find URL'
        else:
            return False

    def check_write_rss(self, rss_response_json) -> Union[dict, bool]:
        """
        Comparison method new and old videos
        :param rss_response_json: rss dict with all youtube feed
        :return:
            False: if videos are the same
            self.new_video: if new video
        """
        self.new_video['name'] = rss_response_json['feed']['entry'][0]['title']
        self.new_video['link'] = rss_response_json['feed']['entry'][0]['link']['@href']

        #print(datetime.datetime.now(), '\nlast request video: ', self.new_video, '\n storage video:', self.last_video)
        if self.new_video['name'] == self.last_video['name'] and self.new_video['link'] == self.last_video['link']:
            return False
        else:
            self.last_video['name'] = rss_response_json['feed']['entry'][0]['title']
            self.last_video['link'] = rss_response_json['feed']['entry'][0]['link']['@href']
            if save_in_local_storage:
                with open(path_rss, 'w', encoding='utf-8') as local_storage:
                    json.dump(self.new_video, local_storage, ensure_ascii=False)

            return self.new_video

