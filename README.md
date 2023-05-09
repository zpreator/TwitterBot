# TwitterBot
Robot for twitter

Beep Beep Boop

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Only regret of getting married is that I never have to wear pants .</p>&mdash; Laura Bot (@fake_laurarawra) <a href="https://twitter.com/fake_laurarawra/status/1654326367423717376?ref_src=twsrc%5Etfw">May 5, 2023</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

The TwitterBot class provides an easy method to connect to the twitter API via Tweepy and emulate a user. Methods used to model the language are
1. Markov
2. LSTM model
3. GRU model

The primary packages are the following (some of which are smaller projects, like Gramformer)
- [Markovify](https://github.com/jsvine/markovify)
- [Gramformer](https://github.com/PrithivirajDamodaran/Gramformer)
- [Tweepy](https://github.com/tweepy/tweepy)
- [Tensorflow](https://github.com/tensorflow/tensorflow)
- [Spacy](https://github.com/explosion/spaCy)

# Prerequisites
1. Create a developer account with Twitter
2. Create and register an application
3. Generate the 4 unique keys
   - consumer_key 
   - consumer_secret
   - access_token
   - access_token_secret
4. Create a file named 'keys.ini'


```ini
[twitter]
access_token = <access_token>
access_token_secret = <access_token_secret>
api_key = <api_key>
api_key_secret = <api_key_secret>
```

# Installation
```commandline
pip install git+https://github.com/zpreator/TwitterBot
```

```commandline
python -m spacy download en_core_web_sm
```

# Usage
```python
from twitter_bot import TwitterBot

if __name__ == '__main__':
    bot = TwitterBot('@<twitter-username>')
    bot.train_model(pull_tweets=True, model_type='markov')  # This may take some time
    # bot.load_model('markov')  # The model is stored when trained and can be loaded
    print('Generating a word: ', bot.generate_word())
    print('Generating a sentence: ', bot.generate_sentence())
    print('Reading tweets: ', bot.get_tweets())
    print('Tweeting message: ', bot.tweet_random_sentence())
```

# Advanced Usage

This is an example of training an LSTM model with access to the model hyperparameters
```python
from twitter_bot import TwitterBot

if __name__ == '__main__':
    bot = TwitterBot('@<twitter-username>')
    bot.train_model(pull_tweets=True,
                    model_type='lstm',
                    rnn_units=256,
                    batch_size=32,
                    num_epochs=10)
    print(bot.generate_sentence(num_chars=280, seed='start'))

```