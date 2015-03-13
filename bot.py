import praw
import os
import praw.helpers

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from threading import Lock, Thread


class RedditWatcher(object):
    def __init__(self, subreddit, reddit_username):
        self.subreddit = subreddit
        self.r = praw.Reddit(user_agent='beetlejuicing bot by /u/{}'.format(reddit_username))
        # TODO: store comment body separately(to avoid api call in the flask app)
        self.comments_processed = 0
        self.matching_comments = []
        self.lock = Lock()

    def update_scores(self):
        for c in self.matching_comments:
            try:
                self.acq_lock()
                c.refresh()
                self.rel_lock()
            except Exception as e:
                print e
                self.rel_lock()

    def run(self):
        print "Background process is running"
        for c in praw.helpers.comment_stream(self.r, subreddit=self.subreddit, verbosity=0):
            print self.comments_processed
            self.acq_lock()
            if self.comments_processed % 500 == 0:
                self.rel_lock()
                self.update_scores()
                self.acq_lock()

            self.comments_processed += 1
            if 'author' not in dir(c):
                self.rel_lock()
                continue
            # my username godlikeme
            if ('god likes' not in c.body) and ('God likes' not in c.body) and ('god hates' not in c.body) and ('God hates' not in c.body):
                # and ('avatar' not in c.body):
                self.rel_lock()
                continue

            self.matching_comments.append(c)
            self.rel_lock()

    def acq_lock(self):
        self.lock.acquire()

    def rel_lock(self):
        self.lock.release()

reddit_username = os.environ['REDDIT_USERNAME']

app = Flask(__name__)
app.reddit_watcher = RedditWatcher('askreddit', reddit_username)
Bootstrap(app)


@app.route('/')
def index():
    try:
        print "Acquiring lock, index"
        app.reddit_watcher.acq_lock()
        print "Acquired lock, index"
        template = render_template('index.html', comments=app.reddit_watcher.matching_comments, comments_processed=app.reddit_watcher.comments_processed)
        app.reddit_watcher.rel_lock()
        return template
    except:
        app.reddit_watcher.rel_lock()

if __name__ == "__main__":
    thread = Thread(target=app.reddit_watcher.run)
    thread.start()
    app.run(debug=False)
