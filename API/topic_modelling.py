import re
import nltk

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

number_of_topics = 5
number_of_words = 5

def remove_links(tweet):
    tweet = re.sub(r'http\S+', '', tweet) # remove http links
    tweet = re.sub(r'bit.ly/\S+', '', tweet) # rempve bitly links
    tweet = tweet.strip('[link]') # remove [links]
    return tweet

def remove_users(tweet):
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove retweet
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove tweeted at
    return tweet

def remove_emojis(tweet):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    tweet = emoji_pattern.sub(r'', tweet)
    return tweet

my_stopwords = nltk.corpus.stopwords.words('english')
add_stopwords = ['co', '...']
my_stopwords.extend(add_stopwords)
word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem
my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@'

def clean_tweet(tweet):
    # tweet = remove_users(tweet)
    tweet = remove_links(tweet)
    # tweet = remove_emojis(tweet)
    # lower case
    tweet = tweet.lower()
    # strip punctuation
    tweet = re.sub('['+my_punctuation + ']+', ' ', tweet)
    tweet = tweet.replace('...', '')
    # remove double spacing
    tweet = re.sub('\s+', ' ', tweet)
    # remove numbers
    tweet = re.sub('([0-9]+)', '', tweet)
    tweet_token_list = [word for word in tweet.split(' ')
                            if word not in my_stopwords] # remove stopwords
    # stemming
    # tweet_token_list = [word_rooter(word) if '#' not in word else word
    #                     for word in tweet_token_list]

    tweet = ' '.join(tweet_token_list)
    return tweet

def display_topics(model, feature_names, number_of_words):
    topic_dict = {}
    for topic_idx, topic in enumerate(model.components_):
        topic_dict["words %d" % (topic_idx)]= ['{}'.format(feature_names[i])
                        for i in topic.argsort()[:-number_of_words - 1:-1]]
        topic_dict["weights %d" % (topic_idx)]= ['{:.1f}'.format(topic[i])
                        for i in topic.argsort()[:-number_of_words - 1:-1]]

    word_maps = []
    for i in range(number_of_topics):
        map = []
        for j in range(number_of_words):
            topic = {}
            topic['text'] = topic_dict['words ' + str(i)][j]
            topic['weight'] = topic_dict['weights ' + str(i)][j]
            map.append(topic)
        word_maps.append(map)
    return word_maps


def train_model(df):
    df['clean_tweet'] = df.tweet.apply(clean_tweet)

    # the vectorizer object will be used to transform text to vector form
    vectorizer = CountVectorizer(max_df=0.6, min_df=25, token_pattern='\w+|\$[\d\.]+|\S+')

    # apply transformation
    tf = vectorizer.fit_transform(df['clean_tweet']).toarray()

    # tf_feature_names tells us what word each column in the matric represents
    tf_feature_names = vectorizer.get_feature_names()

    model = LatentDirichletAllocation(n_components=number_of_topics, random_state=0)
    model.fit(tf)

    return display_topics(model, tf_feature_names, number_of_words)
