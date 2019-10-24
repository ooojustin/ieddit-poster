from settings import IEDDIT, REDDIT
import settings, praw, ieddit, time
from traceback import print_tb

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
    api_key = IEDDIT["API_KEY"]
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
                    post_data = {
                        "title": submission.title + " [r-poster]",
                        "sub": subieddit,
                        "url": submission.url,
                    }
                    post = ieddit.create_post(**post_data)
                except Exception as e:
                    print(e)
                    print_tb(e.__traceback__)
                    continue

                # store in database
                database.add_post([
                    submission.title, 
                    post.id, submission.id, 
                    post.permalink, 
                    "https://reddit.com" + submission.permalink, 
                    subieddit, 
                    subreddit.display_name, 
                    submission.url, 
                    int(time.time())
                ])

                time.sleep(settings.POST_DELAY)