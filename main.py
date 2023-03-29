# bot.py
import os

import discord
from dotenv import load_dotenv
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, insert, select, text)

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata_obj = MetaData()

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    conn.commit()
    print(result.all())


user_table = Table("User_level_Table", metadata_obj, Column("id", Integer, primary_key=True), Column(
    "username", String), Column("level", Integer), Column("exp", Integer))


metadata_obj.create_all(engine)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class botty(discord.Client):

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):

        if message.author.id == self.user.id:
            return
        else:
            org = message.author.id
            stmt = insert(user_table).values(username=org)

            with engine.connect() as conn:
                x = conn.execute(stmt)
                conn.commit()
                print(x.columns)


client = botty(intents=intents)
client.run(TOKEN)
