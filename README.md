# TwitterBot

Twitter bot that emulates a user

![twitter image](resources/images/example1.png)

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
4. Create a file named 'keys.ini' (optional)


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

Create a TwitterBot object using a username and keys.ini file. The keys in the file should be linked to the account which the bot will be tweeting from.
The username passed into the constructor is the username of the tweeter you would like to emulate.
```python
from twitter_bot import TwitterBot

if __name__ == '__main__':
    access_token = ""
    access_token_secret = ""
    api_key = ""
    api_key_secret = ""
    bot = TwitterBot('@laurarawra',
                     access_token=access_token,
                     access_token_secret=access_token_secret,
                     api_key=api_key,
                     api_key_secret=api_key_secret)
    bot.train_model(pull_tweets=True, model_type='markov')
    # bot.load_model(model_path='c:/path/to/model', model_type='markov')  # The model is stored when trained and can be loaded
    print('Generating a word: ', bot.generate_word())
    print('Generating a sentence: ', bot.generate_sentence())
    print('Reading tweets: ', bot.get_tweets())
    print('Tweeting message: ', bot.tweet_random_sentence())
```

Same thing, except this time using a .ini file to store the keys.
```python
from twitter_bot import TwitterBot

if __name__ == '__main__':
    bot = TwitterBot('@<twitter-username>', keys_path='c:/path/to/keys.ini')
    bot.train_model(save_path='c:/path/to/model', pull_tweets=True, model_type='markov')  # This may take some time
    # bot.load_model(model_path='c:/path/to/model', model_type='markov')  # The model is stored when trained and can be loaded
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