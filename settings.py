# File change some personal settings.

import pathlib

# Input your bot token here from Bot Father
telegram_api_token = '5873997594:AAEap5Z-W89scNDjhtp-i_kTAaHXdha5llg'

# Input update time
upd_time = 5

# If you want use local data storage for saving last video. Change this setting.
# By default - bot save last video in variable YoutubeRequest.new_video
save_in_local_storage = False

# Path to local data storage. You can change this setting
path_root = pathlib.Path.cwd()
path_rss = str(pathlib.Path(path_root, 'rss_story', 'last_rss.json'))
