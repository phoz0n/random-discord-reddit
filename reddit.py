import json
import discord
from urllib3 import PoolManager

http = PoolManager()
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'

async def reddit(subreddit, message: discord.Message):
    try:
        response = http.request('GET', f'https://www.reddit.com/r/{subreddit}/random.api', headers={'User-agent': useragent})
        data = json.loads(response.data)
        post_data = data[0]['data']['children'][0]['data']
        
        if 'gallery_data' in post_data:
            gallery = ' '.join(f'https://i.redd.it/{x["media_id"]}.jpg' for x in post_data['gallery_data']['items'])
            await message.reply(gallery)
        elif 'secure_media' in post_data and post_data['secure_media']:
            await message.reply(f"{post_data['title']} {post_data['secure_media']['reddit_video']['fallback_url']}")
        elif 'url' in post_data:
            await message.reply(f"{post_data['title']} {post_data['url']}")
        else:
            raise KeyError
    except (KeyError, IndexError):
        await message.reply('No post found')