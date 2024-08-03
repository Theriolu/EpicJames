import asyncio
import logging
import sys
import discord
from discord import app_commands
from epicstore_api import EpicGamesStoreAPI
from datetime import datetime, timedelta
import aioschedule
from dateutil import parser
import os
from keep_alive import keep_alive
import psycopg2
from dotenv import load_dotenv
import traceback
import hashlib
from typing import Optional

keep_alive()

try:
    load_dotenv()
except:
    print('error loading variables from .env')

MY_GUILD = discord.Object(id=int(os.environ.get('MYGUILD')))

# SQL SHII
try:
    conn = psycopg2.connect(
        dbname=os.environ.get('dbname'),
        user=os.environ.get('user'),
        password=os.environ.get('password'),
        host=os.environ.get('host'),
        port=os.environ.get('port')
    )
    print("Connected to database successfully!")
    cur = conn.cursor()
except psycopg2.Error as e:
    print("Unable to connect to the database:", e)

try:
    cur.execute('''
    CREATE TABLE IF NOT EXISTS guildvars (
        id SERIAL PRIMARY KEY,
        server VARCHAR(255),
        server_id BIGINT,
        channel_id BIGINT,
        UNIQUE (server_id)
    );
    ''')
    conn.commit()
    print('Table created, or already exists')
except psycopg2.Error as e:
    print("Unable to create table:", e)

# TABLE TO STORE DATA ABOUT CURRENT GAMES
try:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gamehistory (
            id SERIAL PRIMARY KEY,
            hash BIGINT NOT NULL,
            UNIQUE (hash)
        );
    """)
    conn.commit()
    print("Table created successfully!")
except Exception as e:
    print(f"Error creating table: {str(e)}")

try:
    cur.execute("""
        CREATE OR REPLACE FUNCTION delete_oldest_rows() RETURNS TRIGGER AS $$
        BEGIN
            IF (SELECT COUNT(*) FROM gamehistory) > 5 THEN
                DELETE FROM gamehistory
                WHERE id IN (
                    SELECT id FROM gamehistory
                    ORDER BY id ASC
                    LIMIT (SELECT COUNT(*) - 5 FROM gamehistory)
                );
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
    """)
    conn.commit()
    print("Stored procedure created successfully!")
except Exception as e:
    print(f"Error creating stored procedure: {str(e)}")

try:
    cur.execute("""
        CREATE TRIGGER limit_rows_after_insert
        AFTER INSERT ON gamehistory
        FOR EACH ROW
        EXECUTE FUNCTION delete_oldest_rows();
    """)
    conn.commit()
    print("Trigger created successfully!")
except Exception as e:
    print(f"Error creating trigger: {str(e)}")

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

TOKEN = os.environ.get('token')

class MyView(discord.ui.View):
    def __init__(self, applink=str, weblink=str):
        super().__init__(timeout=None)
    
        appbutton = discord.ui.Button(label='Open in Epic', style=discord.ButtonStyle.primary, url=str(applink), emoji='🚀')
        self.add_item(appbutton)

        webbutton = discord.ui.Button(label='Open in browser', style=discord.ButtonStyle.secondary, url=str(weblink), emoji='🌐')
        self.add_item(webbutton)

@client.tree.command()
@app_commands.rename(channel_sel='channel')
@app_commands.describe(channel_sel='The channel you want to get the notifications in; Defaults to current channel')
async def channel(interaction: discord.Interaction, channel_sel: discord.TextChannel = None):
    await interaction.response.defer()
    channel_sel = channel_sel or interaction.channel
    for ass in range(0,2):
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO guildvars (server, server_id, channel_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (server_id)
                DO UPDATE SET
                    server = EXCLUDED.server,
                    channel_id = EXCLUDED.channel_id;
            """, (interaction.guild.name, interaction.guild.id, channel_sel.id))
            conn.commit()
            print("Entry added successfully!")
        except Exception as e:
             print('Error adding server info: '+str(e))
             if conn is not None:
                conn.rollback()

    api = EpicGamesStoreAPI(locale='en-US', country='US', session=None)
    free_games = api.get_free_games()
    for i in range(0, len(free_games['data']['Catalog']['searchStore']['elements'])):
        if free_games['data']['Catalog']['searchStore']['elements'][i]['price']['totalPrice']['discount'] != 0:
            date = finder_date(free_games, free_games['data']['Catalog']['searchStore']['elements'][i]['title'], 'endDate')
            parsed_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            try:
                notif = discord.Embed(
                    description='\nOriginal price: ' + '**' + free_games['data']['Catalog']['searchStore']['elements'][i]['price']['totalPrice']['fmtPrice']['originalPrice'] + '**' +
                    '\nDeal expires: ' + parsed_date.strftime("%d.%m.%Y %H:%M") + ' GMT\n\n',
                    title='**' + free_games['data']['Catalog']['searchStore']['elements'][i]['title'] +' (' + free_games['data']['Catalog']['searchStore']['elements'][i]['effectiveDate'][:4] + ')**\n',
                    color=6148864
                )
                notif.set_image(url=str(free_games['data']['Catalog']['searchStore']['elements'][i]['keyImages'][0]['url']))
                notif.add_field(name='Description', value='*' + free_games['data']['Catalog']['searchStore']['elements'][i]['description'] + '*')
                await channel_sel.send(embed=notif, view=MyView(applink='http://188.225.36.132:56565/eglink/en-US/p/'+free_games['data']['Catalog']['searchStore']['elements'][i]['catalogNs']['mappings'][0]['pageSlug'], weblink='https://store.epicgames.com/en-US/p/'+free_games['data']['Catalog']['searchStore']['elements'][i]['catalogNs']['mappings'][0]['pageSlug']))
            except Exception as e:
                print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
                print(f"Error sending message: {str(e)}: {str(free_games['data']['Catalog']['searchStore']['elements'][i]['keyImages'][0]['url'])}")
                continue
            await asyncio.sleep(1)
    await interaction.followup.send(embed=discord.Embed(title="<:greencheck:1269307173029023767> Success!", description=f'{channel_sel.mention} will be used for notifications.', color=6148864).set_footer(text="You can use /channel again if you want to change it."))

def finder_date(data, title_to_find, datetype):
    for element in data['data']['Catalog']['searchStore']['elements']:
        if element['title'] == title_to_find:
            try:
                end_date = element['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0][datetype]
                return(end_date)
            except:
                end_date = element['promotions']['promotionalOffers'][0]['promotionalOffers'][0][datetype]
                return(end_date)

async def checkforupdates_en():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.environ.get('dbname'),
                user=os.environ.get('user'),
                password=os.environ.get('password'),
                host=os.environ.get('host'),
                port=os.environ.get('port')
            )
            print("Connected to database successfully!")
            cur = conn.cursor()
        except psycopg2.Error as e:
            print("Unable to connect to the database:", e)

        try:
            cur.execute("SELECT hash FROM gamehistory ORDER BY id DESC LIMIT 1;")
            result = cur.fetchone()
            if result is None:
                currentgames_en = 0
            else:
                currentgames_en = int(result[0])
        except Exception as e:
            print(f"Error retrieving the latest hash: {str(e)}")
            currentgames_en = 0  # Default value if there is an error

        api = EpicGamesStoreAPI(locale='en-US', country='US', session=None)
        free_games = api.get_free_games()
        new_hash = int(hashlib.sha1(str(free_games).encode("utf-8")).hexdigest(), 16) % (10 ** 8)
        if new_hash != currentgames_en:
            print('Games changed!')
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO gamehistory (hash)
                    VALUES (%s)
                    ON CONFLICT DO NOTHING;
                """, (new_hash,))
                print("Entry added successfully!")
                conn.commit()
            except Exception as e:
                print(f"Error inserting data: {str(e)}")
            cur = conn.cursor()
            cur.execute("SELECT channel_id FROM guildvars")
            allchannels = cur.fetchall()
            ch_id_list = [row[0] for row in allchannels]

            for i in range(0, len(free_games['data']['Catalog']['searchStore']['elements'])):
                if free_games['data']['Catalog']['searchStore']['elements'][i]['price']['totalPrice']['discount'] != 0:
                    date = finder_date(free_games, free_games['data']['Catalog']['searchStore']['elements'][i]['title'], 'endDate')
                    parsed_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
                    for individ in ch_id_list:
                        try:
                            notif = discord.Embed(
                                description='\nOriginal price: ' + '**' + free_games['data']['Catalog']['searchStore']['elements'][i]['price']['totalPrice']['fmtPrice']['originalPrice'] + '**' +
                                '\nDeal expires: ' + parsed_date.strftime("%d.%m.%Y %H:%M") + ' GMT\n\n',
                                title='**' + free_games['data']['Catalog']['searchStore']['elements'][i]['title'] +' (' + free_games['data']['Catalog']['searchStore']['elements'][i]['effectiveDate'][:4] + ')**\n',
                                color=6148864
                            )
                            notif.set_image(url=str(free_games['data']['Catalog']['searchStore']['elements'][i]['keyImages'][0]['url']))
                            notif.add_field(name='Description', value='*' + free_games['data']['Catalog']['searchStore']['elements'][i]['description'] + '*')
                            await client.get_channel(int(individ)).send(embed=notif, view=MyView(applink='http://188.225.36.132:56565/eglink/en-US/p/'+free_games['data']['Catalog']['searchStore']['elements'][i]['catalogNs']['mappings'][0]['pageSlug'], weblink='https://store.epicgames.com/en-US/p/'+free_games['data']['Catalog']['searchStore']['elements'][i]['catalogNs']['mappings'][0]['pageSlug']))
                        except Exception as e:
                            print(f"Error sending message: {str(e)}")
                            continue
                    await asyncio.sleep(1)
            await asyncio.sleep(1)
        else:
            print('Games are the same')
        await asyncio.sleep(600)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for new games!"))
    print("Ready!")

async def main():
    # Start the bot and the scheduled tasks
    await asyncio.gather(
        client.start(TOKEN),
        checkforupdates_en()
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print('start')
    asyncio.run(main())
