from newspaper import Article
import random
import  string
import nltk
from sklearn.feature_extraction.text import  CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import  numpy as np
import  warnings
warnings.filterwarnings('ignore')

#download punkt package

nltk.download('punkt', quiet=True)

#get article
url = 'https://www.mayoclinic.org/diseases-conditions/kidney-cancer/symptoms-causes/syc-20352664'
article = Article(url)
article.download()
article.parse()
article.nlp()
corpus = article.text

#print the articles
print(corpus)

#tokenization
text = corpus
sentense_list = nltk.sent_tokenize(text) #list of setenses
print(sentense_list)

#A function to return a random greeting response to a users greeting
def greeting_response(text):
    text = text.lower()
    #bots greeting response
    bot_greetings = ['howdy', 'hi', 'hey', 'hello', 'hola']
    #user greetings
    user_greetings = ['hi', 'hey', 'hello', 'holla', 'greetings', 'wassup']
    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)

def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x=list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index


#create the bots response
def bot_response(user_input):
    user_input = user_input.lower()
    sentense_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentense_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0
    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] >0.0:
            bot_response = bot_response+ '' +sentense_list[index[i]]
            response_flag = 1
            j = j+1
        if j>3:
            break
    if response_flag ==0:
        bot_response = bot_response+ ' '+'I apologize, I dont understand.'
        sentense_list.remove(user_input)
        return bot_response

#start chart
print('Doc Bot: I am doctor bot. i will answer your questions. To exit, type Bye.')
exit_list = ['exit', 'see you later', 'bye', 'quit', 'break']
while(True):
    user_input = input()
    if user_input.lower() in exit_list:
        print('Doc bot: Chat with you later')
        break
    else:
        if greeting_response(user_input) != None:
            print('Doc Bot: ' +greeting_response(user_input))
        else:
            print('Doc Bot: '+bot_response(user_input))