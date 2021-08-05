import pandas as pd


def load_reddit_posts(reddit_api, subreddit, num_posts):
    """ Loads a reddit subreddit and its posts.

    Options for accessing are:
    (.hot, .new, .controversial, .top, and .gilded)

    Args:
        reddit_api (api object): reddit api object
        subreddit (str): name of subreddit
        num_posts (int): number of posts to grab (limit is 1000)
    """
    subreddit = reddit_api.subreddit(subreddit)
    top = subreddit.top(limit=num_posts)
    topics_dict = {"title": [],
                   "score": [],
                   "id": [], "url": [],
                   "comms_num": [],
                   "created": [],
                   "body": []}
    for submission in top:
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)
    topics_data = pd.DataFrame(topics_dict)
    return topics_data