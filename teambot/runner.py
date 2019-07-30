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
SLACK_TOKEN=os.getenv('SLACK_TOKEN')
client = slack.WebClient(token=SLACK_TOKEN)


def list_users(channel):
    request = client.api_call("conversations.members", params={'channel': channel})
    if request['ok']:
        users = []
        for _, member in enumerate(request['members']):
            req = client.api_call("users.info", params={'user': member})
            users.append(req['user'])
        return users
    return None

def load_user_index():
    f = open(os.getenv("TESTER_FILE"), "r")
    line = f.readline()
    f.close()
    return line

def save_user_index(index):
    f = open(os.getenv("TESTER_FILE"), "w+")
    f.write(str(index))
    f.close()
    pass

if __name__ == "__main__":
    users = list_users(os.getenv('SLACK_CHANNEL'))
    try:
        user_index = int(load_user_index())
    except:
        user_index = 0
    
    j = Jira()
    tasks = ', '.join(["<" + os.getenv('JIRA_URL') + x.key + "|" + x.key + ">" for _, x in enumerate(j.filter())])
    
    user_index = user_index+1
    if user_index >= len(users):
        user_index = 0

    notifier = Notifier()
    notifier.register(SlackClient())

    msg = 'Dziś testuje {0}.\nDo testów z wczoraj: {1}'.format(users[user_index]['real_name'], tasks)  
    notifier.send(msg)

    save_user_index(user_index)