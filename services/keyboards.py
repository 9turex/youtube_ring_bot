from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

add_button = InlineKeyboardButton(text='Edit channel',
                                  callback_data='add_channel')
button_delete = InlineKeyboardButton(text='Delete channel',
                                     callback_data='remove_channel')
exit_button = InlineKeyboardButton(text='Exit from settings',
                                   callback_data='stop_settings')
change_button = InlineKeyboardButton(text='Change channel',
                                     callback_data='add_channel')
start_parse = InlineKeyboardButton(text='Start monitoring!',
                                   callback_data='start_parsing')

# change channel
kb_change_channel = InlineKeyboardMarkup(row_width=2)
kb_change_channel.add(change_button, exit_button)

# add channel
kb_add_channel = InlineKeyboardMarkup(row_width=2)
kb_add_channel.add(add_button, exit_button)

start_monitoring = InlineKeyboardMarkup(row_width=1)
start_monitoring.add(start_parse)
