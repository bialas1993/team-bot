import os
import time
import re
import slack
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tasks.jira import Jira
load_dotenv()

SLACK_TOKEN=os.getenv('SLACK_TOKEN')
client = slack.WebClient(token=SLACK_TOKEN)

if __name__ == "__main__":
    j = Jira()
    print("tasks", ', '.join([x.key for _, x in enumerate(j.filter())]))

    response = client.chat_postMessage(
        channel='#1234test',
        text="To tests: "
    )
    assert response["ok"]