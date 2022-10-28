from unicodedata import name
from discord import Embed
from datetime import datetime, timezone


class NewsHelper:
    def  __init__(self, article, article_url):
        self.article = article
        self.article_url = article_url

    def create_embed(self):
        article = self.article
        article_url = self.article_url

        color = 0x000000

        article_title = article.find("h1", class_="article-body")
        article_type = article.find("div", class_="article-header").findChild().text

        if article_type == "News":
            color = 0x0000ff
        if article_type == "Events":
            color = 0xff8000
        if article_type == "Campaigns":
            color = 0x008000
        if article_type == "Shop":
            color = 0x008000
        if article_type == "Harvests":
            color = 0xff0000
        if article_type == "Issues":
            color = 0x6a3500

        time = datetime.now(timezone.utc)

        embed = Embed(title=article_title.text, type="rich", color=color)
        embed.url = article_url
        embed.set_author(name=article_type + " - " + time.strftime("%I:%M%p" + " UTC"))

        image_url = ""
        image_urls = [img["src"] for img in article.find_all("img")]
        if len(image_urls) > 1:
            image_url = image_urls[1]

            embed.set_image(url=image_url)

        return embed
