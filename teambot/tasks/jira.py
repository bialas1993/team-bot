from jira import JIRA
import re
import os

class Jira(object):
    """
    Manager for jira
    """
    def init(self, url, token):
        self.url = url
        self.token = token

    def filter(self):
        jc = JIRA(server=os.getenv('JIRA_URL'), options={'verify': False}, basic_auth=(os.getenv('JIRA_USER'), os.getenv('JIRA_PASS'),))
        return jc.search_issues( '='.join(['filter', os.getenv('JIRA_TESTS_FILTER')]))