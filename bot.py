import praw
import os
import praw.helpers

reddit_username = os.environ['REDDIT_USERNAME']
r = praw.Reddit(user_agent='beetlejuicing bot by /u/{}'.format(reddit_username))
submissions = r.get_subreddit('todayilearned').get_hot(limit=100)

i = 0
for s in submissions:
    print "Thread {}...".format(i)
    i += 1
    for c in praw.helpers.flatten_tree(s.comments):
        if 'author' not in dir(c):
            continue
        # my username godlikeme
        if ((('God' not in c.body) and ('god' not in c.body) or ('like' not in c.body)) and ('avatar' not in c.body)) or (c.score < 5):
            continue
        print "====="
        print u"{} says: {}".format(c.author, c.body)
