from settings import IEDDIT, REDDIT
import settings, praw, ieddit, time

import database
database.init()

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

while True:
    for subieddit, subreddits in settings.SUB_MAP.items():
        subreddits = [reddit.subreddit(s) for s in subreddits]
        for subreddit in subreddits:
            submissions = subreddit.hot(limit = settings.IMAGES_PER_SUBREDDIT)
            for submission in submissions:

                # make sure it's not just a selfpost (text-only)
                if submission.is_self:
                    continue

                # make sure it hasn't already been reposted
                if database.submission_reposted(subieddit, submission.id):
                    continue
                
                # post it on ieddit
                try:
                    post = {
                        "title": submission.title + " [r-poster]",
                        "sub": subieddit,
                        "url": submission.url,
                        "nsfw": True # submission.over_18
                    }
                    post_id, post_url = ieddit.create_post(**post)
                except Exception as e:
                    print(e)
                    continue

                # store in database
                database.add_post([
                    submission.title, 
                    post_id, submission.id, 
                    post_url, 
                    "https://reddit.com" + submission.permalink, 
                    subieddit, 
                    subreddit.display_name, 
                    submission.url, 
                    int(time.time())
                ])