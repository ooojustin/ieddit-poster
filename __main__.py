import settings
from ieddit_api import Client

client = Client(settings.USERNAME, settings.PASSWORD, settings._2CAPTCHA_API_KEY)
client.login()