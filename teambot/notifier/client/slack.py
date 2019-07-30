import slack
import os
from .client import NotifyClient

class SlackClient(NotifyClient):
    def __init__(self):
        self.__client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))

    def send(self, msg):
        print("sending to slack")
        response = self.__client.chat_postMessage(
            channel=os.getenv('SLACK_CHANNEL'),
            text=msg
        )
        assert response["ok"]
        
