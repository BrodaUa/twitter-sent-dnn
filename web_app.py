import tornado.ioloop
import tornado.web
import tornado.template
import tweepy
import numpy as np

html = """
<!DOCTYPE html>
<html>
  <head>
    <title>
      DNN Twitter sentiment analysis
    </title>
    <script src="http://code.jquery.com/jquery-1.5.js"></script>
    <script>
      $(document).ready(function() {
        var text_max = 140;
        $('#tweet_count').html(text_max + ' characters left');

        $('#tweet').keyup(function() {
          var text_length = $('#tweet').val().length;
          var text_remaining = text_max - text_length;

          $('#tweet_count').html(text_remaining + ' characters left');
        });
      });
    </script>
    <script>
      $(document).ready(function() {
        var text_max = 50;
        $('#hashtag_count').html(text_max + ' characters left');

        $('#hashtag').keyup(function() {
          var text_length = $('#hashtag').val().length;
          var text_remaining = text_max - text_length;

          $('#hashtag_count').html(text_remaining + ' characters left');
        });
      });
    </script>
   
  </head>
  <body>
    <h1> 
      DNN Twitter sentiment analysis
    </h1>
    <div>
      <h3> 
        Single Tweet
      </h3>
      <form method="post" name="tweet_form">
        <div>
          <textarea name="tweet" id="tweet" rows="4" cols="50" placeholder="Input a tweet" maxlength="140"></textarea>
	  <br>
          <div id="tweet_count"></div>
        </div>	
        <input name="tweet_submit_button" type="submit">                        
      </form>
      The sentiment index is {{tweet_senti}}    
    </div>
    <br>
    <br>
    <div>  
      <h3> 
        Hashtag
      </h3> 
      <form method="post" name="hashtag_form">
        <div>
          <textarea name="hashtag" id="hashtag" rows="1" cols="50" placeholder="Input a hashtag" maxlength="50"></textarea>
       	  <br>
          <div id="hashtag_count"></div>
        </div>
        <input name="hashtag_submit_id" type="submit">                        
      </form>
      The sentiment index is {{hashtag_senti}}    
    </div>
    
  </body>
</html>
"""

CONSUMER_KEY = 'ncMZ2CP7YmScHkLYwmfCYaTZz'
CONSUMER_SECRET = 'ZkFEJXxXEOUlqkhrJ14kzWakrXjqIe11de7ks28DyC79P31t9q'
ACCESS_KEY = '1157786504-XB3DXGrMmhvM1PAb6aeys3LJFYI9Y3LzS6veRHj'
ACCESS_SECRET = '8w69uDRm9PPA9iv3fNtkHPKP4FIq5SFtVbcE28wtcY5qx'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        t = tornado.template.Template(html)
        self.write(t.generate(tweet_senti="0", hashtag_senti="0"))

    def post(self):
        tweet = self.get_argument("tweet", default="") 	    
        hashtag = self.get_argument("hashtag", default="")      
        t = tornado.template.Template(html)

	if tweet:
	    index = np.random.randn(1,1)[0][0]
            self.write(t.generate(tweet_senti=str(index), hashtag_senti="0"))
	elif hashtag:
    	    tweets = api.search(hashtag, count=100)
	    tweets_text = [tt.text for tt in tweets]
	    index = np.random.randn(1,1)[0][0]
            self.write(t.generate(tweet_senti="0", hashtag_senti=str(index)))
	else:
            self.write(t.generate(tweet_senti="0", hashtag_senti="0"))



application = tornado.web.Application([(r"/", MainHandler)], autoreload=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    

