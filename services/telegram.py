import asyncio

import aiogram
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from services.keyboards import kb_change_channel, kb_add_channel, start_monitoring
from services.youtube_requests import YouTubeRequest

channel_youtube = YouTubeRequest('')


#@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
    await message.answer(text='Hello!')
    await message.delete()


class SettingYoutube(StatesGroup):
    channel = State()


#@dp.message_handler(commands=['channel_settings'], state=None)
async def help_func(message: types.Message):
    if channel_youtube.channel_id:
        await message.answer(text=f'Channel {channel_youtube.channel_id} is being monitored',
                             reply_markup=kb_change_channel)
    else:
        await message.answer('Ring has not channel for monitoring. Do you want add?',
                             reply_markup=kb_add_channel)


#@dp.callback_query_handler()
async def add_channel(callback: types.CallbackQuery):
    if callback.data == 'add_channel':
        await SettingYoutube.channel.set()
        await callback.message.answer(text='Input YouTube channel ID')

    elif callback.data == 'stop_settings':
        await callback.message.answer(text='OK, Print /channel_settings for change channel')
    elif callback.data == '':
        pass


#@dp.message_handler(state=SettingYoutube.channel)
async def write_channel(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['channel_id'] = message.text
        channel_youtube.channel_id = data['channel_id']
        await message.answer(f'Youtube channel : {data["channel_id"]} is monitored', reply_markup=start_monitoring)
        await state.finish()


#@dp.callback_query_handler(text='start_parsing')
async def monitoring_new_video(callback: types.CallbackQuery):
    if callback.data == 'start_parsing':
        print('whaaait')
        while True:
            rss_line = channel_youtube.request_youtube_rss()
            new_video = channel_youtube.check_write_rss(rss_line)
            print(new_video)
            try:
                if isinstance(new_video, dict):
                    await callback.message.answer(text=f"New video!\n {new_video['name']} \n {new_video['link']}")
            finally:
                #await callback.message.answer(text='No new video')
                await asyncio.sleep(5)


def register_handlers_tg(dp_name: Dispatcher):
    dp_name.register_message_handler(start_func, commands=['start'])
    dp_name.register_message_handler(help_func, commands=['channel_settings'], state=None)
    dp_name.register_message_handler(write_channel, state=SettingYoutube.channel)
    dp_name.register_callback_query_handler(monitoring_new_video, text='start_parsing')
    dp_name.register_callback_query_handler(add_channel)



