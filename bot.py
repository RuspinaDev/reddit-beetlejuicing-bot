import praw
import os
import praw.helpers

reddit_username = os.environ['REDDIT_USERNAME']
r = praw.Reddit(user_agent='beetlejuicing bot by /u/{}'.format(reddit_username))
saved_comments = []

i = 0
for c in praw.helpers.comment_stream(r, subreddit='askreddit'):
    if i % 500 == 0:
        print "Comment {}...".format(i)
    i += 1
    if 'author' not in dir(c):
        continue
    # my username godlikeme
    if ('god likes' not in c.body) and ('God likes' not in c.body) and ('god hates' not in c.body) and ('God hates' not in c.body):
        # and ('avatar' not in c.body):
        continue

    print "====="
    print u"{} says: {}".format(c.author, c.body)
    saved_comments.append(c)
