from api import api_instagram
from collections import OrderedDict
import sched
import time
from datetime import datetime

from api.api_instagram import insta_send


#
class CommunicationManager:
    """
    Post format look like this:
    {"event_title":
        "datetime": (2023, 7, 4, 10, 30, 0)
        "apis": [Instagram, ISEPLife]
        "asset": "picture.jpg"
        "desc": "Workshop à venir ! Abonnez vous !"
    }
    """

    def __init__(self):
        self.schedule = OrderedDict()

    def add(self, post):
        """Add a post in the schedule"""
        self.schedule.update(post)

    def remove(self, post_key):
        """Remove a post from the schedule"""
        self.schedule.pop(post_key)

    def run(self):
        """
        Post all the posts in due time until the dict is empty. NEEDS TO BE REDONE USING ONLY SCHEDULE LIBRARY
        :return: None
        """
        while self.schedule:
            post = dict(self.schedule[0])
            datetime = post["datetime"]
            while self.wait_until(datetime) != "Over":
                continue
            for api in post["apis"]:
                if api == "Instagram":
                    insta_send(post["asset"], post["desc"])
            self.schedule.pop(post)

    def wait_until(target_datetime):
        """ Wait for the due date to unlock the software. NEEDS TO BE REDONE USING ONLY SCHEDULE LIBRARY"""
        scheduler = sched.scheduler(time.time, time.sleep)
        current_datetime = datetime.now()
        time_difference = (target_datetime - current_datetime).total_seconds()

        if time_difference <= 0:
            print("Time is up!")
            return "Over"

        scheduler.enter(time_difference, 1, lambda: print("Time is up!"))
        scheduler.run()
