import textwrap
from PIL import Image, ImageDraw, ImageFont
import os
from instabot import Bot

USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

def insta_send(image_path, caption):
    """
    Post an image on Instagram with the Instagram credentials
    :param image_path: Path to the image
    :param caption: Caption of the image
    :return: None
    """
    bot = Bot()
    bot.login(username=USERNAME, password=PASSWORD)

    # Add exception handling (in case of errors)
    bot.upload_photo(image_path, caption=caption)

if __name__ == '__main__':
    pass