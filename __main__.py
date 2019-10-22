import settings
from ieddit_api import Client

client = Client(settings.USERNAME, settings.PASSWORD)
client.login()