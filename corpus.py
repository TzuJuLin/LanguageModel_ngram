from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import string
stop_words = set(stopwords.words('english'))

# read testing çcscdata and store it as the input
test_data = []
f = open("train.txt", "r")
for line in f:
    line = line.rstrip("\n")
    test_data.append([line])


def tokenization(text):

    # tokenize text
    tokenized = word_tokenize(text[0])

    # get a list of punctuations
    string.punctuation = string.punctuation + '"'+'"'+'-'+'''+'''+'—'+'--'

    # create a list of tokens to remove, including punctuations and stopwords
    removal_list = list(stop_words) + list(string.punctuation)

    # filter out the unwanted tokens
    tokenized = [word.lower()
                 for word in tokenized if word not in removal_list]
    return(tokenized)


def detokenize(tokens):

    # Ensure the first word of the returned string will be capitalized
    tokens[0] = tokens[0].title()

    # detokenization
    detokenized = TreebankWordDetokenizer().detokenize(tokens)
    return(detokenized)
