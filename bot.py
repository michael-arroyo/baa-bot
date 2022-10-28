# discord.py import
import discord
from discord.ext import commands, tasks

# default library imports
import os
import requests

# non-default imports
from bs4 import BeautifulSoup

# local imports
from embed_helper import NewsHelper
from constants import  NEWS_MASTER_URL, NEWS_URL
from crud import session_scope, recreate_database
from models import News


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!eom", intents=intents)

token = os.getenv("DISCORD_BOT_TOKEN")


@tasks.loop(minutes=10)
async def post_news():
    guilds = bot.guilds
    guilds_chunked = []
    while guilds:
        try:
            guilds_chunked.append(guilds[:30])
            del guilds[:30]
        except IndexError:
            guilds_chunked.append(guilds)
            del guilds[:]

    news_soup = BeautifulSoup(requests.get(NEWS_URL).content, "html.parser")
    news_articles = news_soup.find_all("article", class_="article-item")

    for article in news_articles:
        article_id = article.find("a", class_="article-container")["href"].split("/")[-1].split("?")[0]

        with session_scope() as s:
            db_article = s.query(News).filter(News.newsMstId==article_id).first()

            if db_article is None:
                article_url = NEWS_MASTER_URL + article.find("a", class_="article-container")["href"]
                article_data = BeautifulSoup(requests.get(article_url).content, "html.parser")

                helper = NewsHelper(article_data, article_url)
                embed = helper.create_embed()

                new_news_db_entry = News(
                    newsMstId=article_id
                )
                s.add(new_news_db_entry)

                for chunk in guilds_chunked:
                    for guild in chunk:
                        channels = [channel for channel in guild.channels if channel.name == "announcements-news"]

                        for channel in channels:
                            try:
                                await channel.send(embed=embed)
                            except:
                                continue

    
@tasks.loop(hours=1)
async def update_db():
    print("Recreating database")
    recreate_database()


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------------")

    print("Starting tasks")
    update_db.start()
    post_news.start()
    print("Tasks started")
    print("------------")


if __name__ == "__main__":
    bot.run(token)
