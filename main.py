import discord
import os
import urllib3
import json
from dotenv import load_dotenv
from reddit import reddit

class MyBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        self.specific_channel = self.get_channel(int(os.getenv('CHANNEL')))
        print(f'Specific channel {"found" if self.specific_channel else "not found"}')

    async def on_message(self, message):
        if message.author == self.user or message.channel != self.specific_channel:
            return

        if message.content.lower().startswith('random'):
            subreddit = message.content.split()[1] if len(message.content.split()) > 1 else 'pics'
            await reddit(subreddit, message)

load_dotenv()
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
http = urllib3.PoolManager()
intents = discord.Intents.default()
intents.message_content = True
client = MyBot(intents=intents)
client.run(os.getenv('TOKEN'))
