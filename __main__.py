from settings import IEDDIT, REDDIT
import settings, praw, ieddit

reddit = praw.Reddit(
    client_id = REDDIT["CLIENT_ID"],
    client_secret = REDDIT["CLIENT_SECRET"],
    user_agent = REDDIT["USER_AGENT"],
    username = REDDIT["USERNAME"],
    password = REDDIT["PASSWORD"]
)


ieddit = ieddit.Client(
    username = IEDDIT["USERNAME"],
    password = IEDDIT["PASSWORD"], 
    _2captcha_api_key = settings._2CAPTCHA_API_KEY
)

