import os
import time
import re
import slack
import pprint
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tasks.jira import Jira
from notifier.notifier import Notifier
from notifier.client.slack import SlackClient


load_dotenv()
pp = pprint.PrettyPrinter(indent=4)

SLACK_TOKEN=os.getenv('SLACK_TOKEN')
client = slack.WebClient(token=SLACK_TOKEN)

if __name__ == "__main__":
    j = Jira()

    tasks = ', '.join([x.key for _, x in enumerate(j.filter())])

    notifier = Notifier()
    notifier.register(SlackClient())

    notifier.send(tasks)